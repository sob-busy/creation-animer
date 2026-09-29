# Mercerie Incha Allahou — site vitrine

Site vitrine de la mercerie **Mercerie Incha Allahou** (Lomé, Togo) : pagnes wax, bazin, kaki,
fils, boutons, fermetures et outils de couture. Les clients composent une sélection
et l'envoient directement sur WhatsApp (+228 92 88 91 12).

Site 100 % statique (HTML/CSS/JS, sans framework) : très léger, rapide même en 3G.

## Tester en local

- **Le plus simple** : double-cliquez sur `index.html`.
- **Ou avec un petit serveur** (recommandé) :
  ```bash
  npx http-server -p 8080 .
  # puis ouvrir http://localhost:8080
  ```

## Modifier le contenu

Tout se trouve dans **`assets/js/donnees.js`** :

- numéro WhatsApp, adresse, horaires, moyens de paiement, livraison ;
- liste des produits : nom, unité, description, badge, image (pas de prix : ils se discutent sur WhatsApp).

## Mettre vos vraies photos

1. Déposez la photo dans `assets/produits/` (ex. `pagne-wax-cercles.jpg`, format carré conseillé, ~800×800 px).
2. Dans `assets/js/donnees.js`, remplacez `image: "assets/produits/pagne-wax-cercles.svg"` par le nom de votre photo.

Les visuels actuels sont des illustrations vectorielles générées par `outils/generer-visuels.mjs`.

## Structure

```
index.html              page unique
assets/css/style.css    design
assets/js/donnees.js    contenu (produits, coordonnées)
assets/js/app.js        boutique, sélection, messagerie WhatsApp
assets/produits/        visuels des produits
```

## Déploiement

Hébergement statique (Vercel, Netlify, GitHub Pages…) : publier le dossier racine tel quel.
