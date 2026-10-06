"""Voix off : synthèse vocale + horodatage des mots pour les sous-titres."""

from __future__ import annotations

import asyncio
import subprocess
from pathlib import Path

from .config import Style

# Un mot = (texte, début en secondes, fin en secondes)
Mot = tuple[str, float, float]


def duree_audio(chemin: Path) -> float:
    sortie = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", str(chemin)],
        capture_output=True, text=True, check=True,
    )
    return float(sortie.stdout.strip())


def synthetiser(style: Style, texte: str, sortie: Path) -> tuple[Path, list[Mot]]:
    if style.fournisseur_voix == "edge":
        try:
            return asyncio.run(_edge(style, texte, sortie))
        except Exception as erreur:  # réseau indisponible, voix inconnue...
            print(f"  ⚠ voix edge-tts indisponible ({erreur}), piste muette utilisée")
    return _silence(texte, sortie)


async def _edge(style: Style, texte: str, sortie: Path) -> tuple[Path, list[Mot]]:
    import edge_tts

    com = edge_tts.Communicate(texte, style.voix, rate=style.vitesse_voix, boundary="WordBoundary")
    mots: list[Mot] = []
    with open(sortie, "wb") as f:
        async for morceau in com.stream():
            if morceau["type"] == "audio":
                f.write(morceau["data"])
            elif morceau["type"] == "WordBoundary":
                debut = morceau["offset"] / 1e7
                mots.append((morceau["text"], debut, debut + morceau["duration"] / 1e7))
    if not mots:
        mots = repartir_mots(texte, duree_audio(sortie))
    return sortie, mots


def _silence(texte: str, sortie: Path) -> tuple[Path, list[Mot]]:
    duree = max(2.0, len(texte.split()) / 2.6)
    subprocess.run(
        ["ffmpeg", "-y", "-v", "error", "-f", "lavfi", "-i", "anullsrc=r=24000:cl=mono",
         "-t", f"{duree:.2f}", "-c:a", "libmp3lame", str(sortie)],
        check=True,
    )
    return sortie, repartir_mots(texte, duree)


def repartir_mots(texte: str, duree: float) -> list[Mot]:
    """Répartit les mots proportionnellement à leur longueur quand on n'a pas d'horodatage."""
    mots = texte.split()
    poids = [len(m) + 2 for m in mots]
    total, t, resultat = sum(poids), 0.0, []
    for mot, p in zip(mots, poids):
        d = duree * p / total
        resultat.append((mot, t, t + d))
        t += d
    return resultat
