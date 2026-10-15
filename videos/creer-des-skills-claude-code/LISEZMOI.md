# Vidéo : créer des skills dans Claude Code

Explainer TikTok en motion design (1080×1920, ~51 s), voix off française Kokoro (ff_siwis), dynamique, fait avec HyperFrames.

- `renders/video.mp4` : la vidéo finale
- `BRIEF.md`, `STORYBOARD.md`, `SCRIPT.md` : le brief, les 9 scènes et le texte de la voix off
- `compositions/frames/*.html` : les 9 scènes animées (GSAP), générées par `scripts/generer_frames.py`
- `scripts/voix_off.py` : voix off + timing des mots pour les sous-titres
  (`--moteur edge --voix fr-FR-HenriNeural` pour une voix plus naturelle si edge-tts est joignable)
- `scripts/musique_sfx.py` : musique de fond et whooshs synthétisés localement

Refaire la vidéo :

```bash
python3 scripts/voix_off.py --moteur kokoro --modele kokoro-v1.0.int8.onnx --voix-kokoro voices-v1.0.bin   # ou --moteur edge --voix fr-FR-HenriNeural
python3 scripts/musique_sfx.py
node ~/.claude/skills/faceless-explainer/scripts/audio.mjs sync-durations --audio-meta ./audio_meta.json --storyboard ./STORYBOARD.md
python3 scripts/generer_frames.py .
node ~/.claude/skills/faceless-explainer/scripts/captions.mjs build --storyboard ./STORYBOARD.md --audio-meta ./audio_meta.json --hyperframes . --out ./caption_groups.json
node ~/.claude/skills/faceless-explainer/scripts/assemble-index.mjs --storyboard ./STORYBOARD.md --hyperframes .
node ~/.claude/skills/faceless-explainer/scripts/transitions.mjs inject --storyboard ./STORYBOARD.md --hyperframes .
npx hyperframes check && npx hyperframes render --quality high --output renders/video.mp4
```
