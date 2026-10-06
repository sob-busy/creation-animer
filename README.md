# Création d'Animer — Agent IA de vidéos d'histoires

Un agent qui crée automatiquement des vidéos TikTok verticales (1080×1920) de **contes animés en 3D façon Pixar**, racontés par une **voix d'homme**, avec des histoires **toujours nouvelles** :

1. **Histoire**, écrite par Claude : accroche, scènes, description TikTok, hashtags. Les titres déjà faits sont mémorisés pour ne jamais refaire la même histoire.
2. **Images**, une par scène, avec des personnages décrits pareil d'une scène à l'autre.
3. **Voix off** en français (edge-tts, gratuit).
4. **Sous-titres** façon TikTok, mot à mot, avec le mot prononcé surligné en jaune.
5. **Montage** avec ffmpeg : zoom lent sur chaque image, enchaînement des scènes, musique de fond si tu en mets une.

## Installation

```bash
# ffmpeg est obligatoire : https://ffmpeg.org/download.html
pip install -r requirements.txt
export ANTHROPIC_API_KEY="ta-clé"          # https://console.anthropic.com
# Optionnel, pour de vraies images IA :
pip install openai && export OPENAI_API_KEY="ta-clé"
```

## Utilisation

```bash
# Test rapide, sans clé API (histoire de démonstration)
python -m agent_video --demo

# Une nouvelle histoire inventée par l'IA
python -m agent_video

# Avec un thème imposé
python -m agent_video --theme "un petit robot qui cherche sa maman"

# 5 vidéos d'un coup, dans un style précis
python -m agent_video --nombre 5 --style styles/conte_pixar.json
```

Chaque vidéo est rangée dans `sorties/<date>_<titre>/` :

| Fichier | Contenu |
|---|---|
| `video.mp4` | la vidéo, prête à publier |
| `description.txt` | la légende et les hashtags à copier dans TikTok |
| `histoire.json` | le scénario complet (narration et prompts d'images) |
| `travail/` | les fichiers intermédiaires (images, voix, sous-titres) |

## Personnaliser le style

Copie un fichier de `styles/` et change ce que tu veux. Toutes les options sont dans `agent_video/config.py` :

- `genre`, `ton`, `public`, `duree_cible_secondes`, `nombre_scenes` : le type d'histoire
- `style_visuel` : le rendu des images (3D Pixar, anime, aquarelle…)
- `fournisseur_images` : `auto` (par défaut : vraies images IA si `OPENAI_API_KEY` est défini, sinon images de test), `openai` ou `placeholder`
- `voix` : voix d'homme `fr-FR-HenriNeural` (par défaut) ou `fr-FR-RemyMultilingualNeural` ; voix de femme `fr-FR-DeniseNeural` ou `fr-FR-VivienneMultilingualNeural`
- `musique` : chemin vers un mp3 de fond
- `consignes_supplementaires` : toute règle en plus pour l'IA (par exemple « finir par une question au spectateur »)
