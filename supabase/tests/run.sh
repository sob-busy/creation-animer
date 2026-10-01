#!/usr/bin/env bash
# Runs the RLS smoke tests against a throwaway database on any Postgres >= 15.
# Connection comes from the standard libpq variables (PGHOST, PGPORT, PGUSER, PGPASSWORD).
#   PGHOST=localhost PGUSER=postgres supabase/tests/run.sh
set -euo pipefail
cd "$(dirname "$0")/../.."
DB=stylize_rls_test
psql -d postgres -q -c "drop database if exists $DB" -c "create database $DB"
psql -d "$DB" -q -v ON_ERROR_STOP=1 -f supabase/tests/supabase_stub.sql
for f in supabase/migrations/*.sql; do psql -d "$DB" -q -v ON_ERROR_STOP=1 -f "$f"; done
psql -d "$DB" -q -At -v ON_ERROR_STOP=1 -f supabase/tests/rls_smoke.sql
psql -d postgres -q -c "drop database $DB"
