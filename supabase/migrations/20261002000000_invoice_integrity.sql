-- ════════════════════════════════════════════════════════════════════
-- Factures : intégrité des montants + création atomique
--
-- Les totaux ne sont JAMAIS fournis par le client : ils sont recalculés
-- en base à partir des lignes et du taux de TVA, à chaque écriture.
-- Les lignes d'une facture ne sont modifiables qu'en brouillon.
-- ════════════════════════════════════════════════════════════════════

-- Taux de TVA en points de base (1800 = 18 %), source de vérité de tax_minor.
alter table public.invoices
  add column tax_rate_bp int not null default 0 check (tax_rate_bp between 0 and 10000);

-- Recalcule sous-total et TVA avant toute écriture sur une facture.
create or replace function private.invoice_compute_totals()
returns trigger
language plpgsql
set search_path = ''
as $$
begin
  select coalesce(sum(round(i.quantity * i.unit_price_minor)), 0)::bigint
    into new.subtotal_minor
    from public.invoice_items i
   where i.invoice_id = new.id;
  new.tax_minor := round(new.subtotal_minor * new.tax_rate_bp / 10000.0)::bigint;
  return new;
end;
$$;

create trigger invoices_compute_totals
  before insert or update on public.invoices
  for each row execute function private.invoice_compute_totals();

-- Lignes : verrouillées hors brouillon ; toute modification relance le calcul.
create or replace function private.invoice_items_guard()
returns trigger
language plpgsql
set search_path = ''
as $$
declare
  v_invoice uuid := coalesce(new.invoice_id, old.invoice_id);
  v_status public.invoice_status;
begin
  select status into v_status from public.invoices where id = v_invoice;
  -- v_status is null when the parent invoice itself is being deleted (cascade).
  if v_status is not null and v_status <> 'draft' then
    raise exception 'invoice_locked' using errcode = 'P0001',
      hint = 'Seules les factures en brouillon peuvent être modifiées.';
  end if;
  return coalesce(new, old);
end;
$$;

create or replace function private.invoice_items_touch()
returns trigger
language plpgsql
set search_path = ''
as $$
begin
  update public.invoices set updated_at = now()
   where id = coalesce(new.invoice_id, old.invoice_id);
  return null;
end;
$$;

create trigger invoice_items_guard
  before insert or update or delete on public.invoice_items
  for each row execute function private.invoice_items_guard();

create trigger invoice_items_touch
  after insert or update or delete on public.invoice_items
  for each row execute function private.invoice_items_touch();

-- Création atomique d'une facture et de ses lignes.
-- SECURITY INVOKER : le RLS de l'appelant s'applique à chaque lecture/écriture.
create or replace function public.create_invoice(
  p_client_id uuid,
  p_currency text,
  p_items jsonb,
  p_tax_rate_bp int default 0,
  p_issued_at date default current_date,
  p_due_at date default null,
  p_notes text default null
)
returns uuid
language plpgsql
security invoker
set search_path = ''
as $$
declare
  v_studio uuid;
  v_invoice uuid;
  v_year text := to_char(coalesce(p_issued_at, current_date), 'YYYY');
  v_seq int;
begin
  if jsonb_typeof(p_items) <> 'array'
     or jsonb_array_length(p_items) not between 1 and 100 then
    raise exception 'invalid_items' using errcode = '22023';
  end if;

  -- Le studio est déduit du client (visible uniquement si l'appelant en est membre).
  select studio_id into v_studio from public.clients where id = p_client_id;
  if v_studio is null then
    raise exception 'client_not_found' using errcode = 'P0002';
  end if;

  -- Numéro séquentiel par studio et par année : F-2026-0001.
  -- Le verrou consultatif sérialise les créations concurrentes du même studio.
  perform pg_advisory_xact_lock(hashtext('invoice_number:' || v_studio::text));
  select coalesce(max(nullif(split_part(number, '-', 3), '')::int), 0) + 1
    into v_seq
    from public.invoices
   where studio_id = v_studio
     and number ~ ('^F-' || v_year || '-[0-9]+$');

  insert into public.invoices (studio_id, client_id, number, currency, issued_at, due_at, tax_rate_bp, notes)
  values (v_studio, p_client_id, 'F-' || v_year || '-' || lpad(v_seq::text, 4, '0'),
          upper(p_currency), p_issued_at, p_due_at, p_tax_rate_bp, p_notes)
  returning id into v_invoice;

  insert into public.invoice_items (invoice_id, studio_id, description, quantity, unit_price_minor, position)
  select v_invoice, v_studio, it.description, it.quantity, it.unit_price_minor, (it.ord - 1)::int
    from rows from (jsonb_to_recordset(p_items) as (description text, quantity numeric, unit_price_minor bigint))
         with ordinality as it(description, quantity, unit_price_minor, ord);

  return v_invoice;
end;
$$;

revoke all on function public.create_invoice(uuid, text, jsonb, int, date, date, text) from public, anon;
grant execute on function public.create_invoice(uuid, text, jsonb, int, date, date, text) to authenticated;
