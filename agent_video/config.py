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
    genre: str = "conte animé façon film Pixar, émouvant, avec une morale"
    public: str = "grand public, TikTok"
    duree_cible_secondes: int = 60
    nombre_scenes: int = 8
    ton: str = "chaleureux et captivant, voix de conteur, accroche forte dans la première phrase"
    consignes_supplementaires: str = (
        "Un héros attachant (enfant, animal ou objet qui prend vie) avec un rêve ou une peur, "
        "un obstacle, un moment de bravoure ou de tendresse, puis une fin qui touche le cœur. "
        "Termine par une morale courte et mémorable."
    )

    # --- Visuel ---
    style_visuel: str = (
        "Pixar-style 3D animated film still, expressive cartoon characters with big eyes, "
        "soft global illumination, warm cinematic lighting, rich saturated colors, "
        "subsurface scattering, shallow depth of field, highly detailed, vertical 9:16 composition"
    )
    # "auto" = OpenAI si OPENAI_API_KEY est défini, sinon images de test
    fournisseur_images: str = "auto"  # "auto" | "openai" | "placeholder"
    modele_images: str = "gpt-image-1"

    # --- Voix ---
    fournisseur_voix: str = "edge"  # "edge" (gratuit) | "silence"
    voix: str = "fr-FR-HenriNeural"  # voix d'homme ; autre choix : fr-FR-RemyMultilingualNeural
    vitesse_voix: str = "+0%"

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
