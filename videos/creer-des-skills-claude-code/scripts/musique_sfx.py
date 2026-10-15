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
BPM = 112
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


def musique(duree: float) -> np.ndarray:
    n = int(duree * SR)
    out = np.zeros(n)
    beat = 60 / BPM
    # Am - F - C - G, une mesure (4 temps) par accord
    accords = [[220.0, 261.63, 329.63], [174.61, 220.0, 261.63],
               [196.0, 261.63, 329.63], [196.0, 246.94, 293.66]]
    basses = [110.0, 87.31, 130.81, 98.0]
    mesure = 4 * beat
    nb = int(duree / mesure) + 1
    for m in range(nb):
        t0 = int(m * mesure * SR)
        ac, ba = accords[m % 4], basses[m % 4]
        pad = sum(note(f, mesure, "saw", a=0.4, r=3.0) for f in ac) * 0.05
        seg = out[t0:t0 + len(pad)]
        seg += pad[:len(seg)]
        for b in range(4):
            tb = t0 + int(b * beat * SR)
            # grosse caisse
            k = note(55, 0.25, "sine", a=0.001, r=0.09) * 0.55
            k *= np.linspace(1.4, 0.6, len(k))
            seg = out[tb:tb + len(k)]
            seg += k[:len(seg)]
            # basse sur les croches
            for h in range(2):
                th = tb + int(h * beat / 2 * SR)
                bs = note(ba, beat / 2, "saw", a=0.005, r=0.12) * 0.09
                seg = out[th:th + len(bs)]
                seg += bs[:len(seg)]
            # arpège en doubles croches, doux
            for q in range(4):
                tq = tb + int(q * beat / 4 * SR)
                f = ac[(b * 4 + q) % 3] * 2
                pl = note(f, beat / 4, "sine", a=0.002, r=0.08) * 0.05
                seg = out[tq:tq + len(pl)]
                seg += pl[:len(seg)]
            # charleston à contretemps
            th = tb + int(beat / 2 * SR)
            hh = RNG.standard_normal(int(0.05 * SR)) * env(int(0.05 * SR), 0.001, 0.015) * 0.06
            hh -= lowpass(hh, 0.3)
            seg = out[th:th + len(hh)]
            seg += hh[:len(seg)]
    fondu = int(1.5 * SR)
    out[:fondu] *= np.linspace(0, 1, fondu)
    out[-fondu:] *= np.linspace(1, 0, fondu)
    return out / (np.abs(out).max() + 1e-9) * 0.7


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
    meta["bgm"] = {"path": "assets/music/bed.wav", "source": "host", "volume": 0.16,
                   "duration_s": round(total, 2)}
    meta["sfx"] = [{"frame": v["frame"], "file": "assets/sfx/whoosh.wav", "offset_s": 0,
                    "duration_s": 0.45, "volume": 0.3, "source": "host"}
                   for v in meta["voices"] if v["frame"] > 1]
    meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2))
    print(f"musique {total:.1f}s + {len(meta['sfx'])} whooshs → {meta_path}")


if __name__ == "__main__":
    main()
