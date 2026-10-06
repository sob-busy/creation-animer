"""Orchestrateur : histoire -> images -> voix -> sous-titres -> vidéo finale."""

from __future__ import annotations

import json
import re
import unicodedata
from datetime import datetime
from pathlib import Path

from . import images, story, video, voice
from .config import Style


def _slug(texte: str) -> str:
    texte = unicodedata.normalize("NFKD", texte).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-zA-Z0-9]+", "-", texte).strip("-").lower()[:50] or "histoire"


class AgentVideo:
    def __init__(self, style: Style, dossier_sorties: Path):
        self.style = style
        self.sorties = dossier_sorties
        self.sorties.mkdir(parents=True, exist_ok=True)
        self.fichier_historique = self.sorties / "historique.json"

    def _historique(self) -> list[str]:
        if self.fichier_historique.exists():
            return json.loads(self.fichier_historique.read_text(encoding="utf-8"))
        return []

    def _memoriser(self, titre: str) -> None:
        titres = self._historique() + [titre]
        self.fichier_historique.write_text(json.dumps(titres, ensure_ascii=False, indent=2), encoding="utf-8")

    def creer_video(self, theme: str | None = None, demo: bool = False) -> Path:
        print("✍  Écriture de l'histoire...")
        h = story.histoire_demo() if demo else story.generer_histoire(self.style, theme, self._historique())
        print(f"   « {h['titre']} » — {len(h['scenes'])} scènes")

        dossier = self.sorties / f"{datetime.now():%Y%m%d-%H%M%S}_{_slug(h['titre'])}"
        travail = dossier / "travail"
        travail.mkdir(parents=True)
        (dossier / "histoire.json").write_text(json.dumps(h, ensure_ascii=False, indent=2), encoding="utf-8")

        clips: list[Path] = []
        tous_les_mots: list[voice.Mot] = []
        decalage = 0.0
        for i, scene in enumerate(h["scenes"]):
            print(f"🎬 Scène {i + 1}/{len(h['scenes'])}")
            prompt = images.prompt_complet(self.style, h["personnages"], scene["prompt_image"])
            img = images.generer_image(self.style, prompt, travail / f"scene_{i:02d}.png", i)
            audio, mots = voice.synthetiser(self.style, scene["narration"], travail / f"voix_{i:02d}.mp3")
            duree = voice.duree_audio(audio) + video.PAUSE_FIN_SCENE
            clips.append(video.clip_scene(self.style, img, audio, duree, i, travail / f"clip_{i:02d}.mp4"))
            tous_les_mots += [(m, d + decalage, f + decalage) for m, d, f in mots]
            decalage += voice.duree_audio(clips[-1])

        print("🧩 Montage final...")
        st = video.ecrire_sous_titres(self.style, tous_les_mots, travail / "sous_titres.ass")
        final = video.assembler(self.style, clips, st, travail / "video.mp4")
        cible = dossier / "video.mp4"
        final.replace(cible)

        (dossier / "description.txt").write_text(
            f"{h['description_tiktok']}\n\n{' '.join(h['hashtags'])}\n", encoding="utf-8"
        )
        if not demo:
            self._memoriser(h["titre"])
        print(f"✅ Vidéo prête : {cible}  ({decalage:.0f} s)")
        return cible
