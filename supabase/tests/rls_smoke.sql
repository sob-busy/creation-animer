-- RLS smoke tests: run after supabase_stub.sql + migrations on a throwaway database.
-- Every 'OK denied' line must appear and the 'expect N' counts must match.
\set ON_ERROR_STOP 1
-- Inscription de 2 utilisateurs (trigger => profil + studio + owner)
insert into auth.users (id, email, raw_user_meta_data) values
 ('aaaaaaaa-0000-0000-0000-000000000001','a@x.com','{"full_name":"Awa"}'),
 ('bbbbbbbb-0000-0000-0000-000000000002','b@x.com','{"full_name":"Bintou"}');
select s.name, m.role from studios s join studio_members m on m.studio_id=s.id order by 1;
create temp table ids as select (select studio_id from studio_members where user_id='aaaaaaaa-0000-0000-0000-000000000001') a, (select studio_id from studio_members where user_id='bbbbbbbb-0000-0000-0000-000000000002') b;
grant select on ids to authenticated, anon;
insert into designs (id, studio_id, title) select 'dddddddd-0000-0000-0000-000000000001', a, 'Robe A' from ids;
insert into marketplace_listings (studio_id, design_id, title, price_minor, currency, status) select a, 'dddddddd-0000-0000-0000-000000000001', 'Pub', 1000, 'XOF', 'published' from ids;
insert into marketplace_listings (studio_id, design_id, title, price_minor, currency) select a, 'dddddddd-0000-0000-0000-000000000001', 'Draft', 1000, 'XOF' from ids;

create or replace function pg_temp.expect_fail(q text, label text) returns void language plpgsql as $$
begin execute q; raise exception 'FAIL (should have been denied): %', label;
exception when insufficient_privilege or check_violation or foreign_key_violation or others then
  if sqlerrm like 'FAIL%' then raise; end if; raise notice 'OK denied: % (%)', label, sqlerrm; end $$;

-- ── User A
set role authenticated; select set_config('request.jwt.claim.sub','aaaaaaaa-0000-0000-0000-000000000001',false);
insert into clients (studio_id, full_name) select a, 'Cliente A' from ids;
select 'A sees own clients' t, count(*) from clients;
select pg_temp.expect_fail($q$insert into clients (studio_id, full_name) select b, 'intrus' from ids$q$, 'A insert into studio B');
select pg_temp.expect_fail($q$insert into payments (studio_id, provider, provider_payment_id, amount_minor, currency, status) select a,'stripe','pi_1',1,'XOF','succeeded' from ids$q$, 'A forge payment');
select pg_temp.expect_fail($q$select * from stripe_events$q$, 'A read stripe_events');
select 'A storage own' t, count(*) from (select 1) x where private.path_studio((select a::text from ids)||'/x.png') is not null;
insert into storage.objects (bucket_id, name) select 'studio-media', a::text||'/robe.png' from ids;
select pg_temp.expect_fail($q$insert into storage.objects (bucket_id, name) select 'studio-media', b::text||'/hack.png' from ids$q$, 'A upload into B folder');
select pg_temp.expect_fail($q$insert into storage.objects (bucket_id, name) values ('studio-media', 'not-a-uuid/hack.png')$q$, 'A upload bad path');
reset role;

-- ── User B
set role authenticated; select set_config('request.jwt.claim.sub','bbbbbbbb-0000-0000-0000-000000000002',false);
select 'B sees clients (expect 0)' t, count(*) from clients;
select 'B sees designs (expect 0)' t, count(*) from designs;
select 'B sees listings (expect 1 published)' t, count(*) from marketplace_listings;
select 'B sees A storage (expect 0)' t, count(*) from storage.objects;
select 'B sees studios (expect 1)' t, count(*) from studios;
update clients set full_name='pwned';
select 'B update A clients affected rows check' t, count(*) from clients where full_name='pwned';
select pg_temp.expect_fail($q$insert into studio_members (studio_id, user_id, role) select a, 'bbbbbbbb-0000-0000-0000-000000000002', 'owner' from ids$q$, 'B joins studio A as owner');
-- cross-studio FK: B links its try-on to A's design
select pg_temp.expect_fail($q$insert into try_on_sessions (studio_id, design_id) select b, 'dddddddd-0000-0000-0000-000000000001' from ids$q$, 'B try-on on A design');
reset role;

-- ── Anon
set role anon; select set_config('request.jwt.claim.sub','',false);
select 'anon listings (expect 1)' t, count(*) from marketplace_listings;
select pg_temp.expect_fail($q$select * from clients$q$, 'anon read clients');
select pg_temp.expect_fail($q$select * from profiles$q$, 'anon read profiles');
reset role;

-- ── Member (non-admin) privileges
insert into studio_members (studio_id, user_id, role) select a, 'bbbbbbbb-0000-0000-0000-000000000002', 'member' from ids;
set role authenticated; select set_config('request.jwt.claim.sub','bbbbbbbb-0000-0000-0000-000000000002',false);
select 'B as member sees A clients (expect 1)' t, count(*) from clients;
delete from clients; 
select 'member delete blocked (expect 1 left)' t, count(*) from clients;
update studio_members set role='owner' where user_id='bbbbbbbb-0000-0000-0000-000000000002' and studio_id=(select a from ids);
select 'role after promote attempt' t, role from studio_members where user_id='bbbbbbbb-0000-0000-0000-000000000002' and studio_id=(select a from ids);
reset role;
