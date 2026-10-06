"""Réglages de l'agent : format vidéo, style visuel, voix, ton des histoires.

Toutes les valeurs peuvent être surchargées par un fichier JSON passé avec
`--style styles/mon_style.json` (seules les clés présentes sont remplacées).
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field, fields
from pathlib import Path


@dataclass
class Style:
    # --- Histoire ---
    langue: str = "français"
    genre: str = "conte animé émouvant avec une morale"
    public: str = "grand public, TikTok"
    duree_cible_secondes: int = 60
    nombre_scenes: int = 8
    ton: str = "captivant, émouvant, avec une accroche forte dans la première phrase"
    consignes_supplementaires: str = ""

    # --- Visuel ---
    style_visuel: str = (
        "3D animation style, Pixar-like, cinematic lighting, vibrant colors, "
        "highly detailed, vertical 9:16 composition"
    )
    fournisseur_images: str = "placeholder"  # "placeholder" | "openai"
    modele_images: str = "gpt-image-1"

    # --- Voix ---
    fournisseur_voix: str = "edge"  # "edge" (gratuit) | "silence"
    voix: str = "fr-FR-HenriNeural"
    vitesse_voix: str = "+5%"

    # --- Vidéo ---
    largeur: int = 1080
    hauteur: int = 1920
    fps: int = 30
    zoom_max: float = 1.15
    musique: str = ""  # chemin d'un mp3 de fond (optionnel)
    volume_musique: float = 0.12

    # --- Sous-titres ---
    police: str = "DejaVu Sans"
    taille_sous_titres: int = 78
    mots_par_sous_titre: int = 3
    couleur_surlignage: str = "&H0000E5FF"  # format ASS (&HAABBGGRR) : jaune

    # --- Modèle Claude ---
    modele_claude: str = "claude-opus-5-5"
    effort: str = "high"

    extra: dict = field(default_factory=dict)

    @classmethod
    def charger(cls, chemin: str | None) -> "Style":
        style = cls()
        if not chemin:
            return style
        donnees = json.loads(Path(chemin).read_text(encoding="utf-8"))
        connus = {f.name for f in fields(cls)}
        for cle, valeur in donnees.items():
            if cle in connus:
                setattr(style, cle, valeur)
            else:
                style.extra[cle] = valeur
        return style
