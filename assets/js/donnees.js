/* =====================================================================
   MERCERIE INCH'ALLAH — données du site
   C'est le SEUL fichier à modifier pour changer les produits,
   les horaires ou le numéro WhatsApp.
   ===================================================================== */

window.BOUTIQUE = {
  nom: "Mercerie Incha Allahou",
  ville: "Lomé, Togo",
  // Numéro au format international, chiffres uniquement (sans + ni espaces)
  whatsapp: "22891907772",
  whatsappAffiche: "+228 91 90 77 72",
  // À confirmer / compléter par la boutique
  adresse: "Lomé, Togo — quartier à préciser",
  horaires: [
    ["Lundi – Samedi", "8 h 00 – 19 h 00"],
    ["Dimanche", "Sur rendez-vous"],
  ],
  paiement: "Espèces à la boutique ou mobile money (Flooz, T-Money) — à confirmer sur WhatsApp.",
  livraison: "Livraison possible dans Lomé. Les frais dépendent du quartier et sont confirmés sur WhatsApp.",
};

window.CATEGORIES = [
  { id: "pagnes", nom: "Pagnes & wax" },
  { id: "tissus", nom: "Tissus au mètre" },
  { id: "fils", nom: "Fils" },
  { id: "mercerie", nom: "Petite mercerie" },
  { id: "outils", nom: "Outils du tailleur" },
];

/* Pas de prix affichés : les prix se discutent sur WhatsApp.
   image : remplacez par votre photo (ex. "assets/produits/pagne-wax-cercles.jpg"). */
window.PRODUITS = [
  {
    id: "pagne-wax-cercles", categorie: "pagnes",
    nom: "Pagne wax « Cercles »", unite: "le pagne de 6 yards",
    image: "assets/produits/pagne-wax-cercles.svg", badge: "Très demandé",
    description: "Wax 100 % coton aux cercles bleu nuit, ocre et rouge. Idéal pour robes, chemises et ensembles de cérémonie.",
    details: ["100 % coton", "6 yards (≈ 5,5 m)", "Largeur ≈ 1,15 m"],
  },
  {
    id: "pagne-wax-eventail", categorie: "pagnes",
    nom: "Pagne wax « Éventail »", unite: "le pagne de 6 yards",
    image: "assets/produits/pagne-wax-eventail.svg",
    description: "Motif éventail vert, orange et or. Un classique qui habille aussi bien une jupe qu'une tenue d'homme.",
    details: ["100 % coton", "6 yards (≈ 5,5 m)", "Couleurs résistantes au lavage"],
  },
  {
    id: "pagne-wax-premium", categorie: "pagnes",
    nom: "Wax premium, qualité hollandaise", unite: "le pagne de 6 yards",
    image: "assets/produits/pagne-wax-premium.svg", badge: "Premium",
    description: "Wax haut de gamme, toucher ferme et couleurs profondes, pour les grandes occasions : mariages, dots, fêtes.",
    details: ["Coton supérieur", "6 yards (≈ 5,5 m)", "Plusieurs motifs disponibles"],
  },
  {
    id: "pagne-kente", categorie: "pagnes",
    nom: "Imprimé kente", unite: "le pagne de 6 yards",
    image: "assets/produits/pagne-kente.svg",
    description: "Imprimé inspiré du kente, en jaune, vert et rouge. Parfait pour les tenues de fête et les accessoires.",
    details: ["Coton imprimé", "6 yards (≈ 5,5 m)"],
  },
  {
    id: "bazin-riche", categorie: "tissus",
    nom: "Bazin riche", unite: "le mètre",
    image: "assets/produits/bazin-riche.svg", badge: "Cérémonie",
    description: "Bazin damassé brillant, bien amidonné. Pour boubous, grands boubous et tenues de cérémonie.",
    details: ["Coton damassé", "Plusieurs couleurs", "Vendu au mètre"],
  },
  {
    id: "kaki-uniforme", categorie: "tissus",
    nom: "Kaki uniforme", unite: "le mètre",
    image: "assets/produits/kaki-uniforme.svg", badge: "Rentrée",
    description: "Kaki résistant pour tenues scolaires, uniformes et vêtements de travail. Tient bien au repassage.",
    details: ["Sergé coton / polyester", "Largeur ≈ 1,50 m", "Vendu au mètre"],
  },
  {
    id: "coton-popeline", categorie: "tissus",
    nom: "Popeline de coton unie", unite: "le mètre",
    image: "assets/produits/coton-popeline.svg",
    description: "Popeline légère et agréable, pour chemises, doublures légères et finitions.",
    details: ["100 % coton", "Plusieurs coloris", "Vendu au mètre"],
  },
  {
    id: "doublure-satinee", categorie: "tissus",
    nom: "Doublure satinée", unite: "le mètre",
    image: "assets/produits/doublure-satinee.svg",
    description: "Doublure fluide et brillante pour robes, vestes et jupes. Glisse bien sur la peau.",
    details: ["Polyester satiné", "Vendu au mètre"],
  },
  {
    id: "dentelle-brodee", categorie: "tissus",
    nom: "Galon de dentelle brodée", unite: "le mètre",
    image: "assets/produits/dentelle-brodee.svg",
    description: "Galon festonné pour border manches, encolures et bas de robe.",
    details: ["Largeur ≈ 8 cm", "Blanc et écru", "Vendu au mètre"],
  },
  {
    id: "fil-polyester", categorie: "fils",
    nom: "Fil à coudre polyester", unite: "la bobine de 500 m",
    image: "assets/produits/fil-polyester.svg",
    description: "Fil solide pour machine et main. Large choix de couleurs pour s'accorder à vos pagnes.",
    details: ["100 % polyester", "500 m", "Toutes couleurs"],
  },
  {
    id: "cone-fil", categorie: "fils",
    nom: "Cône de fil surjeteuse", unite: "le cône",
    image: "assets/produits/cone-fil.svg", badge: "Atelier",
    description: "Gros cône pour surjeteuse et production en atelier. Blanc, noir et couleurs.",
    details: ["Polyester", "≈ 5 000 yards"],
  },
  {
    id: "boutons-assortis", categorie: "mercerie",
    nom: "Boutons assortis", unite: "le sachet de 50",
    image: "assets/produits/boutons-assortis.svg",
    description: "Boutons 2 et 4 trous, plusieurs tailles et couleurs, pour chemises, vestes et robes.",
    details: ["50 pièces", "Tailles variées"],
  },
  {
    id: "fermeture-eclair", categorie: "mercerie",
    nom: "Fermeture éclair", unite: "la pièce (20 cm)",
    image: "assets/produits/fermeture-eclair.svg",
    description: "Fermetures métal et nylon pour robes, jupes et pantalons. Autres longueurs sur demande.",
    details: ["20 cm", "Plusieurs couleurs"],
  },
  {
    id: "elastique", categorie: "mercerie",
    nom: "Élastique plat 2 cm", unite: "le mètre",
    image: "assets/produits/elastique.svg",
    description: "Élastique souple et durable pour ceintures, jupes et pantalons.",
    details: ["Largeur 2 cm", "Blanc et noir"],
  },
  {
    id: "entoilage-thermocollant", categorie: "mercerie",
    nom: "Entoilage thermocollant", unite: "le mètre",
    image: "assets/produits/entoilage-thermocollant.svg",
    description: "Pour rigidifier cols, poignets et parmentures. Se colle au fer à repasser.",
    details: ["Blanc et noir", "Vendu au mètre"],
  },
  {
    id: "ciseaux-tailleur", categorie: "outils",
    nom: "Ciseaux de tailleur", unite: "la paire (25 cm)",
    image: "assets/produits/ciseaux-tailleur.svg", badge: "Indispensable",
    description: "Grands ciseaux en acier pour une coupe nette, même sur plusieurs épaisseurs de pagne.",
    details: ["Acier", "25 cm"],
  },
  {
    id: "metre-ruban", categorie: "outils",
    nom: "Mètre ruban", unite: "la pièce (150 cm)",
    image: "assets/produits/metre-ruban.svg",
    description: "Mètre souple pour la prise de mesures. Graduations nettes, embouts métalliques.",
    details: ["150 cm", "Double face"],
  },
  {
    id: "pelote-epingles", categorie: "outils",
    nom: "Pelote + épingles", unite: "le lot",
    image: "assets/produits/pelote-epingles.svg",
    description: "Pelote à épingles avec épingles à tête colorée, pour garder tout à portée de main.",
    details: ["Pelote + ≈ 50 épingles"],
  },
  {
    id: "craie-tailleur", categorie: "outils",
    nom: "Craie de tailleur", unite: "la boîte de 10",
    image: "assets/produits/craie-tailleur.svg",
    description: "Craie plate pour tracer les patrons sur le tissu. Part au lavage.",
    details: ["10 pièces", "Couleurs assorties"],
  },
];
