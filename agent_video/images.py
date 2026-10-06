"""Création des images de chaque scène."""

from __future__ import annotations

import base64
import os
import random
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

from .config import Style


def prompt_complet(style: Style, personnages: str, prompt_scene: str) -> str:
    return f"{prompt_scene}. Characters: {personnages}. Style: {style.style_visuel}. No text."


def generer_image(style: Style, prompt: str, sortie: Path, index: int) -> Path:
    fournisseur = style.fournisseur_images
    if fournisseur == "auto":
        fournisseur = "openai" if os.environ.get("OPENAI_API_KEY") else "placeholder"
    if fournisseur == "openai":
        return _openai(style, prompt, sortie)
    return _placeholder(style, prompt, sortie, index)


def _openai(style: Style, prompt: str, sortie: Path) -> Path:
    from openai import OpenAI  # pip install openai ; nécessite OPENAI_API_KEY

    client = OpenAI()
    resultat = client.images.generate(model=style.modele_images, prompt=prompt, size="1024x1536")
    sortie.write_bytes(base64.b64decode(resultat.data[0].b64_json))
    return sortie


def _police(taille: int) -> ImageFont.FreeTypeFont:
    for chemin in (
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/Library/Fonts/Arial Bold.ttf",
        "C:/Windows/Fonts/arialbd.ttf",
    ):
        if Path(chemin).exists():
            return ImageFont.truetype(chemin, taille)
    return ImageFont.load_default()


def _placeholder(style: Style, prompt: str, sortie: Path, index: int) -> Path:
    """Image de remplacement (dégradé + description) pour tester sans API d'images."""
    rng = random.Random(index * 7919 + len(prompt))
    w, h = style.largeur, style.hauteur
    haut = tuple(rng.randint(20, 90) for _ in range(3))
    bas = tuple(rng.randint(110, 220) for _ in range(3))
    img = Image.new("RGB", (w, h))
    px = ImageDraw.Draw(img)
    for y in range(h):
        t = y / h
        px.line([(0, y), (w, y)], fill=tuple(int(a + (b - a) * t) for a, b in zip(haut, bas)))
    halo = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    dh = ImageDraw.Draw(halo)
    for _ in range(25):
        x, y, r = rng.randint(0, w), rng.randint(0, h), rng.randint(40, 220)
        dh.ellipse([x - r, y - r, x + r, y + r], fill=(255, 255, 255, rng.randint(10, 40)))
    img = Image.alpha_composite(img.convert("RGBA"), halo.filter(ImageFilter.GaussianBlur(30)))
    d = ImageDraw.Draw(img)
    d.text((w // 2, h * 0.18), f"SCÈNE {index + 1}", font=_police(70), fill="white", anchor="mm")
    texte = "\n".join(textwrap.wrap(prompt.split(". Characters:")[0], 32))
    d.multiline_text((w // 2, h * 0.32), texte, font=_police(44), fill=(255, 255, 255, 220),
                     anchor="ma", align="center", spacing=14)
    img.convert("RGB").save(sortie)
    return sortie
