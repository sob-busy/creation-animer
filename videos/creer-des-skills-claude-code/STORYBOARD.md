---
format: 1080x1920
duration: 67s
message: "Un skill, c'est un dossier avec un SKILL.md : écris tes consignes une fois, Claude Code les applique tout seul."
arc: how-to-process
audience: créateurs et développeurs qui utilisent Claude Code, débutants sur les skills
mode: autonomous
music: energetic minimal tech underscore, light pulse, modern
---

## Video direction

- **Palette (frame.md, by role):** fond `cream` partout, avec une grille hairline très légère (ink@6%) ; cartes et dossiers sur `tile` / `tile-strong` avec hairline + l'unique ombre douce ; surfaces de code (terminal, éditeur SKILL.md, barre de commande) en `navy` / `navy-soft`, texte cream, syntaxe teal `#5DB8A6` / amber `#E8A55A` ; **un seul moment coral par frame** (le mot-clé, le badge d'étape ou le CTA). Titres en EB Garamond 400 (display / display-cover), libellés en JetBrains Mono (kicker avec ✱ coral), corps en Inter.
- **Les flottants (demande explicite de l'utilisateur) :** chaque frame porte une couche d'ambiance de 4 à 6 petits objets flottants dessinés (mini-cartes de fichiers `.md`, dossiers, chevrons `/`, ✱), en tile/ink@20 %, à profondeur réduite (flou léger, opacité 35–55 %), qui dérivent lentement par tweens **finis** et **déterministes** (amplitude faible, direction dérivée de l'index), sans jamais traverser la zone de lecture. Le héros de chaque frame, une fois posé, a une **lévitation douce** (subtle jitter / `sine-wave-loop` basse amplitude, un seul cycle long fini). Pas de rebond, pas de respiration en boucle, pas d'objets qui flottent tous indépendamment au premier plan.
- **Grammaire de mouvement :** arrivées en courbe longue `power3` / `expo.out` (lisse, jamais de bounce) ; chaque élément apparaît **quand la voix le nomme** (mots horodatés dans `audio_meta.json`), jamais tout à t=0 ; les mots-clés prononcés reçoivent un `asr-keyword-glow` coral ; les coutures internes sont des coupes à vitesse égale (`cut-catalog.md`). Caméra : légère poussée au début de frame seulement, aucune dérive dans la seconde moitié.
- **Rythme :** frames 1–2 rapides et percutantes ; frames 3–5 = une même « scène atelier » (badge d'étape 01/02/03 en haut, objet central qui évolue) enchaînée en `push-slide UP` ; frame 6 = le moment « aha », plus aéré ; frame 7 court et nerveux ; frame 9 = **frame tenue** : la phrase finale se construit puis reste immobile (lecture calme avant la fin).
- **Mise en page 9:16 :** héros centré vers y ≈ 0,42 × hauteur ; tout le contenu important dans le haut 83 % (bande des sous-titres libre) ; au moins 3 plans de profondeur (fond grille + flottants, héros, libellés).
- **Liste négative :** pas de dégradé violet/bleu « IA », pas de bokeh générique, pas de logo officiel Anthropic/Claude (on écrit simplement « Claude Code » en texte), pas de vrai curseur système, pas de deux corals dans une frame ; ni diaporama (tout poser puis figer), ni économiseur d'écran (tout qui flotte en vrac au premier plan).

## Frame 1 — Le hook : toujours les mêmes consignes

- scene: Des bulles de messages identiques s'empilent en flottant ; le mot « encore » se répète puis tout se fige
- voiceover: "Tu répètes les mêmes consignes à Claude… à chaque fois ?"
- duration: 3.381s
- transition_in: cut
- status: animated
- src: compositions/frames/01-hook.html
- type: hook
- persuasion: Pain validation + répétition visuelle
- beat: Recognition + tension
- blueprint: compose
- focal: la bulle de message « Rappelle-toi : … » répétée
- roles: bulles de message tile = foreground subject · grille cream + flottants = background · compteur mono « ×3 » = supporting

narrativeRole: Ouvre le manque — la fatigue de réexpliquer la même chose à chaque conversation.
keyMessage: Répéter ses consignes à chaque fois, c'est du temps perdu.

Compose (inspiré de kinetic-type-beats) : garder le swap de mots en place comme moteur ; les « mots » deviennent des bulles de message empilées.
Scene 1 (0.0–1.0s): fond cream + grille ; une bulle de message tile flotte au centre haut avec « Rappelle-toi : réponds en français, ton direct… » — entrée per-word / spring-pop lisse (`spring-pop-entrance`, power3). Flottants d'ambiance déjà en dérive lente. Centered, héros ~50 % largeur.
Scene 2 (1.0–2.2s): sur « consignes… à Claude », deux copies identiques de la bulle s'empilent dessous en cascade décalée (`dynamic-content-sequencing`), chacune un peu plus floue ; un compteur mono « ×2 », « ×3 » s'incrémente à droite (hard-cut token cycle, `discrete-text-sequence`).
Scene 3 (2.2–3.38s): sur « à chaque fois ? », le titre display-cover « Encore ? » claque au-dessus de la pile (`kinetic-beat-slam`), seul moment coral = le point d'interrogation ; la pile tremble une fois puis se fige (tenue courte).

## Frame 2 — Le concept : un skill

- scene: Les bulles se compressent en un seul dossier qui flotte au centre ; dedans apparaît la carte SKILL.md ; le mot SKILL claque en grand
- voiceover: "La solution : un skill. Un dossier, un fichier SKILL.md… et Claude sait faire."
- duration: 7.817s
- transition_in: zoom-through
- status: animated
- src: compositions/frames/02-concept.html
- type: product_intro
- persuasion: Concretization (consigne abstraite → dossier tangible) + Distillation
- beat: Clarity + anticipation
- blueprint: compose
- focal: le dossier « mon-skill/ » flottant
- roles: dossier tile-strong = foreground subject · carte SKILL.md (navy) = supporting · mot SKILL display = foreground titre · flottants = background

narrativeRole: Nomme l'idée et la rend tangible : un skill est un objet concret, un dossier.
keyMessage: Un skill = un dossier + un fichier SKILL.md.

Compose (inspiré de kinetic-type-beats) : la frappe de mots reste le moteur, posée sur un objet dossier qui naît.
Scene 1 (0.0–1.4s): entrée zoom-through (transition) ; sur « La solution », kicker mono « ✱ LA SOLUTION » apparaît en haut (per-word reveal).
Scene 2 (1.4–2.4s): sur « un skill », le mot « skill » en display-cover se pose au centre haut avec glow coral (seul coral de la frame : le mot) — `spring-pop-entrance` lisse.
Scene 3 (2.4–3.6s): sur « Un dossier », un grand dossier illustré (onglet + étiquette mono « mon-skill/ ») monte depuis le bas et se place sous le titre (~45 % du cadre), puis commence sa lévitation douce.
Scene 4 (3.6–5.8s): sur « un fichier SKILL.md », une carte navy « SKILL.md » sort du dossier en glissant vers le haut-droite, en léger 3D, avec 3 lignes de code grisées (svg/typo) — `card-morph-anchor` pour le passage dossier→carte.
Scene 5 (5.8–7.8s): sur « et Claude sait faire », une ligne Inter « → Claude sait faire. » s'écrit sous l'ensemble (type-on, `discrete-text-sequence`) ; un petit check ✓ se dessine (`svg-path-draw`) ; tenue.

## Frame 3 — Étape 1 : le dossier

- scene: Badge « 01 » ; un terminal flottant tape la commande mkdir ; deux chemins flottent ensuite : projet et perso
- voiceover: "Étape un : crée un dossier dans point claude, slash skills. Dans ton projet… ou dans ton dossier perso."
- duration: 7.338s
- transition_in: push-slide UP
- status: animated
- src: compositions/frames/03-dossier.html
- type: feature_showcase
- persuasion: Signposting + Comparison of two options
- beat: Focus + momentum
- blueprint: prompt-type-submit-generate (Adapt)
- focal: le terminal navy qui tape la commande
- roles: badge d'étape « 01 » coral = supporting (coral unique) · terminal navy = foreground subject · deux cartes chemin (projet / perso) tile = supporting · flottants = background

narrativeRole: Premier geste concret : où vit un skill, et la différence projet / perso.
keyMessage: `.claude/skills/<nom>/` dans le projet, `~/.claude/skills/<nom>/` pour soi.

Adapt (prompt-type-submit-generate) : garder la commande tapée qui produit un résultat ; le « résultat » = les deux emplacements possibles.
Scene 1 (0.0–1.2s): badge « ÉTAPE 01 » (pastille coral) + titre headline « Le dossier » entrent en haut (per-word, power3).
Scene 2 (1.2–3.8s): un terminal navy flottant (barre à 3 points, titre mono « terminal ») se pose au centre ; la commande `mkdir -p .claude/skills/mon-skill` se tape caractère par caractère avec caret (`discrete-text-sequence` + `context-sensitive-cursor`), « .claude » arrivant sur « point claude » et « /skills » sur « slash skills ».
Scene 3 (3.8–5.6s): sur « Dans ton projet », une carte tile « 📁 Projet · .claude/skills/ » glisse depuis la gauche sous le terminal (mono-label), étiquette Inter « partagé avec l'équipe ».
Scene 4 (5.6–7.34s): sur « ou dans ton dossier perso », une seconde carte « Perso · ~/.claude/skills/ » arrive depuis la droite et s'empile ; les deux cartes flottent doucement ; tenue.

## Frame 4 — Étape 2 : l'en-tête du SKILL.md

- scene: Badge « 02 » ; même univers d'éditeur ; une carte SKILL.md flotte, l'en-tête se tape ligne à ligne : name, puis description, surlignée
- voiceover: "Étape deux : le fichier SKILL.md. En haut, deux champs : name, le nom du skill. Et description : ce qu'il fait, et quand l'utiliser."
- duration: 13.663s
- transition_in: push-slide UP
- status: animated
- src: compositions/frames/04-entete.html
- type: feature_showcase
- persuasion: Progressive disclosure (un champ à la fois)
- beat: Comprehension
- blueprint: typewriter-reveal (Adapt)
- focal: l'éditeur SKILL.md et son en-tête
- roles: badge « 02 » coral = supporting · éditeur navy « SKILL.md » = foreground subject · étiquettes de champ (« le nom », « quoi + quand ») tile = supporting · flottants = background

narrativeRole: Montre le cœur du fichier : l'en-tête YAML et ses deux champs clés.
keyMessage: L'en-tête contient name et description.

Adapt (typewriter-reveal) : le moteur = l'en-tête qui se tape ligne à ligne ; pas de logo final, la payoff est la ligne description surlignée.
Scene 1 (0.0–1.9s): badge « ÉTAPE 02 » + titre headline « Le fichier SKILL.md » en haut (per-word reveal) ; un onglet d'éditeur navy « SKILL.md » se déploie au centre (scale-in lisse depuis la carte de la frame précédente).
Scene 2 (1.9–5.5s): sur « En haut, deux champs », la ligne `---` se tape, puis deux lignes vides réservées clignotent faiblement (squelette), puis `---` de fermeture.
Scene 3 (5.5–9.8s): sur « name », `name: mon-skill` se tape avec caret ; une étiquette tile « ← le nom (la commande /mon-skill) » flotte à droite et pointe la ligne (`svg-path-draw` pour la flèche) au moment « le nom du skill ».
Scene 4 (9.8–13.66s): sur « description », `description: Rédige un post LinkedIn… Utiliser quand…` se tape ; sur « quand l'utiliser », la ligne description reçoit un surlignage coral doux (`css-marker-patterns` highlight sweep — le coral unique) et une étiquette « ← quoi + quand » ; l'éditeur se pose en lévitation ; tenue.

## Frame 5 — Étape 3 : les instructions

- scene: Badge « 03 » ; la même carte s'allonge, des lignes d'instructions Markdown se remplissent ; une étiquette « comme un brief à un collègue » flotte à côté
- voiceover: "Étape trois : dessous, écris tes instructions en Markdown… comme si tu briefais un collègue."
- duration: 6.683s
- transition_in: push-slide UP
- status: animated
- src: compositions/frames/05-instructions.html
- type: feature_showcase
- persuasion: Analogy (briefer un collègue)
- beat: Confidence
- blueprint: typewriter-reveal (Adapt)
- focal: le corps du SKILL.md qui se remplit
- roles: badge « 03 » coral = supporting · éditeur navy prolongé = foreground subject · bulle « comme un brief à un collègue » tile = supporting · flottants = background

narrativeRole: Termine le fichier : le corps, ce que Claude doit faire, écrit en langage naturel.
keyMessage: Le corps du SKILL.md, ce sont tes consignes en Markdown.

Adapt (typewriter-reveal) : même éditeur que la frame 4 (scène atelier continue), on tape le corps.
Scene 1 (0.0–1.3s): badge « ÉTAPE 03 » + titre « Les instructions » ; l'éditeur (en-tête déjà rempli, atténué à 60 %) est en place.
Scene 2 (1.3–3.9s): sur « dessous, écris tes instructions », l'éditeur s'allonge vers le bas et trois lignes Markdown se tapent l'une après l'autre : `# Instructions`, `1. Lis le sujet donné`, `2. Écris 5 lignes, ton direct` (`dynamic-content-sequencing`).
Scene 3 (3.9–4.7s): sur « Markdown », un petit tag mono « .md » pop à côté du titre (glow coral léger — le coral unique de la frame est le badge, donc le tag reste ink).
Scene 4 (4.7–6.68s): sur « comme si tu briefais un collègue », une bulle tile en EB Garamond italique « “comme un brief à un collègue” » flotte en haut-droite de l'éditeur (pull-quote, entrée lisse) ; tenue.

## Frame 6 — Le secret : la description

- scene: Plusieurs cartes de skills orbitent en flottant autour d'une bulle de demande ; une seule s'allume et se rapproche, les autres restent en veille
- voiceover: "Le secret, c'est la description. Claude les lit toutes… et charge ton skill seulement quand ta demande correspond."
- duration: 6.705s
- transition_in: blur-crossfade
- status: animated
- src: compositions/frames/06-description.html
- type: benefit_highlight
- persuasion: Demonstration (montrer le mécanisme qui tourne) + Causal chain
- beat: "Aha" + fascination
- blueprint: constellation-hub (Reproduce)
- focal: la bulle de demande au centre et la carte de skill qui s'allume
- roles: bulle demande navy = foreground subject (le hub) · 5 cartes de skills tile (« traduire », « post-linkedin », « revue-code », « résumé », « emails ») = supporting en orbite · flottants = background

narrativeRole: Révèle le mécanisme : la description sert de déclencheur, le contenu ne se charge qu'au besoin.
keyMessage: Une bonne description = un skill qui se déclenche au bon moment.

Reproduce (constellation-hub) : nodes en anneau autour d'un centre, puis résolution sur le cœur.
Scene 1 (0.0–1.9s): kicker « ✱ LE SECRET » + titre display « La description. » en haut (per-word reveal) ; au centre, une bulle de demande navy « Écris un post LinkedIn sur… » se pose.
Scene 2 (1.9–3.3s): sur « Claude les lit toutes », 5 cartes de skills (nom mono + une ligne de description Inter) apparaissent en anneau autour de la bulle via `orbit-3d-entry`, puis dérivent d'un petit arc fini (le flottant de la frame) ; un balayage mono « lecture des descriptions… » passe sur chacune (keyword glow léger en séquence).
Scene 3 (3.3–5.7s): sur « charge ton skill seulement quand », la carte « post-linkedin » s'allume (bordure coral = le coral unique), quitte l'anneau et rejoint la bulle (zoom-to-target lisse, `coordinate-target-zoom`) ; les 4 autres passent en flou de profondeur (`depth-of-field-blur`).
Scene 4 (5.7–6.7s): sur « ta demande correspond », une ligne de connexion se dessine entre la bulle et la carte (`svg-path-draw`) + petit badge « chargé ✓ » ; tenue.

## Frame 7 — L'appeler soi-même

- scene: Une barre de saisie flotte ; on tape « / », une liste de skills apparaît, « /mon-skill » se sélectionne et s'exécute
- voiceover: "Tu peux aussi l'appeler toi-même : tape slash… puis le nom du skill."
- duration: 6.284s
- transition_in: blur-crossfade
- status: animated
- src: compositions/frames/07-slash.html
- type: feature_showcase
- persuasion: Demonstration
- beat: Mastery
- blueprint: prompt-type-submit-generate (Adapt)
- focal: la barre de commande et la commande /mon-skill
- roles: barre de saisie navy = foreground subject · menu déroulant de skills tile = supporting · touche « / » géante = supporting · flottants = background

narrativeRole: Donne le contrôle manuel : l'invocation directe par commande.
keyMessage: `/nom-du-skill` lance le skill à la demande.

Adapt (prompt-type-submit-generate) : le moteur = la commande tapée puis envoyée ; ici la frappe du « / » ouvre le menu.
Scene 1 (0.0–1.9s): titre headline « Ou appelle-le toi-même » en haut (per-word) ; une barre de saisie navy flotte au centre avec placeholder « Demande quelque chose à Claude Code… ».
Scene 2 (1.9–3.5s): sur « tape slash », une grosse touche clavier « / » tombe et presse (`press-release-spring`, sans rebond), et le caractère « / » apparaît dans la barre ; un menu tile s'ouvre dessous avec 3 lignes `/mon-skill`, `/revue-code`, `/resume` (cascade).
Scene 3 (3.5–6.28s): sur « puis le nom du skill », « mon-skill » se tape après le slash, la ligne `/mon-skill` du menu se surligne (coral unique), puis le menu se referme et la barre émet une pulsation douce « ↵ » ; tenue.

## Frame 8 — Les fichiers d'appui

- scene: Le dossier s'ouvre en éventail ; des cartes flottent autour (exemples.md, reference.md, scripts/) et s'alignent en grille
- voiceover: "Besoin de plus ? Ajoute des fichiers à côté : exemples, références, scripts. Claude les ouvre seulement si besoin."
- duration: 8.447s
- transition_in: zoom-through
- status: animated
- src: compositions/frames/08-fichiers.html
- type: feature_showcase
- persuasion: Frame-then-fill + Rule of three
- beat: Foresight
- blueprint: grid-card-assemble (Adapt)
- focal: le dossier ouvert et ses fichiers d'appui
- roles: dossier « mon-skill/ » = foreground subject · cartes fichiers (SKILL.md, exemples.md, reference.md, scripts/) tile = supporting · étiquette « chargés si besoin » = supporting · flottants = background

narrativeRole: Montre comment un skill grandit sans alourdir le contexte.
keyMessage: Les fichiers d'appui se chargent seulement quand Claude en a besoin.

Adapt (grid-card-assemble) : la cascade en grille est le moteur ; les cartes sortent du dossier au lieu d'arriver du hors-champ.
Scene 1 (0.0–1.0s): titre display « Besoin de plus ? » en haut (per-word) ; le dossier « mon-skill/ » est au centre, déjà en lévitation, la carte SKILL.md visible devant.
Scene 2 (1.0–2.5s): sur « Ajoute des fichiers à côté », le dossier s'ouvre (rabat qui pivote) — `center-outward-expansion` prépare 3 emplacements en arborescence verticale sous SKILL.md (lignes hairline qui se dessinent).
Scene 3 (2.5–5.2s): « exemples.md » (2.5s), « reference.md » (3.8s), « scripts/ » (4.6s) jaillissent du dossier un par un et se rangent dans l'arborescence (staggered cascade), chacun avec icône + nom mono.
Scene 4 (5.2–8.45s): sur « Claude les ouvre seulement si besoin », les trois cartes passent en veille (opacité 55 %, contour pointillé) sauf une qui s'éclaire brièvement au mot « besoin » ; étiquette « ✱ chargés seulement si besoin » (kicker, ✱ coral = le coral unique) ; tenue.

## Frame 9 — À toi

- scene: Retour au dossier flottant du début, refermé et brillant ; la phrase finale se construit en trois temps ; « À toi de jouer » en accent
- voiceover: "Un dossier, un fichier… et Claude apprend un nouveau talent. À toi de créer ton premier skill !"
- duration: 6.493s
- transition_in: blur-crossfade
- status: animated
- src: compositions/frames/09-cta.html
- type: cta
- persuasion: Callback (le dossier du concept) + Distillation
- beat: Inspiration + resolve
- blueprint: compose
- focal: la phrase finale et le dossier refermé
- roles: phrase display = foreground subject · dossier « mon-skill/ » refermé = supporting (callback) · bouton CTA coral « À toi de jouer » = supporting (coral unique) · flottants = background

narrativeRole: Referme la boucle sur l'image du dossier et pousse à essayer tout de suite.
keyMessage: Crée ton premier skill maintenant.

Compose (inspiré de kinetic-type-beats) : construction de la phrase en 3 temps sur un dossier qui revient (callback de la frame 2) ; frame tenue.
Scene 1 (0.0–1.4s): sur « Un dossier », le dossier refermé revient au centre bas (callback) ; le mot « Un dossier, » s'écrit en display au-dessus (per-word).
Scene 2 (1.4–2.5s): sur « un fichier », « un fichier, » s'ajoute sur la ligne suivante ; une mini-carte SKILL.md se glisse dans le dossier.
Scene 3 (2.5–4.4s): sur « Claude apprend un nouveau talent », la ligne display-italic « et Claude apprend un nouveau talent. » se construit mot à mot ; ambient glow très doux derrière le dossier (`ambient-glow-bloom`).
Scene 4 (4.4–6.49s): sur « À toi de créer ton premier skill », un bouton pill coral « À toi de jouer → » apparaît (spring-pop lisse) avec la ligne mono « mkdir -p ~/.claude/skills/ton-skill » dessous ; tout se fige ; seule exit de la vidéo : fondu final doux sur les 0,4 dernières secondes.

