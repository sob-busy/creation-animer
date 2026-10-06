"""Ligne de commande.

Exemples :
    python -m agent_video --demo
    python -m agent_video --theme "un chat qui veut devenir astronaute"
    python -m agent_video --nombre 5 --style styles/conte_anime.json
"""

from __future__ import annotations

import argparse
from pathlib import Path

from .agent import AgentVideo
from .config import Style


def main() -> None:
    p = argparse.ArgumentParser(prog="agent_video", description="Agent IA de création de vidéos d'histoires animées")
    p.add_argument("--theme", help="Thème de l'histoire (sinon Claude en invente un)")
    p.add_argument("--nombre", type=int, default=1, help="Nombre de vidéos à créer")
    p.add_argument("--style", help="Fichier JSON de style (voir styles/)")
    p.add_argument("--sorties", default="sorties", help="Dossier de sortie")
    p.add_argument("--demo", action="store_true", help="Histoire de démonstration, sans appel à Claude")
    args = p.parse_args()

    agent = AgentVideo(Style.charger(args.style), Path(args.sorties))
    for n in range(args.nombre):
        if args.nombre > 1:
            print(f"\n===== Vidéo {n + 1}/{args.nombre} =====")
        agent.creer_video(theme=args.theme, demo=args.demo)


if __name__ == "__main__":
    main()
