"""Musique de fond et bruitages synthétisés localement (aucun service externe).

Écrit assets/music/bed.wav, assets/sfx/{whoosh,pop,tick}.wav et ajoute à audio_meta.json
la musique + un whoosh au début de chaque frame (entrées "source": "host").

    python3 scripts/musique_sfx.py
"""

from __future__ import annotations

import json
import wave
from pathlib import Path

import numpy as np

SR = 44100
BPM = 92
RNG = np.random.default_rng(7)  # déterministe


def ecrire(chemin: Path, x: np.ndarray) -> None:
    chemin.parent.mkdir(parents=True, exist_ok=True)
    x = np.clip(x, -1, 1)
    pcm = (np.column_stack([x, x]) * 32767).astype(np.int16) if x.ndim == 1 else (x * 32767).astype(np.int16)
    with wave.open(str(chemin), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())


def env(n: int, a: float, r: float) -> np.ndarray:
    t = np.arange(n) / SR
    return np.minimum(1, t / max(a, 1e-4)) * np.exp(-t / r)


def note(f: float, dur: float, kind: str = "saw", a=0.01, r=0.3) -> np.ndarray:
    n = int(dur * SR)
    t = np.arange(n) / SR
    if kind == "sine":
        s = np.sin(2 * np.pi * f * t)
    else:  # dents de scie douces (somme d'harmoniques)
        s = sum(np.sin(2 * np.pi * f * k * t) / k for k in range(1, 7))
    return s * env(n, a, r)


def lowpass(x: np.ndarray, alpha: float) -> np.ndarray:
    y = np.empty_like(x)
    acc = 0.0
    for i, v in enumerate(x):
        acc += alpha * (v - acc)
        y[i] = acc
    return y


def marimba(f: float, dur: float) -> np.ndarray:
    n = int(dur * SR)
    t = np.arange(n) / SR
    s = np.sin(2 * np.pi * f * t) + 0.35 * np.sin(2 * np.pi * f * 4 * t) * np.exp(-t * 30)
    return s * env(n, 0.002, 0.16)


def celesta(f: float, dur: float) -> np.ndarray:
    n = int(dur * SR)
    t = np.arange(n) / SR
    s = np.sin(2 * np.pi * f * t) + 0.3 * np.sin(2 * np.pi * f * 2 * t) * np.exp(-t * 8) + 0.12 * np.sin(2 * np.pi * f * 5.4 * t) * np.exp(-t * 25)
    return s * env(n, 0.002, 0.5)


def musique(duree: float) -> np.ndarray:
    """Petite musique tendre : boîte à musique, nappe douce, basse ronde, pulsation légère."""
    n = int(duree * SR)
    out = np.zeros(n)
    beat = 60 / BPM
    # F - Dm - Bb - C (fa majeur, doux)
    accords = [[349.23, 440.0, 523.25], [293.66, 349.23, 440.0], [233.08, 293.66, 349.23], [261.63, 329.63, 392.0]]
    basses = [87.31, 73.42, 58.27, 65.41]
    melodie = [[2, 1, 0, 1, 2, 2, 2, -1], [1, 1, 1, -1, 2, 0, 0, -1], [0, 1, 2, 1, 0, 1, 2, -1], [2, 1, 2, 0, 1, -1, 1, -1]]
    mesure = 4 * beat

    def add(x, t0):
        i = int(t0 * SR)
        seg = out[i:i + len(x)]
        seg += x[:len(seg)]

    for m in range(int(duree / mesure) + 1):
        t0 = m * mesure
        ac, ba = accords[m % 4], basses[m % 4]
        add(sum(note(f, mesure, "sine", a=0.6, r=3.5) for f in ac) * 0.05, t0)
        for b in range(4):
            tb = t0 + b * beat
            if b in (0, 2):
                k = note(55, 0.25, "sine", a=0.002, r=0.09) * 0.35
                add(k * np.linspace(1.3, 0.6, len(k)), tb)
            add(note(ba, beat * 0.95, "sine", a=0.02, r=0.4) * 0.22, tb)
            for q in range(2):
                sh = RNG.standard_normal(int(0.04 * SR)) * env(int(0.04 * SR), 0.004, 0.012) * 0.025
                add(sh - lowpass(sh, 0.4), tb + (q + 0.5) * beat / 2)
        for e, deg in enumerate(melodie[m % 4]):
            if deg >= 0:
                add(celesta(ac[deg] * 2, beat * 1.2) * 0.13, t0 + e * beat / 2)
    fondu = int(1.2 * SR)
    out[:fondu] *= np.linspace(0, 1, fondu)
    out[-int(2.0 * SR):] *= np.linspace(1, 0, int(2.0 * SR))
    return out / (np.abs(out).max() + 1e-9) * 0.7


def etincelle() -> np.ndarray:
    n = int(0.9 * SR)
    t = np.arange(n) / SR
    s = sum(np.sin(2 * np.pi * f * t) * np.exp(-t * (5 + i)) for i, f in enumerate([1568, 2093, 2637, 3136]))
    return s / 4 * 0.5


def whoosh() -> np.ndarray:
    n = int(0.45 * SR)
    bruit = RNG.standard_normal(n)
    t = np.linspace(0, 1, n)
    alpha = 0.02 + 0.35 * np.sin(np.pi * t) ** 2
    y, acc = np.empty(n), 0.0
    for i in range(n):
        acc += alpha[i] * (bruit[i] - acc)
        y[i] = acc
    y *= np.sin(np.pi * t) ** 1.5
    return y / np.abs(y).max() * 0.6


def pop() -> np.ndarray:
    n = int(0.12 * SR)
    t = np.arange(n) / SR
    f = 900 * np.exp(-t * 25) + 300
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.001, 0.03) * 0.5


def tick() -> np.ndarray:
    n = int(0.03 * SR)
    b = RNG.standard_normal(n) * env(n, 0.0005, 0.006)
    return (b - lowpass(b, 0.2)) * 0.5


def main() -> None:
    projet = Path(__file__).resolve().parent.parent
    meta_path = projet / "audio_meta.json"
    meta = json.loads(meta_path.read_text())
    total = sum(v["duration_s"] for v in meta["voices"]) + 2
    ecrire(projet / "assets/music/bed.wav", musique(total))
    ecrire(projet / "assets/sfx/whoosh.wav", whoosh())
    ecrire(projet / "assets/sfx/pop.wav", pop())
    ecrire(projet / "assets/sfx/tick.wav", tick())
    ecrire(projet / "assets/sfx/etincelle.wav", etincelle())
    meta["bgm"] = {"path": "assets/music/bed.wav", "source": "host", "volume": 0.2,
                   "duration_s": round(total, 2)}
    meta["sfx"] = [{"frame": v["frame"], "file": "assets/sfx/whoosh.wav", "offset_s": 0,
                    "duration_s": 0.45, "volume": 0.22, "source": "host"}
                   for v in meta["voices"] if v["frame"] > 1]
    # étincelle sur l'apparition du logo (« Sibabi » dans la frame 1)
    mots1 = next(v for v in meta["voices"] if v["frame"] == 1)["words"]
    t_logo = next(w["start"] for w in mots1 if w["text"].lower().startswith("taye"))
    meta["sfx"].append({"frame": 1, "file": "assets/sfx/etincelle.wav", "offset_s": round(t_logo - 0.05, 2),
                        "duration_s": 0.9, "volume": 0.35, "source": "host"})
    meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2))
    print(f"musique {total:.1f}s + {len(meta['sfx'])} whooshs → {meta_path}")


if __name__ == "__main__":
    main()
