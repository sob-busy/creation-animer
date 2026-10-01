# Prototype PHP « Création d'Animer » (archivé)

Ancien prototype PHP/MySQL (inscription / connexion), conservé uniquement pour référence.
**Il n'est ni déployé ni maintenu** — l'application StyliZ (Next.js + Supabase) le remplace.

Problèmes connus (ne pas réutiliser tel quel) :
- identifiants de base de données codés en dur (`root` sans mot de passe) ;
- pas de session après connexion, pas de CSRF, pas de validation des entrées ;
- jeton de réinitialisation stocké en clair, sans expiration ;
- messages d'erreur internes (PDO, SMTP) renvoyés à l'utilisateur.
