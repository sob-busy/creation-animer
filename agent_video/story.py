"""Génération d'histoires originales avec Claude (sortie JSON structurée)."""

from __future__ import annotations

import json

import anthropic

from .config import Style

SCHEMA = {
    "type": "object",
    "properties": {
        "titre": {"type": "string"},
        "accroche": {"type": "string"},
        "personnages": {
            "type": "string",
            "description": "Description visuelle fixe des personnages (en anglais), "
            "réutilisée dans chaque prompt d'image pour garder la cohérence.",
        },
        "scenes": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "narration": {"type": "string"},
                    "prompt_image": {"type": "string"},
                },
                "required": ["narration", "prompt_image"],
                "additionalProperties": False,
            },
        },
        "description_tiktok": {"type": "string"},
        "hashtags": {"type": "array", "items": {"type": "string"}},
    },
    "required": [
        "titre",
        "accroche",
        "personnages",
        "scenes",
        "description_tiktok",
        "hashtags",
    ],
    "additionalProperties": False,
}

SYSTEME = """Tu es scénariste pour une chaîne TikTok d'histoires animées courtes en format vertical.
Chaque vidéo est une histoire complète, racontée en voix off, illustrée par une suite d'images.

Règles d'écriture :
- La première phrase de la narration est l'accroche : elle doit donner envie de rester dès la première seconde.
- Phrases courtes, faciles à dire à voix haute, rythme soutenu, une émotion claire.
- Une vraie progression : situation, problème, retournement, chute ou morale.
- La narration de toutes les scènes, lue bout à bout, forme l'histoire entière.
- Histoires 100 % originales : ne reprends aucune histoire déjà connue ni aucun titre de la liste à éviter.

Règles pour les images :
- `personnages` : une description visuelle précise et stable (âge, vêtements, couleurs, traits), en anglais.
- `prompt_image` : en anglais, décrit uniquement ce qu'on voit dans la scène (cadrage, action, décor, lumière),
  sans texte ni lettres dans l'image. Ne répète pas le style graphique, il est ajouté automatiquement."""


def _consigne(style: Style, theme: str | None, a_eviter: list[str]) -> str:
    mots = int(style.duree_cible_secondes * 2.6)  # ~2,6 mots/seconde en voix off
    lignes = [
        f"Écris une nouvelle histoire en {style.langue}.",
        f"Genre : {style.genre}.",
        f"Public : {style.public}.",
        f"Ton : {style.ton}.",
        f"Nombre de scènes : exactement {style.nombre_scenes}.",
        f"Longueur totale de la narration : environ {mots} mots "
        f"(≈ {style.duree_cible_secondes} secondes lues).",
        f"Thème imposé : {theme}." if theme else "Thème : choisis-en un nouveau et surprenant.",
    ]
    if style.consignes_supplementaires:
        lignes.append(f"Consignes supplémentaires : {style.consignes_supplementaires}")
    if a_eviter:
        lignes.append("Titres déjà publiés, à ne pas refaire : " + " | ".join(a_eviter[-50:]))
    return "\n".join(lignes)


def generer_histoire(
    style: Style, theme: str | None = None, a_eviter: list[str] | None = None
) -> dict:
    client = anthropic.Anthropic()
    reponse = client.beta.messages.create(
        model=style.modele_claude,
        max_tokens=16000,
        betas=["server-side-fallback-2026-07-01"],
        fallbacks="default",
        output_config={
            "effort": style.effort,
            "format": {"type": "json_schema", "schema": SCHEMA},
        },
        system=SYSTEME,
        messages=[{"role": "user", "content": _consigne(style, theme, a_eviter or [])}],
    )
    if reponse.stop_reason == "refusal":
        raise RuntimeError("Claude a refusé ce thème. Essaie un autre thème.")
    if reponse.stop_reason == "max_tokens":
        raise RuntimeError("Réponse tronquée : réduis le nombre de scènes ou la durée.")
    texte = next(b.text for b in reponse.content if b.type == "text")
    return json.loads(texte)


def histoire_demo() -> dict:
    """Histoire fixe pour tester le montage sans clé API."""
    return {
        "titre": "La luciole qui avait peur du noir",
        "accroche": "Une luciole qui a peur du noir, tu imagines ?",
        "personnages": "Lumi, a tiny firefly with big round eyes, a glowing yellow tail and a red scarf",
        "scenes": [
            {
                "narration": "Une luciole qui a peur du noir, tu imagines ? C'était Lumi.",
                "prompt_image": "close-up of Lumi trembling on a leaf at dusk, worried face",
            },
            {
                "narration": "Chaque soir, ses amies s'envolaient pour illuminer la forêt. Lui restait caché sous une feuille.",
                "prompt_image": "hundreds of fireflies flying over a dark forest while Lumi hides under a leaf",
            },
            {
                "narration": "Une nuit, une petite fille s'est perdue entre les arbres. Elle pleurait.",
                "prompt_image": "a little girl crying alone in a dark forest at night, moonlight",
            },
            {
                "narration": "Toutes les lucioles étaient loin. Il ne restait que Lumi.",
                "prompt_image": "Lumi peeking out from his leaf, looking at the lost girl, determined",
            },
            {
                "narration": "Il a pris une grande inspiration, et il a allumé sa lumière, plus fort que jamais.",
                "prompt_image": "Lumi glowing brightly, light rays piercing the darkness",
            },
            {
                "narration": "Pas à pas, il l'a guidée jusqu'à chez elle. Et ce soir-là, Lumi a compris.",
                "prompt_image": "Lumi leading the smiling girl toward a warm cottage with lit windows",
            },
            {
                "narration": "Le courage, ce n'est pas ne pas avoir peur. C'est briller quand même.",
                "prompt_image": "Lumi proudly glowing on the windowsill, starry sky behind, heartwarming",
            },
        ],
        "description_tiktok": "Le courage, c'est briller quand même ✨",
        "hashtags": ["#histoire", "#conte", "#animation", "#courage", "#pourtoi"],
    }
