# Création d'Animer — site vitrine

Site statique (HTML/CSS/JS, sans dépendance ni build). Ouvrez `index.html` ou déployez le dossier tel quel (Netlify, Vercel, GitHub Pages, hébergement mutualisé).

## À personnaliser

| Quoi | Où |
|---|---|
| **Logo officiel** | Déposez-le sous `assets/img/logo.png` (fond transparent, carré de préférence). Il remplace automatiquement le logo provisoire `logo.svg` dans l'en-tête, l'intro et le pied de page. |
| Numéro WhatsApp | `index.html` (liens `wa.me/22892355735`) et `WHATSAPP_NUMBER` dans `assets/js/main.js` |
| Chiffres clés | Section « Le studio » dans `index.html` (attributs `data-count`) |
| Réalisations | Section « Réalisations » : remplacez chaque `<div class="card__visual v-…">` par `<img class="card__visual" src="assets/img/…" alt="…">` |
| Avis clients | Section « Avis clients » : remplacez les textes d'exemple par de vrais témoignages |
| Couleurs | Variables en haut de `assets/css/style.css` (`--accent`, `--ink`, `--paper`…) |

## Fonctionnalités

- Intro animée, titre révélé mot à mot, formes en parallaxe, bandeau défilant
- Menu mobile plein écran, en-tête qui se masque au défilement, barre de progression
- Services interactifs, filtres des réalisations, frise de méthode animée
- Carrousel d'avis, FAQ en accordéon
- Formulaire de contact qui ouvre WhatsApp avec le message prérédigé + bouton WhatsApp flottant
- Curseur personnalisé et boutons magnétiques (souris uniquement)
- Accessibilité : navigation clavier, `prefers-reduced-motion` respecté, contenu visible sans JavaScript
- SEO : balises meta, Open Graph, données structurées `LocalBusiness`

L'ancien prototype PHP reste disponible dans `creation_animer_project.zip`.
