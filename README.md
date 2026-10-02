# StyliZ — iziFashion Studio

SaaS de mode assistée par IA : création de modèles, essayage virtuel, gestion clients,
facturation multi-devises et marketplace.

**Stack :** Next.js 16 (App Router, React 19) · Supabase (Auth, Postgres + RLS, Storage) ·
Tailwind CSS v4 + shadcn/ui · Zod · Stripe · Vercel.

> Next.js 16 plutôt que 14 : la dernière version 14.x n'est plus maintenue et cumule des
> failles critiques non corrigées (dont une RCE). `npm audit` est propre sur 16.

## Démarrage local

```bash
npm install
cp .env.example .env.local   # puis renseignez les valeurs
npm run dev                  # http://localhost:3000
```

| Script | Rôle |
| --- | --- |
| `npm run dev` | serveur de développement |
| `npm run build` / `npm start` | build + serveur de production |
| `npm run lint` / `npm run typecheck` | ESLint / TypeScript strict |

### Supabase en local (recommandé pour développer)

Nécessite Docker. La configuration est versionnée dans `supabase/config.toml`.

```bash
npx supabase start          # applique automatiquement supabase/migrations
npx supabase status         # affiche l'URL API et les clés locales à copier dans .env.local
```

En local, la confirmation d'e-mail est désactivée : l'inscription connecte directement.

### Base de données Supabase (production)

1. Créez un projet sur [supabase.com](https://supabase.com) et copiez URL + clés dans `.env.local`.
2. Appliquez la migration `supabase/migrations/*.sql` :
   - via la CLI : `supabase link --project-ref <ref>` puis `supabase db push` ;
   - ou en collant le fichier dans **SQL Editor**.
3. **Authentication → Providers → Email** : longueur minimale 8 et exigence « letters and digits »
   (même règle que la validation Zod, appliquée aussi par Supabase côté serveur) ; activez la
   protection contre les mots de passe compromis si votre plan le permet.
4. **Authentication → URL Configuration** : `Site URL` = votre URL, et ajoutez
   `http://localhost:3000/**` et `https://<votre-domaine>/**` aux *Redirect URLs*.
5. **Authentication → Email Templates** : pour « Confirm signup » et « Reset password », utilisez
   le lien `{{ .SiteURL }}/auth/confirm?token_hash={{ .TokenHash }}&type={{ .Type }}&next={{ .RedirectTo }}`
   (ou laissez le modèle par défaut : `/auth/callback` gère aussi le flux PKCE).

Tests RLS (Postgres ≥ 15 local) : `PGHOST=localhost PGUSER=postgres supabase/tests/run.sh`.

### Stripe

1. Clés API dans `.env.local` (`STRIPE_SECRET_KEY`).
2. Webhook → `https://<domaine>/api/webhooks/stripe`, événements
   `payment_intent.succeeded` et `payment_intent.payment_failed` ; copiez le secret `whsec_…`.
3. En local : `stripe listen --forward-to localhost:3000/api/webhooks/stripe`.
4. En créant un PaymentIntent côté serveur, renseignez `metadata.studio_id` (et `invoice_id`).

## Modules disponibles

| Module | État |
| --- | --- |
| Authentification (inscription, connexion, mot de passe oublié) | ✅ |
| Clients : fiches, coordonnées, mesures, recherche | ✅ |
| Factures multi-devises : lignes, TVA, numérotation `F-AAAA-0001`, statuts, impression/PDF | ✅ |
| Paiement Stripe (webhook → facture payée) | ✅ côté serveur |
| Modèles IA, essayage virtuel, marketplace | schéma prêt, interface à venir |

Les montants sont stockés en unités mineures (centimes ; XOF/XAF sans décimales) et
**recalculés en base** à chaque écriture : un client de l'API ne peut pas falsifier un total.
Une facture émise ne peut plus être modifiée (seulement payée ou annulée).

## Sécurité — ce qui est en place

- **Secrets** : seuls les `NEXT_PUBLIC_*` atteignent le navigateur. `lib/env/server.ts` et
  `lib/supabase/admin.ts` importent `server-only` (build cassé si importés côté client) ;
  `next.config.ts` refuse de builder si une variable `NEXT_PUBLIC_*` ressemble à un secret.
  Tous les `.env*` sauf `.env.example` sont ignorés par Git.
- **Auth** : `src/proxy.ts` rafraîchit la session (`getClaims()`, signature JWT vérifiée) et
  protège `/dashboard` ; chaque page protégée revérifie via `requireUser()` (défense en profondeur).
  Messages d'erreur génériques (pas d'énumération de comptes), redirections `?next=` limitées
  aux chemins relatifs (pas d'open redirect).
- **RLS** sur toutes les tables ; accès limité aux membres du studio, suppression réservée aux
  admins, FKs composites empêchant les liens inter-studios ; `payments` / `stripe_events`
  écrits uniquement par le webhook (service_role) ; Storage privé cloisonné par `<studio_id>/`.
- **Webhook Stripe** : signature HMAC vérifiée sur le corps brut, tolérance 5 min (anti-rejeu),
  taille limitée, métadonnées validées par Zod, idempotence par `event.id`.
- **Entrées** : toutes les Server Actions valident avec Zod (`src/lib/validations`).
- **En-têtes HTTP** : CSP, HSTS, `X-Frame-Options: DENY`, `nosniff`, `Referrer-Policy`,
  `Permissions-Policy`.

## Déploiement Vercel

1. [vercel.com/new](https://vercel.com/new) → importez `sob-busy/creation-animer`
   (framework détecté : Next.js, aucun réglage de build à modifier).
2. **Settings → Environment Variables** : ajoutez toutes les variables de `.env.example`
   (Production + Preview). `NEXT_PUBLIC_SITE_URL` = URL de production.
3. Chaque push sur `main` déploie en production ; chaque branche/PR obtient une preview.
4. Ajoutez l'URL Vercel aux *Redirect URLs* Supabase et au webhook Stripe.

## Structure

```
src/
  app/
    (auth)/          login, signup, forgot/reset password + Server Actions
    (dashboard)/     espace protégé (layout + /dashboard)
    api/webhooks/    webhook Stripe signé
    auth/            confirm (token_hash) & callback (PKCE)
  components/        ui/ (shadcn), forms/, dashboard/, brand/
  lib/               env/, supabase/, validations/, auth.ts, stripe.ts
  proxy.ts           garde d'authentification (ex-middleware)
supabase/
  migrations/        schéma + RLS
  tests/             tests RLS
legacy/              ancien prototype PHP (archivé, non déployé)
```
