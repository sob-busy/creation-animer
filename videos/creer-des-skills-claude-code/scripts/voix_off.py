"""Voix off de la vidéo : SCRIPT.md -> assets/voice/NN.wav + audio_meta.json (voices[].words).

Chaque réplique est découpée en morceaux de phrase synthétisés séparément, ce qui donne
le timing réel de chaque morceau ; les mots sont ensuite répartis dans leur morceau
selon leur longueur. Les sous-titres affichent le texte d'origine, la synthèse reçoit
une version « phonétique » (skill -> skile, etc.) pour une meilleure prononciation.

    python3 scripts/voix_off.py --moteur piper --modele /chemin/fr-gilles-low.onnx
    python3 scripts/voix_off.py --moteur edge --voix fr-FR-HenriNeural
"""

from __future__ import annotations

import argparse
import asyncio
import json
import re
import subprocess
import tempfile
import wave
from pathlib import Path

PHONETIQUE = [
    (r"SKILL\.md", "skile point M D"),
    (r"\bskills\b", "skiles"),
    (r"\bskill\b", "skile"),
    (r"\bClaude\b", "Clôde"),
    (r"\bclaude\b", "clôde"),
    (r"\bname\b", "nème"),
    (r"\bMarkdown\b", "markdaoune"),
    (r"\bslash\b", "slache"),
    (r"…", ","),
]
PAUSE_MORCEAU = 0.16
DEBUT, FIN = 0.1, 0.4  # silence avant la 1re phrase et après la dernière (s)
SR = 44100


def lignes_script(chemin: Path) -> list[tuple[int, str]]:
    lignes, frame = [], None
    for l in chemin.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^#{2,3}\s+.*\(frame\s+(\d+)\)", l, re.I)
        if m:
            frame = int(m.group(1))
        elif frame is not None and re.match(r"^( {4,}|\t)\S", l):
            lignes.append((frame, l.strip()))
            frame = None
    return lignes


def morceaux(texte: str) -> list[str]:
    parties = re.split(r"(?<=[.,:;!?…])\s+", texte)
    return [p for p in (x.strip() for x in parties) if p]


def phonetique(texte: str) -> str:
    for motif, rempl in PHONETIQUE:
        texte = re.sub(motif, rempl, texte)
    return texte


def synth_piper(modele: str, texte: str, sortie: Path, vitesse: float = 0.82) -> None:
    subprocess.run(["python3", "-m", "piper", "-m", modele, "-f", str(sortie),
                    "--length-scale", str(vitesse)],
                   input=texte.encode(), check=True, capture_output=True)


def synth_edge(voix: str, texte: str, sortie: Path) -> None:
    import edge_tts

    mp3 = sortie.with_suffix(".mp3")
    asyncio.run(edge_tts.Communicate(texte, voix, rate="+8%").save(str(mp3)))
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(mp3), str(sortie)], check=True)


def normaliser(entree: Path, sortie: Path) -> float:
    """44,1 kHz mono, silences de bord coupés ; renvoie la durée."""
    subprocess.run([
        "ffmpeg", "-y", "-v", "error", "-i", str(entree), "-af",
        "silenceremove=start_periods=1:start_threshold=-45dB,areverse,"
        "silenceremove=start_periods=1:start_threshold=-45dB,areverse",
        "-ar", str(SR), "-ac", "1", str(sortie)], check=True)
    with wave.open(str(sortie)) as w:
        return w.getnframes() / w.getframerate()


def silence(duree: float, sortie: Path) -> None:
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "lavfi", "-i",
                    f"anullsrc=r={SR}:cl=mono", "-t", f"{duree:.3f}", str(sortie)], check=True)


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--moteur", choices=["piper", "edge"], default="piper")
    p.add_argument("--modele", help="modèle Piper .onnx")
    p.add_argument("--voix", default="fr-FR-HenriNeural")
    p.add_argument("--projet", default=".")
    a = p.parse_args()

    projet = Path(a.projet).resolve()
    dossier = projet / "assets" / "voice"
    dossier.mkdir(parents=True, exist_ok=True)
    meta_path = projet / "audio_meta.json"
    meta = json.loads(meta_path.read_text()) if meta_path.exists() else {"bgm": None, "sfx": []}
    voix = []

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        for frame, texte in lignes_script(projet / "SCRIPT.md"):
            pistes, mots, t = [], [], DEBUT
            silence(DEBUT, tmp / "d.wav")
            pistes.append(tmp / "d.wav")
            parts = morceaux(texte)
            for i, part in enumerate(parts):
                brut, net = tmp / f"{frame}_{i}_b.wav", tmp / f"{frame}_{i}.wav"
                (synth_piper(a.modele, phonetique(part), brut) if a.moteur == "piper"
                 else synth_edge(a.voix, phonetique(part), brut))
                d = normaliser(brut, net)
                affiches = part.replace("…", "").split()
                poids = [len(m) + 1 for m in affiches]
                tot, c = sum(poids), t
                for m, pw in zip(affiches, poids):
                    dm = d * pw / tot
                    mots.append({"text": m, "start": round(c, 3), "end": round(c + dm, 3)})
                    c += dm
                pistes.append(net)
                t += d
                if i < len(parts) - 1:
                    pause = PAUSE_MORCEAU * (1.6 if part.endswith((".", "?", "!", "…")) else 1)
                    silence(pause, tmp / f"{frame}_{i}_p.wav")
                    pistes.append(tmp / f"{frame}_{i}_p.wav")
                    t += pause
            silence(FIN, tmp / "f.wav")
            pistes.append(tmp / "f.wav")
            liste = tmp / "l.txt"
            liste.write_text("".join(f"file '{x}'\n" for x in pistes))
            sortie = dossier / f"{frame:02d}.wav"
            subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0",
                            "-i", str(liste), "-af", "loudnorm=I=-16:TP=-1.5:LRA=7",
                            "-ar", str(SR), str(sortie)], check=True)
            with wave.open(str(sortie)) as w:
                duree = round(w.getnframes() / w.getframerate(), 3)
            for k, m in enumerate(mots):
                m["id"] = f"w{k}"
            voix.append({"frame": frame, "path": f"assets/voice/{frame:02d}.wav",
                         "duration_s": duree, "words": mots})
            print(f"frame {frame:02d}: {duree:.2f}s · {len(mots)} mots")

    meta["voices"] = voix
    meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2))
    print(f"total voix : {sum(v['duration_s'] for v in voix):.1f}s → {meta_path}")


if __name__ == "__main__":
    main()
