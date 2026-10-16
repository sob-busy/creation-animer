---
format: 1080x1920
duration: 55s
message: "Chez Madame Sibabi, des jus naturels bien glacés et une salade délicieuse : appelez le 93 17 05 34 ou venez au quartier Tchitchao."
arc: Hook (numéro) → Marque → Produits un par un (4 jus + salade) → Promesse → Appel à l'action
audience: habitants du quartier Tchitchao et alentours, clients sur TikTok / WhatsApp / Facebook
mode: autonomous
music: none
---

## Video direction

- **Palette (couleurs de l'affiche) :** vert feuille `#1F7A34` (fond de marque, bandeaux), jaune soleil `#FFD21F` (logo SIBABI, accents), rouge `#D7192F` (numéro de téléphone, CTA), crème `#FFF8EC` (cartes), brun `#2A160C` (contours du logo, texte). Chaque jus a son propre univers coloré : citron = vert-jaune acidulé, bissap = rubis profond, ananas = or chaud, tamarin = ambre/caramel.
- **Typo :** Lilita One (titres, noms des jus, chiffres, « SIBABI »), Kaushan Script (« Madame », touches manuscrites), Poppins 400/600/800 (qualités, infos). Le logo « Madame SIBABI » est recréé en vectoriel comme sur l'affiche : « Madame » blanc manuscrit, « SIBABI » jaune en dégradé avec gros contour brun, couronne dorée.
- **Effets spéciaux :** éclat de lumière radial, rayons tournants (finis), glaçons et tranches de fruits qui flottent en profondeur, bulles qui montent dans les verres, reflets brillants qui balaient le logo et les verres, éclaboussures/étincelles au moment des révélations. Tout est déterministe et fini (pas de boucle infinie).
- **Grammaire de mouvement :** arrivées en courbe longue `power3`/`expo.out`, un pop discret (`back.out` léger) seulement pour les badges et le numéro ; chaque nom de jus et chaque qualité apparaît **au moment où la voix le dit** ; les héros (verre, photo, logo) lévitent doucement une fois posés.
- **Rythme :** ouverture rapide et spectaculaire (numéro + logo) → 5 plans produits de même construction (nom en haut, verre au centre, qualités en pastilles, vraie photo du produit en carte) enchaînés en `push-slide LEFT` → plan humain (photo de Madame Sibabi) plus calme → fin dense et claire (adresse + numéro) tenue jusqu'au bout.
- **Mise en page 9:16 :** contenu important dans le haut 83 % (bande sous-titres libre) ; héros vers y ≈ 0,42 × hauteur.
- **Liste négative :** ne jamais inventer de prix, d'horaires ni de promesse santé ; pas de logo d'une autre marque ; pas d'effet glitch/néon hors sujet ; pas de tout-qui-flotte au premier plan.

## Frame 1 — Le numéro qui flotte

- scene: Fond vert profond, rayons de lumière ; les chiffres 93 17 05 34 tombent et flottent un à un avec un éclat ; icône téléphone qui sonne ; flash et étincelles quand la voix dit « Madame Sibabi »
- voiceover: "93 17 05 34 : retenez bien ce numéro… c'est celui de Madame Sibabi !"
- duration: 6.614s
- transition_in: cut
- status: animated
- src: compositions/frames/01-numero.html
- type: hook
- persuasion: Numéro mémorisable + curiosité
- beat: Surprise + intérêt
- blueprint: compose
- asset_candidates:

narrativeRole: Accroche : le numéro à retenir dès la première seconde, rattaché au nom.
keyMessage: 93 17 05 34, c'est Madame Sibabi.

Scene 1 (début → « numéro ») : rayons de lumière jaunes tournent lentement derrière ; glaçons et tranches de citron flottent en profondeur ; les quatre groupes de chiffres « 93 · 17 · 05 · 34 » tombent du haut un par un en Lilita One blanc sur pastille rouge, chacun avec un petit éclat d'étincelles, puis flottent ; une icône de téléphone vibre à gauche du numéro.
Scene 2 (« retenez bien ») : le numéro se rassemble en une grande pastille rouge brillante (reflet qui balaie), qui lévite.
Scene 3 (« Madame Sibabi ») : flash blanc radial + couronne d'étincelles dorées ; le logo « Madame SIBABI » apparaît sous le numéro en pop, reflet brillant.

## Frame 2 — La marque

- scene: Logo Madame SIBABI en grand avec couronne ; photo ronde de Madame Sibabi ; bandeau « Jus naturels & salade délicieuse » ; badge glacé
- voiceover: "Chez Madame Sibabi, on vend des jus naturels et une salade délicieuse… le tout, bien glacé."
- duration: 6.314s
- transition_in: zoom-through
- status: animated
- src: compositions/frames/02-marque.html
- type: product_intro
- persuasion: Présentation de marque + promesse
- beat: Clarté + envie
- blueprint: compose
- asset_candidates: assets/portrait-sibabi-2.png — Madame Sibabi souriante, foulard et tenue colorés

narrativeRole: Présente la marque et ce qu'elle vend.
keyMessage: Madame Sibabi = jus naturels + salade délicieuse, bien glacés.

Scene 1 (« Chez Madame Sibabi ») : logo en haut (≈ 900 px de large), couronne qui se pose ; photo de Madame Sibabi en médaillon rond cerclé de jaune et de vert, entrée en zoom doux.
Scene 2 (« jus naturels ») : bandeau en bois/vert « Jus naturels » glisse sous le médaillon ; quatre mini-verres colorés (citron, bissap, ananas, tamarin) sautent en ligne.
Scene 3 (« salade délicieuse ») : pastille jaune « + Salade délicieuse ♥ » pop à côté.
Scene 4 (« bien glacé ») : badge rouge « Tout bien glacé ! » avec glaçons qui tombent et givre ; tenue.

## Frame 3 — Jus de citron

- scene: Univers vert-jaune ; un grand verre se remplit de jus de citron, glaçons, paille ; tranches de citron qui flottent ; qualités en pastilles ; vraie photo en carte
- voiceover: "Le jus de citron : frais, acidulé, plein de vitamine C. Parfait pour se réveiller."
- duration: 5.787s
- transition_in: push-slide LEFT
- status: animated
- src: compositions/frames/03-citron.html
- type: feature_showcase
- persuasion: Produit isolé + qualités
- beat: Fraîcheur
- blueprint: compose
- asset_candidates: assets/photo-citron.png — gobelet de jus de citron glacé, citrons et menthe

narrativeRole: Présente le jus de citron et ses qualités.
keyMessage: Jus de citron : frais, acidulé, vitamine C.

Scene 1 (« Le jus de citron ») : compteur « 1/4 » ; titre « Jus de » (Kaushan) + « CITRON » (Lilita, très grand) entrent par la gauche ; le verre vide se pose au centre et le jus monte, glaçons qui tombent, bulles.
Scene 2 (« frais », « acidulé », « vitamine C ») : trois pastilles blanches à coche verte arrivent l'une après l'autre sur le côté, chacune sur son mot.
Scene 3 (« se réveiller ») : la vraie photo du jus apparaît en carte inclinée « Photo réelle » ; tranches de citron flottent ; tenue.

## Frame 4 — Jus de bissap

- scene: Univers rubis ; verre de bissap ; fleurs d'hibiscus qui flottent ; qualités ; vraie photo
- voiceover: "Le jus de bissap, fait avec la fleur d'hibiscus : une belle couleur rubis et un goût doux qui désaltère."
- duration: 5.918s
- transition_in: push-slide LEFT
- status: animated
- src: compositions/frames/04-bissap.html
- type: feature_showcase
- persuasion: Produit isolé + origine (hibiscus)
- beat: Envie
- blueprint: compose
- asset_candidates: assets/photo-bissap.png — gobelet de jus de bissap rouge rubis, fleurs d'hibiscus

narrativeRole: Présente le bissap, son origine et son goût.
keyMessage: Bissap : fleur d'hibiscus, couleur rubis, goût doux.

Scene 1 (« Le jus de bissap ») : « 2/4 », titre « Jus de BISSAP » ; verre qui se remplit de rouge rubis.
Scene 2 (« fleur d'hibiscus ») : fleurs d'hibiscus dessinées éclosent autour du verre ; pastille « À la fleur d'hibiscus ».
Scene 3 (« couleur rubis », « goût doux ») : pastilles « Couleur rubis », « Goût doux » ; vraie photo en carte ; tenue.

## Frame 5 — Jus d'ananas

- scene: Univers doré ; verre d'ananas ; morceaux d'ananas flottants ; qualités ; vraie photo
- voiceover: "Le jus d'ananas : doré, fruité, plein de soleil. Un vrai plaisir à chaque gorgée."
- duration: 5.845s
- transition_in: push-slide LEFT
- status: animated
- src: compositions/frames/05-ananas.html
- type: feature_showcase
- persuasion: Produit isolé + sensations
- beat: Plaisir
- blueprint: compose
- asset_candidates: assets/photo-ananas.png — gobelet de jus d'ananas doré, ananas coupé

narrativeRole: Présente le jus d'ananas.
keyMessage: Ananas : doré, fruité, plein de soleil.

Scene 1 (« Le jus d'ananas ») : « 3/4 », titre « Jus d'ANANAS » ; verre doré qui se remplit, soleil rayonnant derrière.
Scene 2 (« doré », « fruité », « soleil ») : trois pastilles une par une.
Scene 3 (« plaisir ») : vraie photo en carte ; morceaux d'ananas flottent ; tenue.

## Frame 6 — Jus de tamarin

- scene: Univers ambre ; verre de tamarin ; gousses de tamarin flottantes ; qualités ; vraie photo
- voiceover: "Le jus de tamarin : acidulé et parfumé, le goût de chez nous, qui rafraîchit vraiment."
- duration: 5.438s
- transition_in: push-slide LEFT
- status: animated
- src: compositions/frames/06-tamarin.html
- type: feature_showcase
- persuasion: Produit isolé + ancrage local
- beat: Fierté + fraîcheur
- blueprint: compose
- asset_candidates: assets/photo-tamarin.png — gobelet de jus de tamarin ambré, gousses de tamarin

narrativeRole: Présente le tamarin, goût local.
keyMessage: Tamarin : acidulé, parfumé, le goût de chez nous.

Scene 1 (« Le jus de tamarin ») : « 4/4 », titre « Jus de TAMARIN » ; verre ambré qui se remplit.
Scene 2 (« acidulé », « parfumé », « de chez nous ») : trois pastilles une par une.
Scene 3 (« rafraîchit ») : vraie photo ; givre/glaçons ; tenue.

## Frame 7 — La salade délicieuse

- scene: Univers vert frais ; grande photo ronde de la salade ; légumes stylisés qui flottent ; qualités
- voiceover: "Et pour accompagner, la salade délicieuse : fraîche, croquante et colorée."
- duration: 4.972s
- transition_in: push-slide LEFT
- status: animated
- src: compositions/frames/07-salade.html
- type: feature_showcase
- persuasion: Produit complémentaire
- beat: Gourmandise
- blueprint: compose
- asset_candidates: assets/photo-salade.png — saladier coloré : tomates, maïs, œuf, carottes, laitue

narrativeRole: Ajoute la salade à l'offre.
keyMessage: Salade délicieuse : fraîche, croquante, colorée.

Scene 1 (« pour accompagner ») : titre « Salade » (Lilita) + « délicieuse ♥ » (Kaushan) ; la photo de la salade entre en médaillon rond qui tourne légèrement.
Scene 2 (« fraîche », « croquante », « colorée ») : trois pastilles ; rondelles de tomate, concombre et feuilles stylisées flottent ; tenue.

## Frame 8 — La promesse

- scene: Photo de Madame Sibabi en grand ; liste de promesses cochées ; ruban « Votre satisfaction, notre priorité ♥ »
- voiceover: "Fraîcheur, goût naturel, et votre satisfaction : c'est la priorité de Madame Sibabi."
- duration: 5.815s
- transition_in: blur-crossfade
- status: animated
- src: compositions/frames/08-promesse.html
- type: benefit_highlight
- persuasion: Visage humain + engagement
- beat: Confiance
- blueprint: compose
- asset_candidates: assets/portrait-sibabi-2.png — Madame Sibabi souriante

narrativeRole: Met un visage sur la marque et donne la promesse de qualité.
keyMessage: Fraîcheur, goût naturel, satisfaction garantie.

Scene 1 : la photo de Madame Sibabi entre en grand cadre arrondi (bord jaune) avec léger zoom.
Scene 2 (« Fraîcheur », « goût naturel », « satisfaction ») : trois lignes cochées apparaissent une par une sur une carte crème.
Scene 3 (« priorité ») : ruban rouge « Votre satisfaction, notre priorité ♥ » se déroule ; cœur qui bat une fois ; tenue.

## Frame 9 — Venez chez Madame Sibabi

- scene: Fond vert de marque ; logo ; épingle de localisation « Quartier Tchitchao » ; gros bouton rouge 93 17 05 34 qui pulse ; « Venez goûter ! » ; étal en photo
- voiceover: "Venez au quartier Tchitchao, ou appelez le 93 17 05 34. Venez goûter : vous serez toujours satisfait !"
- duration: 8.312s
- transition_in: zoom-through
- status: animated
- src: compositions/frames/09-cta.html
- type: cta
- persuasion: Appel à l'action double (lieu + téléphone)
- beat: Décision
- blueprint: compose
- asset_candidates: assets/etal-jus-salade.png — l'étal : bocaux, gobelets, glaçons, fruits, salade

narrativeRole: Dit exactement où venir et qui appeler.
keyMessage: Quartier Tchitchao — 93 17 05 34.

Scene 1 (« quartier Tchitchao ») : photo de l'étal en bandeau arrondi en haut ; épingle rouge qui tombe et rebondit doucement, « Quartier TCHITCHAO » en Lilita jaune.
Scene 2 (« appelez le 93 17 05 34 ») : gros bouton rouge avec icône téléphone et le numéro, ondes qui pulsent.
Scene 3 (« Venez goûter ») : logo Madame SIBABI en bas du bloc ; bandeau jaune « Venez goûter, vous serez toujours satisfait ! » ; étincelles ; tenue jusqu'à la fin, fondu final.
