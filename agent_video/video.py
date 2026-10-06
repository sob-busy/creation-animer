"""Montage vidéo vertical avec ffmpeg : zoom lent sur chaque image, voix off,
sous-titres mot à mot surlignés et musique de fond optionnelle."""

from __future__ import annotations

import subprocess
from pathlib import Path

from .config import Style
from .voice import Mot

PAUSE_FIN_SCENE = 0.35  # respiration entre deux scènes (secondes)


def _ffmpeg(*args: str) -> None:
    subprocess.run(["ffmpeg", "-y", "-v", "error", *args], check=True)


def clip_scene(style: Style, image: Path, audio: Path, duree: float, index: int, sortie: Path) -> Path:
    w, h, fps = style.largeur, style.hauteur, style.fps
    images = max(1, int(duree * fps))
    pas = (style.zoom_max - 1) / images
    # Alterne zoom avant / zoom arrière pour varier le mouvement d'une scène à l'autre.
    zoom = f"min(1+{pas:.6f}*on,{style.zoom_max})" if index % 2 == 0 else \
           f"max({style.zoom_max}-{pas:.6f}*on,1)"
    filtre = (
        f"[0:v]scale={w * 2}:{h * 2}:force_original_aspect_ratio=increase,crop={w * 2}:{h * 2},"
        f"zoompan=z='{zoom}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={images}:s={w}x{h}:fps={fps},"
        f"fade=t=in:st=0:d=0.25,format=yuv420p[v];"
        f"[1:a]apad=pad_dur={PAUSE_FIN_SCENE},aresample=44100[a]"
    )
    _ffmpeg(
        "-loop", "1", "-i", str(image), "-i", str(audio),
        "-filter_complex", filtre, "-map", "[v]", "-map", "[a]",
        "-t", f"{duree:.3f}", "-r", str(fps),
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
        "-c:a", "aac", "-b:a", "160k", "-ac", "2", str(sortie),
    )
    return sortie


def _temps_ass(t: float) -> str:
    h, reste = divmod(t, 3600)
    m, s = divmod(reste, 60)
    return f"{int(h)}:{int(m):02d}:{s:05.2f}"


def _echapper(texte: str) -> str:
    return texte.replace("\\", "").replace("{", "(").replace("}", ")")


def ecrire_sous_titres(style: Style, mots: list[Mot], sortie: Path) -> Path:
    """Sous-titres ASS façon TikTok : groupes de quelques mots, le mot prononcé surligné."""
    entete = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {style.largeur}
PlayResY: {style.hauteur}
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Def,{style.police},{style.taille_sous_titres},&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,-1,0,0,0,100,100,0,0,1,6,3,2,80,80,{int(style.hauteur * 0.30)},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    lignes = []
    n = max(1, style.mots_par_sous_titre)
    for i in range(0, len(mots), n):
        groupe = mots[i:i + n]
        fin_groupe = mots[i + n][1] if i + n < len(mots) else groupe[-1][2]
        for j, (_, debut, fin) in enumerate(groupe):
            fin = groupe[j + 1][1] if j + 1 < len(groupe) else fin_groupe
            texte = " ".join(
                f"{{\\c{style.couleur_surlignage}}}{_echapper(m).upper()}{{\\c&H00FFFFFF}}" if k == j
                else _echapper(m).upper()
                for k, (m, _, _) in enumerate(groupe)
            )
            lignes.append(f"Dialogue: 0,{_temps_ass(debut)},{_temps_ass(fin)},Def,,0,0,0,,{texte}")
    sortie.write_text(entete + "\n".join(lignes) + "\n", encoding="utf-8")
    return sortie


def assembler(style: Style, clips: list[Path], sous_titres: Path, sortie: Path) -> Path:
    dossier = sortie.parent
    liste = dossier / "clips.txt"
    liste.write_text("".join(f"file '{c.name}'\n" for c in clips), encoding="utf-8")
    brut = dossier / "brut.mp4"
    _ffmpeg("-f", "concat", "-safe", "0", "-i", str(liste), "-c", "copy", str(brut))

    # Chemin relatif + cwd pour éviter les soucis d'échappement du filtre subtitles.
    filtre_v = f"subtitles={sous_titres.name}"
    args = ["-i", brut.name]
    if style.musique and Path(style.musique).exists():
        args += ["-stream_loop", "-1", "-i", str(Path(style.musique).resolve())]
        filtre = (
            f"[0:v]{filtre_v}[v];[1:a]volume={style.volume_musique}[m];"
            f"[0:a][m]amix=inputs=2:duration=first:dropout_transition=0[a]"
        )
        args += ["-filter_complex", filtre, "-map", "[v]", "-map", "[a]"]
    else:
        args += ["-vf", filtre_v, "-map", "0:v", "-map", "0:a"]
    subprocess.run(
        ["ffmpeg", "-y", "-v", "error", *args, "-c:v", "libx264", "-preset", "medium",
         "-crf", "19", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", sortie.name],
        check=True, cwd=dossier,
    )
    brut.unlink(missing_ok=True)
    return sortie
