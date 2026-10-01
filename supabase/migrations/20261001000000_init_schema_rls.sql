-- ════════════════════════════════════════════════════════════════════
-- StyliZ — schéma initial + Row Level Security
--
-- Modèle multi-tenant : chaque donnée métier appartient à un « studio ».
-- Un utilisateur n'accède qu'aux studios dont il est membre.
-- RÈGLE : chaque table a RLS activé ; aucune n'est lisible sans policy
-- explicite. Les tables sans policy (ex. stripe_events) ne sont accessibles
-- qu'au service_role (webhooks serveur).
-- ════════════════════════════════════════════════════════════════════

create extension if not exists pgcrypto;

-- Schéma non exposé par l'API REST pour les fonctions d'aide RLS.
create schema if not exists private;
revoke all on schema private from public;
grant usage on schema private to authenticated;

-- ─── Types ──────────────────────────────────────────────────────────
create type public.studio_role as enum ('owner', 'admin', 'member');
create type public.design_status as enum ('draft', 'generating', 'ready', 'archived');
create type public.try_on_status as enum ('pending', 'processing', 'succeeded', 'failed');
create type public.invoice_status as enum ('draft', 'sent', 'paid', 'void', 'overdue');
create type public.listing_status as enum ('draft', 'published', 'archived');
create type public.payment_status as enum ('pending', 'succeeded', 'failed', 'refunded');

-- ─── Utilitaires ────────────────────────────────────────────────────
create or replace function private.set_updated_at()
returns trigger
language plpgsql
set search_path = ''
as $$
begin
  new.updated_at = now();
  return new;
end;
$$;

-- ─── Profils ────────────────────────────────────────────────────────
create table public.profiles (
  id uuid primary key references auth.users (id) on delete cascade,
  full_name text check (char_length(full_name) <= 100),
  avatar_url text check (char_length(avatar_url) <= 2048),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

-- ─── Studios & membres ──────────────────────────────────────────────
create table public.studios (
  id uuid primary key default gen_random_uuid(),
  name text not null check (char_length(name) between 1 and 120),
  default_currency char(3) not null default 'XOF' check (default_currency ~ '^[A-Z]{3}$'),
  created_by uuid not null default auth.uid() references auth.users (id) on delete restrict,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table public.studio_members (
  studio_id uuid not null references public.studios (id) on delete cascade,
  user_id uuid not null references auth.users (id) on delete cascade,
  role public.studio_role not null default 'member',
  created_at timestamptz not null default now(),
  primary key (studio_id, user_id)
);
create index studio_members_user_idx on public.studio_members (user_id);

-- Fonctions d'aide RLS : SECURITY DEFINER pour éviter la récursion des
-- policies sur studio_members ; search_path vide contre le détournement.
create or replace function private.is_member(p_studio uuid)
returns boolean
language sql
stable
security definer
set search_path = ''
as $$
  select exists (
    select 1 from public.studio_members m
    where m.studio_id = p_studio and m.user_id = (select auth.uid())
  );
$$;

create or replace function private.has_role(p_studio uuid, p_roles public.studio_role[])
returns boolean
language sql
stable
security definer
set search_path = ''
as $$
  select exists (
    select 1 from public.studio_members m
    where m.studio_id = p_studio
      and m.user_id = (select auth.uid())
      and m.role = any (p_roles)
  );
$$;

revoke all on function private.is_member(uuid) from public;
revoke all on function private.has_role(uuid, public.studio_role[]) from public;
grant execute on function private.is_member(uuid) to authenticated;
grant execute on function private.has_role(uuid, public.studio_role[]) to authenticated;

-- Le créateur d'un studio en devient automatiquement propriétaire.
create or replace function private.add_studio_owner()
returns trigger
language plpgsql
security definer
set search_path = ''
as $$
begin
  insert into public.studio_members (studio_id, user_id, role)
  values (new.id, new.created_by, 'owner')
  on conflict do nothing;
  return new;
end;
$$;

create trigger studios_add_owner
  after insert on public.studios
  for each row execute function private.add_studio_owner();

-- À l'inscription : profil + studio personnel.
create or replace function private.handle_new_user()
returns trigger
language plpgsql
security definer
set search_path = ''
as $$
declare
  v_name text := nullif(left(trim(new.raw_user_meta_data ->> 'full_name'), 100), '');
begin
  insert into public.profiles (id, full_name) values (new.id, v_name);
  insert into public.studios (name, created_by)
  values (coalesce('Studio ' || v_name, 'Mon studio'), new.id);
  return new;
end;
$$;

create trigger on_auth_user_created
  after insert on auth.users
  for each row execute function private.handle_new_user();

-- ─── Clients ────────────────────────────────────────────────────────
create table public.clients (
  id uuid primary key default gen_random_uuid(),
  studio_id uuid not null references public.studios (id) on delete cascade,
  full_name text not null check (char_length(full_name) between 1 and 120),
  email text check (char_length(email) <= 254),
  phone text check (char_length(phone) <= 32),
  measurements jsonb not null default '{}'::jsonb check (jsonb_typeof(measurements) = 'object'),
  notes text check (char_length(notes) <= 5000),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique (id, studio_id)
);
create index clients_studio_idx on public.clients (studio_id);

-- ─── Modèles (créations IA) ─────────────────────────────────────────
create table public.designs (
  id uuid primary key default gen_random_uuid(),
  studio_id uuid not null references public.studios (id) on delete cascade,
  title text not null check (char_length(title) between 1 and 160),
  description text check (char_length(description) <= 5000),
  prompt text check (char_length(prompt) <= 4000),
  image_path text check (char_length(image_path) <= 1024),
  status public.design_status not null default 'draft',
  created_by uuid default auth.uid() references auth.users (id) on delete set null,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique (id, studio_id)
);
create index designs_studio_idx on public.designs (studio_id);

-- ─── Essayages virtuels ─────────────────────────────────────────────
create table public.try_on_sessions (
  id uuid primary key default gen_random_uuid(),
  studio_id uuid not null references public.studios (id) on delete cascade,
  client_id uuid,
  design_id uuid not null,
  input_image_path text check (char_length(input_image_path) <= 1024),
  result_image_path text check (char_length(result_image_path) <= 1024),
  status public.try_on_status not null default 'pending',
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  -- FKs composites : impossible de lier un client/modèle d'un autre studio.
  foreign key (client_id, studio_id) references public.clients (id, studio_id) on delete cascade,
  foreign key (design_id, studio_id) references public.designs (id, studio_id) on delete cascade
);
create index try_on_studio_idx on public.try_on_sessions (studio_id);

-- ─── Facturation multi-devises ──────────────────────────────────────
-- Montants en unités mineures (centimes) ; XOF/XAF n'ont pas de décimales.
create table public.invoices (
  id uuid primary key default gen_random_uuid(),
  studio_id uuid not null references public.studios (id) on delete cascade,
  client_id uuid not null,
  number text not null check (char_length(number) between 1 and 40),
  currency char(3) not null check (currency ~ '^[A-Z]{3}$'),
  status public.invoice_status not null default 'draft',
  issued_at date,
  due_at date,
  subtotal_minor bigint not null default 0 check (subtotal_minor >= 0),
  tax_minor bigint not null default 0 check (tax_minor >= 0),
  total_minor bigint generated always as (subtotal_minor + tax_minor) stored,
  notes text check (char_length(notes) <= 5000),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique (studio_id, number),
  unique (id, studio_id),
  check (due_at is null or issued_at is null or due_at >= issued_at),
  foreign key (client_id, studio_id) references public.clients (id, studio_id) on delete restrict
);
create index invoices_studio_idx on public.invoices (studio_id, status);

create table public.invoice_items (
  id uuid primary key default gen_random_uuid(),
  invoice_id uuid not null,
  studio_id uuid not null,
  description text not null check (char_length(description) between 1 and 500),
  quantity numeric(12, 3) not null default 1 check (quantity > 0),
  unit_price_minor bigint not null check (unit_price_minor >= 0),
  position int not null default 0,
  created_at timestamptz not null default now(),
  foreign key (invoice_id, studio_id) references public.invoices (id, studio_id) on delete cascade
);
create index invoice_items_invoice_idx on public.invoice_items (invoice_id);

-- Paiements : écrits UNIQUEMENT par le webhook (service_role), lus par les membres.
create table public.payments (
  id uuid primary key default gen_random_uuid(),
  studio_id uuid not null references public.studios (id) on delete cascade,
  invoice_id uuid,
  provider text not null check (provider in ('stripe')),
  provider_payment_id text not null,
  amount_minor bigint not null check (amount_minor >= 0),
  currency char(3) not null check (currency ~ '^[A-Z]{3}$'),
  status public.payment_status not null,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique (provider, provider_payment_id),
  foreign key (invoice_id, studio_id) references public.invoices (id, studio_id) on delete set null (invoice_id)
);
create index payments_studio_idx on public.payments (studio_id);

-- Idempotence des webhooks Stripe — service_role uniquement (aucune policy).
create table public.stripe_events (
  id text primary key,
  type text not null,
  received_at timestamptz not null default now()
);

-- ─── Marketplace ────────────────────────────────────────────────────
create table public.marketplace_listings (
  id uuid primary key default gen_random_uuid(),
  studio_id uuid not null references public.studios (id) on delete cascade,
  design_id uuid not null,
  title text not null check (char_length(title) between 1 and 160),
  description text check (char_length(description) <= 5000),
  price_minor bigint not null check (price_minor >= 0),
  currency char(3) not null check (currency ~ '^[A-Z]{3}$'),
  status public.listing_status not null default 'draft',
  published_at timestamptz,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  foreign key (design_id, studio_id) references public.designs (id, studio_id) on delete cascade
);
create index listings_published_idx on public.marketplace_listings (status, published_at desc);

-- ─── Triggers updated_at ────────────────────────────────────────────
do $$
declare t text;
begin
  foreach t in array array['profiles','studios','clients','designs','try_on_sessions','invoices','payments','marketplace_listings']
  loop
    execute format(
      'create trigger %I_updated_at before update on public.%I for each row execute function private.set_updated_at()',
      t, t
    );
  end loop;
end $$;

-- ════════════════════════════════════════════════════════════════════
-- ROW LEVEL SECURITY
-- ════════════════════════════════════════════════════════════════════
alter table public.profiles enable row level security;
alter table public.studios enable row level security;
alter table public.studio_members enable row level security;
alter table public.clients enable row level security;
alter table public.designs enable row level security;
alter table public.try_on_sessions enable row level security;
alter table public.invoices enable row level security;
alter table public.invoice_items enable row level security;
alter table public.payments enable row level security;
alter table public.stripe_events enable row level security;
alter table public.marketplace_listings enable row level security;

-- Le rôle anonyme n'a besoin que de la vitrine marketplace.
revoke all on all tables in schema public from anon;
grant select on public.marketplace_listings to anon;
-- Tables en écriture serveur uniquement.
revoke insert, update, delete on public.payments from authenticated;
revoke all on public.stripe_events from authenticated;

-- profiles : soi-même + coéquipiers (lecture), soi-même (écriture).
create policy "profiles: read self and teammates" on public.profiles
  for select to authenticated
  using (
    id = (select auth.uid())
    or exists (
      select 1 from public.studio_members m
      where m.user_id = profiles.id and private.is_member(m.studio_id)
    )
  );
create policy "profiles: update self" on public.profiles
  for update to authenticated
  using (id = (select auth.uid()))
  with check (id = (select auth.uid()));

-- studios
create policy "studios: members read" on public.studios
  for select to authenticated using (private.is_member(id));
create policy "studios: authenticated create own" on public.studios
  for insert to authenticated with check (created_by = (select auth.uid()));
create policy "studios: admins update" on public.studios
  for update to authenticated
  using (private.has_role(id, array['owner','admin']::public.studio_role[]))
  with check (private.has_role(id, array['owner','admin']::public.studio_role[]));
create policy "studios: owner delete" on public.studios
  for delete to authenticated using (private.has_role(id, array['owner']::public.studio_role[]));

-- studio_members : lecture par les membres ; gestion par owner/admin.
-- Seul un owner peut créer/promouvoir un owner.
create policy "members: members read" on public.studio_members
  for select to authenticated using (private.is_member(studio_id));
create policy "members: admins add" on public.studio_members
  for insert to authenticated
  with check (
    private.has_role(studio_id, array['owner','admin']::public.studio_role[])
    and (role <> 'owner' or private.has_role(studio_id, array['owner']::public.studio_role[]))
  );
create policy "members: admins update" on public.studio_members
  for update to authenticated
  using (private.has_role(studio_id, array['owner','admin']::public.studio_role[]))
  with check (
    private.has_role(studio_id, array['owner','admin']::public.studio_role[])
    and (role <> 'owner' or private.has_role(studio_id, array['owner']::public.studio_role[]))
  );
create policy "members: admins remove or self leave" on public.studio_members
  for delete to authenticated
  using (
    user_id = (select auth.uid())
    or private.has_role(studio_id, array['owner','admin']::public.studio_role[])
  );

-- Tables métier : CRUD réservé aux membres du studio ; suppression aux admins.
do $$
declare t text;
begin
  foreach t in array array['clients','designs','try_on_sessions','invoices','invoice_items']
  loop
    execute format('create policy "%1$s: members read" on public.%1$I for select to authenticated using (private.is_member(studio_id))', t);
    execute format('create policy "%1$s: members insert" on public.%1$I for insert to authenticated with check (private.is_member(studio_id))', t);
    execute format('create policy "%1$s: members update" on public.%1$I for update to authenticated using (private.is_member(studio_id)) with check (private.is_member(studio_id))', t);
    execute format($p$create policy "%1$s: admins delete" on public.%1$I for delete to authenticated using (private.has_role(studio_id, array['owner','admin']::public.studio_role[]))$p$, t);
  end loop;
end $$;

-- payments : lecture seule pour les membres (écriture via webhook service_role).
create policy "payments: members read" on public.payments
  for select to authenticated using (private.is_member(studio_id));

-- stripe_events : AUCUNE policy volontairement (service_role uniquement).

-- marketplace : vitrine publique pour les annonces publiées ; gestion par les membres.
create policy "listings: public read published" on public.marketplace_listings
  for select to anon, authenticated using (status = 'published');
create policy "listings: members read all" on public.marketplace_listings
  for select to authenticated using (private.is_member(studio_id));
create policy "listings: members insert" on public.marketplace_listings
  for insert to authenticated with check (private.is_member(studio_id));
create policy "listings: members update" on public.marketplace_listings
  for update to authenticated
  using (private.is_member(studio_id)) with check (private.is_member(studio_id));
create policy "listings: admins delete" on public.marketplace_listings
  for delete to authenticated
  using (private.has_role(studio_id, array['owner','admin']::public.studio_role[]));

-- ════════════════════════════════════════════════════════════════════
-- STORAGE — bucket privé ; chemin obligatoire : <studio_id>/<fichier>
-- ════════════════════════════════════════════════════════════════════
-- Extrait le studio_id du chemin ; NULL (donc refus) si ce n'est pas un UUID.
create or replace function private.path_studio(p_name text)
returns uuid
language sql
immutable
set search_path = ''
as $$
  select case
    when split_part(p_name, '/', 1) ~* '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
    then split_part(p_name, '/', 1)::uuid
  end;
$$;
grant execute on function private.path_studio(text) to authenticated;

insert into storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
values ('studio-media', 'studio-media', false, 10485760, array['image/png','image/jpeg','image/webp'])
on conflict (id) do nothing;

create policy "studio-media: members read" on storage.objects
  for select to authenticated
  using (bucket_id = 'studio-media' and private.is_member(private.path_studio(name)));
create policy "studio-media: members upload" on storage.objects
  for insert to authenticated
  with check (bucket_id = 'studio-media' and private.is_member(private.path_studio(name)));
create policy "studio-media: members update" on storage.objects
  for update to authenticated
  using (bucket_id = 'studio-media' and private.is_member(private.path_studio(name)))
  with check (bucket_id = 'studio-media' and private.is_member(private.path_studio(name)));
create policy "studio-media: admins delete" on storage.objects
  for delete to authenticated
  using (
    bucket_id = 'studio-media'
    and private.has_role(private.path_studio(name), array['owner','admin']::public.studio_role[])
  );
