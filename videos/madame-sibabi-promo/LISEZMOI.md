# Pub vidéo : Madame SIBABI

Publicité motion design (1080×1920, 55 s) pour Madame SIBABI, vendeuse de jus naturels et salade délicieuse, faite avec HyperFrames.

- `renders/video.mp4` : la vidéo finale (TikTok, WhatsApp, Facebook, Instagram)
- `description.txt` : texte et hashtags à copier en légende
- `BRIEF.md`, `STORYBOARD.md`, `SCRIPT.md` : le brief, les 9 scènes, le texte de la voix off
- `capture/source/` : les deux affiches d'origine ; `capture/assets/` : les photos découpées dedans
- `scripts/generer_frames.py` : génère les 9 scènes animées (logo vectoriel, verres qui se remplissent, fruits flottants…)
- `scripts/voix_off.py` : voix off (Kokoro `ff_siwis`, ou `--moteur edge --voix fr-FR-DeniseNeural`)
- `scripts/musique_sfx.py` : musique tropicale et bruitages synthétisés localement

Refaire la vidéo après une modification du texte (`STORYBOARD.md` puis `SCRIPT.md`) :

```bash
python3 scripts/voix_off.py --moteur kokoro --modele kokoro-v1.0.int8.onnx --voix-kokoro voices-v1.0.bin
python3 scripts/musique_sfx.py
H=~/.claude/skills/product-launch-video/scripts
node $H/audio.mjs sync-durations --audio-meta ./audio_meta.json --storyboard ./STORYBOARD.md
python3 scripts/generer_frames.py .
node $H/captions.mjs build --storyboard ./STORYBOARD.md --audio-meta ./audio_meta.json --hyperframes . --out ./caption_groups.json
node $H/assemble-index.mjs --storyboard ./STORYBOARD.md --hyperframes .
node $H/transitions.mjs inject --storyboard ./STORYBOARD.md --hyperframes .
npx hyperframes check && npx hyperframes render --quality high --output renders/video.mp4
```
