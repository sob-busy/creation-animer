"""Génère compositions/frames/NN-*.html pour la pub « Taye — Vente de Trousseau Bébé ».

Chaque frame = un <template> autonome, timeline GSAP en pause sur window.__timelines[frame_id],
1080×1920, contenu au-dessus de y=1600. Apparitions calées sur les mots de la voix off.

    python3 scripts/generer_frames.py .
"""

from __future__ import annotations

import json
import math
import re
import sys
import unicodedata
from pathlib import Path

PROJ = Path(sys.argv[1]).resolve()
OUT = PROJ / "compositions" / "frames"
OUT.mkdir(parents=True, exist_ok=True)

SB = (PROJ / "STORYBOARD.md").read_text(encoding="utf-8")
DUR = {int(n): float(d) for n, d in re.findall(r"## Frame (\d+) —.*?- duration: ([\d.]+)s", SB, re.S)}
META = {v["frame"]: v for v in json.loads((PROJ / "audio_meta.json").read_text())["voices"]}

ROSE, ROSE_F, POUDRE, JAUNE, BLEU, PRUNE, VERT_WA = "#E2197A", "#B80F5E", "#FFE3EF", "#FFD54A", "#8EC5F0", "#4A1530", "#25B755"


def _norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", s.lower()).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9']", "", s)


def cue(n: int, mot: str, k: int = 0, avance: float = 0.08) -> float:
    cible = _norm(mot)
    hits = [w["start"] for w in META[n]["words"]
            if _norm(w["text"]).startswith(cible) or _norm(w["text"]).split("'")[-1].startswith(cible)]
    if len(hits) <= k:
        raise SystemExit(f"frame {n}: mot « {mot} » introuvable dans {[w['text'] for w in META[n]['words']]}")
    return round(max(0.0, hits[k] - avance), 3)


# ─────────────────────────────── briques visuelles ───────────────────────────────

def css_base(P: str) -> str:
    return f"""
@font-face {{ font-family: "Lilita One"; src: url("assets/fonts/LilitaOne-400.woff2") format("woff2"); }}
@font-face {{ font-family: "Kaushan Script"; src: url("assets/fonts/KaushanScript-400.woff2") format("woff2"); }}
@font-face {{ font-family: "Poppins"; src: url("assets/fonts/Poppins-400.woff2") format("woff2"); font-weight: 400; }}
@font-face {{ font-family: "Poppins"; src: url("assets/fonts/Poppins-600.woff2") format("woff2"); font-weight: 600; }}
@font-face {{ font-family: "Poppins"; src: url("assets/fonts/Poppins-800.woff2") format("woff2"); font-weight: 800; }}
#root {{ position: absolute; inset: 0; width: 1080px; height: 1920px; overflow: hidden; font-family: "Poppins", sans-serif; color: {PRUNE}; }}
#root * {{ box-sizing: border-box; }}
.{P}-abs {{ position: absolute; }}
.{P}-bg {{ position: absolute; inset: 0; }}
.{P}-rays {{ position: absolute; left: -460px; top: -300px; width: 2000px; height: 2000px; opacity: .5; }}
.{P}-float {{ position: absolute; }}
/* logo Taye */
.{P}-lw {{ position: absolute; width: 900px; height: 740px; transform-origin: 50% 50%; }}
.{P}-logo {{ position: absolute; inset: 0; }}
.{P}-txt {{ position: absolute; left: 0; right: 0; text-align: center; font-family: "Lilita One", sans-serif; line-height: 1; }}
.{P}-taye-b {{ top: 30px; font-size: 270px; color: #fff; -webkit-text-stroke: 30px #fff; text-shadow: 0 16px 0 #F7B6D2, 0 24px 34px rgba(184,15,94,.35); }}
.{P}-taye-f {{ top: 30px; font-size: 270px; background-image: linear-gradient(100deg, rgba(255,255,255,0) 40%, rgba(255,255,255,.9) 50%, rgba(255,255,255,0) 60%),
  linear-gradient(180deg, #FF6FB1 0%, #E2197A 55%, #B80F5E 100%); background-size: 300% 100%, 100% 100%; background-position: 120% 0, 0 0;
  -webkit-background-clip: text; background-clip: text; color: transparent; }}
.{P}-vente {{ position: absolute; left: 150px; top: 318px; width: 600px; height: 112px; border-radius: 60px; background: linear-gradient(180deg, #FFE27A, #FFC928);
  transform: rotate(-3deg); display: flex; align-items: center; justify-content: center; font-family: "Kaushan Script", cursive; font-size: 82px; color: {PRUNE};
  box-shadow: 0 10px 20px rgba(184,15,94,.2); }}
.{P}-trou {{ top: 440px; font-size: 158px; color: {ROSE}; -webkit-text-stroke: 22px #fff; paint-order: stroke fill; text-shadow: 0 12px 0 #F7B6D2; }}
.{P}-bebe {{ top: 590px; font-size: 158px; color: {ROSE}; -webkit-text-stroke: 22px #fff; paint-order: stroke fill; text-shadow: 0 12px 0 #F7B6D2; }}
/* pastilles et cartes */
.{P}-pill {{ position: absolute; display: flex; align-items: center; gap: 16px; padding: 16px 30px 16px 16px; border-radius: 9999px;
  background: #FFFFFF; color: {PRUNE}; font-weight: 600; font-size: 42px; box-shadow: 0 10px 24px rgba(184,15,94,.22); white-space: nowrap; }}
.{P}-count {{ position: absolute; left: 60px; top: 110px; padding: 8px 24px; border-radius: 9999px; background: #FFFFFF; color: {ROSE};
  font-family: "Lilita One", sans-serif; font-size: 42px; box-shadow: 0 6px 14px rgba(184,15,94,.2); }}
.{P}-t1 {{ position: absolute; left: 0; right: 0; text-align: center; font-family: "Kaushan Script", cursive; font-size: 80px; line-height: 1; color: {PRUNE}; }}
.{P}-t2 {{ position: absolute; left: 0; right: 0; text-align: center; font-family: "Lilita One", sans-serif; line-height: 1; color: {ROSE};
  -webkit-text-stroke: 20px #fff; paint-order: stroke fill; text-shadow: 0 12px 0 rgba(184,15,94,.35); }}
.{P}-card {{ position: absolute; background: #FFFFFF; padding: 14px; border-radius: 34px; box-shadow: 0 24px 50px rgba(184,15,94,.28); }}
.{P}-card img {{ display: block; width: 100%; height: 100%; object-fit: cover; border-radius: 24px; }}
.{P}-round {{ position: absolute; border-radius: 50%; overflow: hidden; border: 12px solid #FFFFFF; box-shadow: 0 0 0 8px {JAUNE}, 0 20px 40px rgba(184,15,94,.3); background: #fff; }}
.{P}-round img {{ width: 100%; height: 100%; object-fit: cover; transform: scale(1.18); }}
.{P}-halo {{ position: absolute; border-radius: 50%; background: radial-gradient(closest-side, rgba(255,255,255,.95), rgba(255,255,255,0)); }}
"""


def rays_svg(P: str, couleur: str = "#FFFFFF", n: int = 20) -> str:
    c = 1000
    w = []
    for i in range(n):
        a0 = 2 * math.pi * i / n
        a1 = a0 + math.pi / n * 0.8
        w.append(f"M{c} {c} L{c + 1400 * math.cos(a0):.0f} {c + 1400 * math.sin(a0):.0f} L{c + 1400 * math.cos(a1):.0f} {c + 1400 * math.sin(a1):.0f} Z")
    return (f'<svg id="{P}-rays" class="{P}-rays" viewBox="0 0 2000 2000"><defs><radialGradient id="{P}-rg">'
            f'<stop offset="0" stop-color="{couleur}" stop-opacity=".7"/><stop offset="1" stop-color="{couleur}" stop-opacity="0"/>'
            f'</radialGradient></defs><path d="{" ".join(w)}" fill="url(#{P}-rg)"/></svg>')


def crown_svg(w: int = 130) -> str:
    return (f'<svg width="{w}" height="{int(w * .8)}" viewBox="0 0 190 150"><path d="M14 120 L4 34 L52 74 L95 8 L138 74 L186 34 L176 120 Z" fill="#FFC928" stroke="#E0A000" stroke-width="8" stroke-linejoin="round"/>'
            '<rect x="14" y="116" width="162" height="26" rx="6" fill="#FFC928" stroke="#E0A000" stroke-width="8"/><circle cx="95" cy="88" r="12" fill="#E2197A"/></svg>')


def bow_svg(w: int = 170) -> str:
    return (f'<svg width="{w}" height="{int(w * .62)}" viewBox="0 0 170 105"><path d="M85 52 Q40 0 12 18 Q-4 52 12 86 Q40 104 85 52 Z" fill="#FF7DB8" stroke="#D81B72" stroke-width="5"/>'
            '<path d="M85 52 Q130 0 158 18 Q174 52 158 86 Q130 104 85 52 Z" fill="#FF7DB8" stroke="#D81B72" stroke-width="5"/>'
            '<rect x="70" y="36" width="30" height="34" rx="12" fill="#E2197A"/></svg>')


def coeur_svg(s: int = 60, c: str = ROSE) -> str:
    return (f'<svg width="{s}" height="{s}" viewBox="0 0 100 100"><path d="M50 88 L14 52 Q0 36 12 22 Q28 6 50 28 Q72 6 88 22 Q100 36 86 52 Z" fill="{c}"/></svg>')


def etoile_svg(s: int = 70, c: str = "#FFD54A") -> str:
    return (f'<svg width="{s}" height="{s}" viewBox="0 0 100 100"><path d="M50 0 Q56 44 100 50 Q56 56 50 100 Q44 56 0 50 Q44 44 50 0 Z" fill="{c}"/></svg>')


def bulle_svg(s: int = 110) -> str:
    return (f'<svg width="{s}" height="{s}" viewBox="0 0 100 100"><circle cx="50" cy="50" r="46" fill="rgba(255,255,255,.18)" stroke="rgba(255,255,255,.9)" stroke-width="3"/>'
            '<path d="M24 38 Q30 22 46 18" stroke="#fff" stroke-width="6" fill="none" stroke-linecap="round"/></svg>')


def check_svg(c: str = ROSE) -> str:
    return (f'<svg width="54" height="54" viewBox="0 0 56 56"><circle cx="28" cy="28" r="28" fill="{c}"/>'
            '<path d="M15 29 L24 38 L41 19" fill="none" stroke="#fff" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/></svg>')


def wa_svg(s: int = 120) -> str:
    """Icône générique « message + téléphone » (pas le logo officiel)."""
    return (f'<svg width="{s}" height="{s}" viewBox="0 0 100 100"><circle cx="50" cy="50" r="48" fill="#fff"/>'
            f'<path d="M50 14 A36 36 0 1 1 26 78 L12 88 L18 70 A36 36 0 0 1 50 14 Z" fill="{VERT_WA}"/>'
            '<path d="M38 30 L46 42 L41 47 Q45 56 53 60 L58 55 L70 62 L66 70 Q60 75 50 71 Q34 63 30 46 Q29 38 33 34 Z" fill="#fff"/></svg>')


def pill(P, ident, x, y, txt, c=ROSE):
    return f'<div id="{ident}" class="{P}-pill" style="left:{x}px;top:{y}px">{check_svg(c)}<span>{txt}</span></div>'


def logo(P: str, ident: str, x: int, y: int, scale: float = 1.0) -> str:
    """Logo recréé : couronne + « Taye » + bandeau « Vente de » + « Trousseau Bébé » + nœud et cœurs."""
    return (f'<div class="{P}-lw" style="left:{x}px;top:{y}px;transform:scale({scale})"><div id="{ident}" class="{P}-logo">'
            f'<div class="{P}-txt {P}-taye-b">Taye</div><div id="{ident}-f" class="{P}-txt {P}-taye-f">Taye</div>'
            f'<div class="{P}-abs" style="left:185px;top:-20px;transform:rotate(-18deg)">{crown_svg(120)}</div>'
            f'<div class="{P}-abs" style="left:690px;top:-10px;transform:rotate(12deg)">{bow_svg(160)}</div>'
            f'<div class="{P}-vente">Vente de</div>'
            f'<div class="{P}-txt {P}-trou">Trousseau</div><div class="{P}-txt {P}-bebe">Bébé</div>'
            f'<div class="{P}-abs" style="left:120px;top:640px">{coeur_svg(56)}</div><div class="{P}-abs" style="left:725px;top:640px">{coeur_svg(56)}</div>'
            f'</div></div>')


def burst_svg(P, ident, cx, cy, r=170, c="#FFFFFF"):
    pts = []
    for i in range(14):
        a = i * 2 * math.pi / 14
        pts.append(f'<g transform="translate({cx + r * math.cos(a):.0f} {cy + r * math.sin(a):.0f}) scale({.5 + (i % 3) * .25})">'
                   f'<path d="M0 -26 Q4 -4 26 0 Q4 4 0 26 Q-4 4 -26 0 Q-4 -4 0 -26 Z" fill="{c if i % 2 else JAUNE}"/></g>')
    return f'<svg id="{ident}" width="1080" height="1920" class="{P}-abs" style="left:0;top:0;overflow:visible;opacity:0">{"".join(pts)}</svg>'


def floaters(P: str, items: list, d: float) -> tuple[str, str]:
    html, js = [], []
    for i, (svg, x, y, prof) in enumerate(items):
        fid = f"{P}-fl{i}"
        flou = 0 if prof > .7 else (2 if prof > .4 else 4)
        html.append(f'<div id="{fid}" class="{P}-float" style="left:{x}px;top:{y}px;filter:blur({flou}px);opacity:0">{svg}</div>')
        dy = -(50 + 40 * prof) * (1 if i % 2 else 0.7)
        dx = (-1) ** i * (16 + 10 * (i % 3))
        rot = (-1) ** (i + 1) * (10 + 6 * (i % 4))
        js.append(f'tl.fromTo("#{fid}", {{opacity: 0, scale: 0.5}}, {{opacity: {0.6 + 0.4 * prof:.2f}, scale: 1, duration: 0.8, ease: "back.out(1.6)"}}, {0.05 * i:.2f});')
        js.append(f'tl.fromTo("#{fid}", {{x: 0, y: 0, rotation: 0}}, {{x: {dx}, y: {dy:.0f}, rotation: {rot}, duration: {d:.3f}, ease: "sine.inOut", immediateRender: false}}, 0);')
    return "\n".join(html), "\n".join(js)


def amb(i: int) -> list:
    """Jeux d'objets flottants (cœurs, étoiles, bulles, ourson) qui varient selon la frame."""
    sets = [
        [(coeur_svg(80), 70, 230, .6), (etoile_svg(70), 930, 210, .7), (bulle_svg(130), 880, 1180, .4), (coeur_svg(54, "#FFFFFF"), 60, 1150, .3),
         (etoile_svg(50, "#FFFFFF"), 500, 1530, .3), (bulle_svg(90), 40, 1480, .2)],
        [(etoile_svg(80), 60, 260, .6), (coeur_svg(70), 920, 300, .6), (bulle_svg(120), 50, 1250, .4), (coeur_svg(60, "#FFFFFF"), 930, 1250, .3),
         (etoile_svg(46, "#FFFFFF"), 520, 1540, .3), (bulle_svg(80), 960, 1500, .2)],
    ]
    return sets[i % 2]


JS_HELPERS = """
const R = document.querySelector('[data-composition-id="__F__"]');
const q = (s) => R.querySelector(s);
const qa = (s) => Array.from(R.querySelectorAll(s));
function popIn(sel, at, from, to) {
  tl.fromTo(q(sel), Object.assign({ opacity: 0, scale: 0.6, y: 40 }, from || {}),
    Object.assign({ opacity: 1, scale: 1, y: 0, duration: 0.7, ease: "back.out(1.5)" }, to || {}), at);
}
function slideIn(sel, at, dx, dy, rot) {
  tl.fromTo(q(sel), { opacity: 0, x: dx || 0, y: dy || 0, rotation: (rot || 0) + 10 }, { opacity: 1, x: 0, y: 0, rotation: rot || 0, duration: 0.8, ease: "power3.out" }, at);
}
function levitate(sel, at, end, amp) {
  tl.fromTo(q(sel), { y: 0 }, { y: -(amp || 14), duration: Math.max(0.3, end - at), ease: "sine.inOut", immediateRender: false }, at);
}
function shine(sel, at) {
  tl.fromTo(q(sel), { backgroundPosition: "120% 0, 0 0" }, { backgroundPosition: "-20% 0, 0 0", duration: 1.1, ease: "power2.inOut", immediateRender: false }, at);
}
function burst(sel, at) {
  tl.fromTo(q(sel), { opacity: 0, scale: 0.4, transformOrigin: "50% 50%" }, { opacity: 1, scale: 1, duration: 0.3, ease: "power2.out", immediateRender: false }, at);
  tl.to(q(sel), { opacity: 0, scale: 1.3, duration: 0.5, ease: "power2.in" }, at + 0.3);
}
"""


def write_frame(n, slug, bg_css, body, css, js, flot, rays="#FFFFFF"):
    f = f"{n:02d}-{slug}"
    P = "f" + f
    d = DUR[n]
    fl_html, fl_js = floaters(P, flot, d)
    rep = lambda s: s.replace("__F__", P)
    rays_html = rays_svg(P, rays) if rays else ""
    rays_js = (f'tl.fromTo("#{P}-rays", {{rotation: 0, svgOrigin: "1000 1000"}}, {{rotation: 24, svgOrigin: "1000 1000", duration: {d:.3f}, ease: "none"}}, 0);' if rays else "")
    html = f"""<template>
<script src="assets/vendor/gsap.min.js"></script>
<style>{css_base(P)}
#{P}-bg {{ {bg_css} }}
{rep(css)}
</style>
<div id="root" data-composition-id="{f}" data-width="1080" data-height="1920" data-duration="{d}">
  <div id="{P}-bg" class="{P}-bg clip" data-start="0" data-duration="{d}" data-track-index="0"></div>
  <div id="{P}-amb" class="clip" data-start="0" data-duration="{d}" data-track-index="1" style="position:absolute;inset:0">
{rays_html}
{fl_html}
  </div>
  <div id="{P}-stage" class="clip" data-start="0" data-duration="{d}" data-track-index="2" style="position:absolute;inset:0">
{rep(body)}
  </div>
</div>
<script>
(function () {{
window.__timelines = window.__timelines || {{}};
const tl = gsap.timeline({{ paused: true }});
{JS_HELPERS.replace("__F__", f)}
{rays_js}
{fl_js}
{rep(js)}
tl.set({{}}, {{}}, {d});
window.__timelines["{f}"] = tl;
}})();
</script>
</template>
"""
    (OUT / f"{f}.html").write_text(html, encoding="utf-8")
    print("écrit", f, d)


def radial(c1, c2):
    return f"background: radial-gradient(1200px 1400px at 50% 38%, {c1} 0%, {c2} 78%);"


# ─────────────────────────────── Frame 1 — logo flottant + numéro ───────────────────────────────
def frame1():
    n = 1
    t_bebe, t_tres, t_taye = cue(n, "bebe"), cue(n, "tresor"), cue(n, "taye")
    body = f"""
<div id="__F__-halo" class="__F__-halo" style="left:90px;top:300px;width:900px;height:900px"></div>
{logo("__F__", "__F__-logo", 90, 300, 1.0)}
<div id="__F__-ours" class="__F__-abs" style="left:770px;top:880px"><img src="assets/ourson.png" alt="" style="width:260px;height:auto"></div>
{burst_svg("__F__", "__F__-b1", 540, 670, 430)}
<div id="__F__-num" class="__F__-abs __F__-num">{wa_svg(110)}<span>+228 93 17 05 34</span></div>
"""
    css = """
.__F__-num { left: 70px; width: 940px; top: 1200px; height: 170px; border-radius: 9999px; background: linear-gradient(180deg, #3AD06D, #1E9A47);
  border: 8px solid #fff; display: flex; align-items: center; justify-content: center; gap: 24px; box-shadow: 0 20px 40px rgba(30,154,71,.35); }
.__F__-num span { font-family: "Lilita One"; font-size: 96px; color: #fff; text-shadow: 0 6px 0 rgba(10,80,30,.4); }
"""
    js = f"""
tl.fromTo("#__F__-halo", {{ opacity: 0, scale: 0.3 }}, {{ opacity: 1, scale: 1, duration: 1.0, ease: "power2.out" }}, 0.0);
popIn("#__F__-logo", 0.15, {{ scale: 0.2, rotation: -8 }}, {{ rotation: 0, duration: 1.0, ease: "back.out(1.3)" }});
burst("#__F__-b1", 0.6);
shine("#__F__-logo-f", 1.2);
levitate("#__F__-logo", 1.2, {DUR[n]}, 22);
tl.fromTo("#__F__-ours", {{ opacity: 0, x: 200, rotation: 30 }}, {{ opacity: 1, x: 0, rotation: -6, duration: 0.8, ease: "back.out(1.5)" }}, {t_bebe});
popIn("#__F__-num", {t_tres}, {{ scale: 0.3, y: 120 }});
levitate("#__F__-num", {t_tres + 0.8:.2f}, {DUR[n]}, 10);
burst("#__F__-b1", {t_taye});
shine("#__F__-logo-f", {t_taye + 0.1:.2f});
tl.fromTo("#__F__-logo", {{ scale: 1 }}, {{ keyframes: {{ scale: [1, 1.06, 1] }}, duration: 0.5, ease: "power2.out", immediateRender: false }}, {t_taye});
"""
    write_frame(n, "logo", radial("#FFF6FA", "#FFC2DC"), body, css, js, amb(0))


# ─────────────────────────────── Frame 2 — Taye ───────────────────────────────
def frame2():
    n = 2
    t_vente, t_hab, t_zero, t_bon = cue(n, "vente"), cue(n, "habiller"), cue(n, "zero"), cue(n, "bonheur")
    vigs = ["vignette-grenouillere-jaune.png", "vignette-ensembles.png", "vignette-chaussons.png", "vignette-serviettes.png"]
    row = "".join(f'<div id="__F__-v{i}" class="__F__-round" style="left:{70 + i * 245}px;top:1330px;width:200px;height:200px"><img src="assets/{v}" alt=""></div>' for i, v in enumerate(vigs))
    body = f"""
<div id="__F__-t1" class="__F__-t1" style="top:110px">Vente de</div>
<div id="__F__-t2" class="__F__-t2" style="top:200px;font-size:140px">Trousseau Bébé</div>
<div id="__F__-ph" class="__F__-round" style="left:240px;top:420px;width:600px;height:600px"><img src="assets/portrait-taye.png" alt="" style="transform:none;object-position:50% 20%"></div>
<div id="__F__-name" class="__F__-abs __F__-name">Taye</div>
<div id="__F__-age" class="__F__-abs __F__-age"><b>0 à 24</b><span>mois</span></div>
<div id="__F__-slo" class="__F__-abs __F__-slo">Le bonheur de votre bébé commence ici ! {coeur_svg(50)}</div>
{row}
"""
    css = f"""
.__F__-name {{ left: 390px; width: 300px; top: 960px; height: 100px; border-radius: 9999px; background: {ROSE}; border: 6px solid #fff; color: #fff;
  display: flex; align-items: center; justify-content: center; font-family: "Lilita One"; font-size: 70px; box-shadow: 0 12px 26px rgba(184,15,94,.3); }}
.__F__-age {{ left: 790px; top: 430px; width: 240px; height: 240px; border-radius: 50%; background: {JAUNE}; border: 8px solid #fff; display: flex; flex-direction: column;
  align-items: center; justify-content: center; font-family: "Lilita One"; color: {PRUNE}; box-shadow: 0 14px 30px rgba(184,15,94,.3); }}
.__F__-age b {{ font-weight: 400; font-size: 70px; line-height: 1; }} .__F__-age span {{ font-size: 44px; }}
.__F__-slo {{ left: 50px; width: 980px; top: 1110px; height: 140px; border-radius: 30px; background: #fff; display: flex; align-items: center; justify-content: center; gap: 12px;
  font-family: "Kaushan Script"; font-size: 54px; color: {PRUNE}; box-shadow: 0 14px 30px rgba(184,15,94,.22); }}
"""
    js = f"""
tl.fromTo("#__F__-ph", {{ opacity: 0, scale: 0.5 }}, {{ opacity: 1, scale: 1, duration: 0.9, ease: "back.out(1.3)" }}, 0.0);
popIn("#__F__-name", 0.4);
tl.fromTo("#__F__-t1", {{ opacity: 0, y: -40 }}, {{ opacity: 1, y: 0, duration: 0.6, ease: "power3.out" }}, {t_vente});
tl.fromTo("#__F__-t2", {{ opacity: 0, scale: 1.5, filter: "blur(10px)" }}, {{ opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.7, ease: "expo.out" }}, {t_vente + 0.4:.2f});
{"".join(f'popIn("#__F__-v{i}", {t_hab + i * 0.15:.2f}, {{ scale: 0.2, y: 80 }});' for i in range(4))}
popIn("#__F__-age", {t_zero}, {{ scale: 0.2, rotation: 40 }}, {{ rotation: 8 }});
tl.fromTo("#__F__-slo", {{ opacity: 0, scaleX: 0 }}, {{ opacity: 1, scaleX: 1, duration: 0.7, ease: "expo.out" }}, {t_bon});
levitate("#__F__-ph", 1.0, {DUR[n]}, 12);
"""
    write_frame(n, "taye", radial("#FFF6FA", "#FFC2DC"), body, css, js, amb(1))


# ─────────────────────────────── Frames 3–7 — articles ───────────────────────────────
def titre(nom: str) -> str:
    taille = min(190, int(1000 / (0.56 * len(nom))))
    return f'<div id="__F__-t1" class="__F__-t1" style="top:150px">Les</div><div id="__F__-t2" class="__F__-t2" style="top:230px;font-size:{taille}px">{nom}</div>'


def intro_js(t_nom: float) -> str:
    return f"""
tl.fromTo("#__F__-count", {{ opacity: 0, x: -60 }}, {{ opacity: 1, x: 0, duration: 0.5, ease: "power3.out" }}, 0.0);
tl.fromTo("#__F__-t1", {{ opacity: 0, y: -30 }}, {{ opacity: 1, y: 0, duration: 0.5, ease: "power3.out" }}, 0.05);
tl.fromTo("#__F__-t2", {{ opacity: 0, scale: 1.5, filter: "blur(10px)" }}, {{ opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.6, ease: "expo.out" }}, {t_nom});
"""


def frame3():
    n = 3
    t_nom, t_dou, t_our = cue(n, "grenouilleres"), cue(n, "douces"), cue(n, "ourson")
    body = f"""<div id="__F__-count" class="__F__-count">1/5</div>{titre("GRENOUILLÈRES")}
<div id="__F__-halo" class="__F__-halo" style="left:40px;top:430px;width:800px;height:900px"></div>
<div id="__F__-c1" class="__F__-card" style="left:100px;top:440px;width:620px;height:710px"><img src="assets/grenouillere-bleue.png" alt=""></div>
<div id="__F__-c2" class="__F__-round" style="left:700px;top:880px;width:330px;height:330px"><img src="assets/vignette-grenouillere-jaune.png" alt=""></div>
{burst_svg("__F__", "__F__-b", 410, 790, 380)}
{pill("__F__", "__F__-p0", 100, 1260, "Toutes douces")}
{pill("__F__", "__F__-p1", 330, 1390, "Motifs ourson", "#5AA9E6")}"""
    js = intro_js(t_nom) + f"""
slideIn("#__F__-c1", 0.15, -300, 80, -3);
burst("#__F__-b", 0.7);
levitate("#__F__-c1", 1.0, {DUR[n]}, 14);
popIn("#__F__-p0", {t_dou}, {{ x: -100 }}, {{ x: 0 }});
popIn("#__F__-c2", {t_our - 0.2:.2f}, {{ scale: 0.2, rotation: -30 }}, {{ rotation: 0 }});
popIn("#__F__-p1", {t_our}, {{ x: 100 }}, {{ x: 0 }});
"""
    write_frame(n, "grenouilleres", radial("#EAF5FF", "#9CCDF5"), body, "", js, amb(0))


def frame4():
    n = 4
    t_bod, t_ens, t_col, t_jour, t_occ = cue(n, "bodies"), cue(n, "ensembles"), cue(n, "colores"), cue(n, "jour"), cue(n, "occasion")
    body = f"""<div id="__F__-count" class="__F__-count">2/5</div>
<div id="__F__-t1" class="__F__-t1" style="top:150px">Les</div><div id="__F__-t2" class="__F__-t2" style="top:225px;font-size:125px">BODIES &amp;<br>ENSEMBLES</div>
<div id="__F__-c1" class="__F__-card" style="left:70px;top:530px;width:540px;height:540px"><img src="assets/pile-bodies.png" alt=""></div>
<div id="__F__-c2" class="__F__-card" style="left:600px;top:610px;width:420px;height:490px"><img src="assets/robe-rose.png" alt=""></div>
<div id="__F__-c3" class="__F__-round" style="left:670px;top:1150px;width:290px;height:290px"><img src="assets/vignette-ensembles.png" alt=""></div>
{pill("__F__", "__F__-p0", 70, 1140, "Colorés")}
{pill("__F__", "__F__-p1", 70, 1260, "Chaque jour")}
{pill("__F__", "__F__-p2", 70, 1380, "Chaque occasion")}"""
    css = "#__F__-t2 { line-height: .95; }"
    js = intro_js(t_bod) + f"""
slideIn("#__F__-c1", {max(0.1, t_bod - 0.1):.2f}, -300, 60, -4);
slideIn("#__F__-c2", {t_ens}, 300, 60, 5);
popIn("#__F__-c3", {t_ens + 0.4:.2f}, {{ scale: 0.2 }});
popIn("#__F__-p0", {t_col}, {{ x: -100 }}, {{ x: 0 }});
popIn("#__F__-p1", {t_jour}, {{ x: -100 }}, {{ x: 0 }});
popIn("#__F__-p2", {t_occ}, {{ x: -100 }}, {{ x: 0 }});
levitate("#__F__-c1", 1.2, {DUR[n]}, 10);
levitate("#__F__-c2", 1.6, {DUR[n]}, 14);
"""
    write_frame(n, "bodies", radial("#FFF3F8", "#FFB8D6"), body, css, js, amb(1))


def frame5():
    n = 5
    t_nom, t_lap, t_our, t_chaud = cue(n, "chaussons"), cue(n, "lapin"), cue(n, "ourson"), cue(n, "chaud")
    body = f"""<div id="__F__-count" class="__F__-count">3/5</div>{titre("CHAUSSONS")}
<div id="__F__-halo" class="__F__-halo" style="left:0;top:380px;width:1080px;height:700px"></div>
<div id="__F__-c1" class="__F__-card" style="left:80px;top:470px;width:920px;height:460px"><img src="assets/chaussons.png" alt=""></div>
<div id="__F__-c2" class="__F__-round" style="left:90px;top:990px;width:340px;height:340px"><img src="assets/vignette-chaussons.png" alt=""></div>
{burst_svg("__F__", "__F__-b", 540, 700, 470)}
{pill("__F__", "__F__-p0", 470, 1020, "Lapin")}
{pill("__F__", "__F__-p1", 470, 1140, "Ourson", "#5AA9E6")}
{pill("__F__", "__F__-p2", 470, 1260, "Pieds au chaud")}"""
    js = intro_js(t_nom) + f"""
tl.fromTo("#__F__-c1", {{ opacity: 0, scale: 0.4, rotation: -10 }}, {{ opacity: 1, scale: 1, rotation: -2, duration: 0.9, ease: "back.out(1.4)" }}, 0.2);
burst("#__F__-b", 0.8);
levitate("#__F__-c1", 1.1, {DUR[n]}, 12);
popIn("#__F__-p0", {t_lap}, {{ x: 100 }}, {{ x: 0 }});
popIn("#__F__-p1", {t_our}, {{ x: 100 }}, {{ x: 0 }});
popIn("#__F__-c2", {t_our + 0.15:.2f}, {{ scale: 0.2 }});
popIn("#__F__-p2", {t_chaud}, {{ x: 100 }}, {{ x: 0 }});
"""
    write_frame(n, "chaussons", radial("#F6F0FF", "#CDB8F2"), body, "", js, amb(0))


def frame6():
    n = 6
    t_nom, t_ado, t_ore = cue(n, "bonnets"), cue(n, "adorables"), cue(n, "oreilles")
    body = f"""<div id="__F__-count" class="__F__-count">4/5</div>{titre("BONNETS")}
<div id="__F__-halo" class="__F__-halo" style="left:140px;top:400px;width:800px;height:900px"></div>
<div id="__F__-c1" class="__F__-card" style="left:230px;top:450px;width:620px;height:660px"><img src="assets/bonnet.png" alt=""></div>
{burst_svg("__F__", "__F__-b", 540, 780, 400)}
{pill("__F__", "__F__-p0", 130, 1190, "Adorables")}
{pill("__F__", "__F__-p1", 470, 1310, "Petites oreilles")}"""
    js = intro_js(t_nom) + f"""
tl.fromTo("#__F__-c1", {{ opacity: 0, y: 500, rotation: 15 }}, {{ opacity: 1, y: 0, rotation: 3, duration: 0.9, ease: "back.out(1.3)" }}, 0.15);
burst("#__F__-b", 0.8);
levitate("#__F__-c1", 1.1, {DUR[n]}, 14);
popIn("#__F__-p0", {t_ado}, {{ x: -100 }}, {{ x: 0 }});
popIn("#__F__-p1", {t_ore}, {{ x: 100 }}, {{ x: 0 }});
"""
    write_frame(n, "bonnets", radial("#FFF5EE", "#FFC6B4"), body, "", js, amb(1))


def frame7():
    n = 7
    t_ser, t_bav, t_acc = cue(n, "serviettes"), cue(n, "bavoirs"), cue(n, "accessoires")
    body = f"""<div id="__F__-count" class="__F__-count">5/5</div>
<div id="__F__-t1" class="__F__-t1" style="top:150px">Et aussi</div><div id="__F__-t2" class="__F__-t2" style="top:230px;font-size:150px">ACCESSOIRES</div>
<div id="__F__-c1" class="__F__-card" style="left:60px;top:470px;width:440px;height:420px"><img src="assets/vignette-serviettes.png" alt=""></div>
<div id="__F__-c2" class="__F__-card" style="left:560px;top:540px;width:460px;height:360px"><img src="assets/bavoir.png" alt=""></div>
<div id="__F__-c3" class="__F__-card" style="left:330px;top:1030px;width:420px;height:400px"><img src="assets/pile-bodies.png" alt=""></div>
{pill("__F__", "__F__-p0", 90, 920, "Serviettes", "#3DBE8B")}
{pill("__F__", "__F__-p1", 640, 920, "Bavoirs")}
{pill("__F__", "__F__-p2", 330, 1460, "Accessoires", "#5AA9E6")}"""
    js = intro_js(max(0.2, t_acc - 0.9)) + f"""
slideIn("#__F__-c1", {max(0.1, t_ser - 0.3):.2f}, -300, 0, -4);
popIn("#__F__-p0", {t_ser}, {{ y: 40 }});
slideIn("#__F__-c2", {t_bav - 0.2:.2f}, 300, 0, 4);
popIn("#__F__-p1", {t_bav}, {{ y: 40 }});
slideIn("#__F__-c3", {t_acc - 0.2:.2f}, 0, 300, -2);
popIn("#__F__-p2", {t_acc + 0.1:.2f}, {{ y: 40 }});
levitate("#__F__-c1", 1.2, {DUR[n]}, 10);
"""
    write_frame(n, "accessoires", radial("#F0FFF8", "#A8E6CF"), body, "", js, amb(0))


# ─────────────────────────────── Frame 8 — qualités ───────────────────────────────
def frame8():
    n = 8
    t_q, t_c, t_p = cue(n, "qualite"), cue(n, "confort"), cue(n, "prix")
    photos = ["grenouillere-bleue.png", "robe-rose.png", "chaussons.png", "bonnet.png"]
    mos = "".join(f'<div class="__F__-card __F__-mos" style="left:{40 + (i % 2) * 520}px;top:{360 + (i // 2) * 560}px;width:480px;height:520px;transform:rotate({(-1) ** i * 4}deg)"><img src="assets/{p}" alt=""></div>' for i, p in enumerate(photos))
    tag = ('<svg width="70" height="70" viewBox="0 0 100 100"><path d="M10 50 L50 10 L90 10 L90 50 L50 90 Z" fill="#fff"/><circle cx="72" cy="28" r="8" fill="#E2197A"/></svg>')
    body = f"""
<div id="__F__-mos" class="__F__-abs" style="left:0;top:0;width:1080px;height:1600px">{mos}</div>
<div id="__F__-veil" class="__F__-abs" style="left:0;top:0;width:1080px;height:1920px;background:rgba(255,227,239,.72)"></div>
<div id="__F__-t1" class="__F__-t1" style="top:170px">Chez Taye, c'est</div>
<div id="__F__-q0" class="__F__-abs __F__-q" style="top:420px;background:{ROSE}">{etoile_svg(76, "#fff")}<span>Qualité</span></div>
<div id="__F__-q1" class="__F__-abs __F__-q" style="top:700px;background:#5AA9E6">{coeur_svg(76, "#fff")}<span>Confort</span></div>
<div id="__F__-q2" class="__F__-abs __F__-q" style="top:980px;background:#F5A623">{tag}<span>Prix abordables</span></div>
{burst_svg("__F__", "__F__-b", 540, 1100, 470)}
"""
    css = """
.__F__-mos img { filter: saturate(1.1); }
.__F__-q { left: 90px; width: 900px; height: 210px; border-radius: 9999px; border: 10px solid #fff; display: flex; align-items: center; justify-content: center; gap: 30px;
  box-shadow: 0 20px 40px rgba(184,15,94,.3); }
.__F__-q span { font-family: "Lilita One"; font-size: 110px; color: #fff; text-shadow: 0 8px 0 rgba(0,0,0,.15); }
"""
    js = f"""
tl.fromTo("#__F__-mos", {{ opacity: 0, scale: 1.15 }}, {{ opacity: 1, scale: 1, duration: 1.2, ease: "power2.out" }}, 0.0);
tl.fromTo("#__F__-t1", {{ opacity: 0, y: -30 }}, {{ opacity: 1, y: 0, duration: 0.6, ease: "power3.out" }}, 0.1);
popIn("#__F__-q0", {t_q}, {{ scale: 0.3, x: -200 }}, {{ x: 0 }});
popIn("#__F__-q1", {t_c}, {{ scale: 0.3, x: 200 }}, {{ x: 0 }});
popIn("#__F__-q2", {t_p}, {{ scale: 0.3, x: -200 }}, {{ x: 0 }});
burst("#__F__-b", {t_p + 0.3:.2f});
"""
    write_frame(n, "qualites", radial("#FFF6FA", "#FFC2DC"), body, css, js, amb(1), rays=None)


# ─────────────────────────────── Frame 9 — contact ───────────────────────────────
def frame9():
    n = 9
    t_con, t_wa, t_num, t_hab = cue(n, "contactez"), cue(n, "whatsapp"), cue(n, "+228"), cue(n, "habillez")
    body = f"""
<div id="__F__-ph" class="__F__-round" style="left:70px;top:150px;width:400px;height:400px"><img src="assets/portrait-taye.png" alt="" style="transform:none;object-position:50% 20%"></div>
{logo("__F__", "__F__-logo", 360, 40, 0.62)}
<div id="__F__-cm" class="__F__-abs __F__-cm">Contactez Taye</div>
<div id="__F__-wa" class="__F__-abs __F__-wa"><div id="__F__-wave" class="__F__-wave"></div>{wa_svg(140)}<div><small>WhatsApp</small><span>+228 93 17 05 34</span></div></div>
<div id="__F__-hab" class="__F__-abs __F__-hab">{coeur_svg(54)} Habillez votre bébé avec amour {coeur_svg(54)}</div>
<div id="__F__-ours" class="__F__-abs" style="left:780px;top:1290px"><img src="assets/ourson.png" alt="" style="width:240px;height:auto"></div>
{burst_svg("__F__", "__F__-b", 540, 900, 500)}
"""
    css = f"""
.__F__-cm {{ left: 0; right: 0; top: 650px; text-align: center; font-family: "Kaushan Script"; font-size: 96px; color: {ROSE}; }}
.__F__-wa {{ left: 50px; width: 980px; top: 790px; height: 250px; border-radius: 9999px; background: linear-gradient(180deg, #3AD06D, #1E9A47); border: 10px solid #fff;
  display: flex; align-items: center; justify-content: center; gap: 28px; box-shadow: 0 24px 50px rgba(30,154,71,.4); }}
.__F__-wa small {{ display: block; font-weight: 800; font-size: 40px; color: #FFFFFF; text-shadow: 0 3px 0 rgba(10,80,30,.45); }}
.__F__-wa span {{ display: block; font-family: "Lilita One"; font-size: 104px; line-height: 1; color: #fff; text-shadow: 0 6px 0 rgba(10,80,30,.35); }}
.__F__-wave {{ position: absolute; inset: -10px; border-radius: 9999px; border: 10px solid {VERT_WA}; opacity: 0; }}
.__F__-hab {{ left: 40px; width: 1000px; top: 1110px; height: 150px; border-radius: 30px; background: {JAUNE}; transform: rotate(-2deg); display: flex; align-items: center;
  justify-content: center; gap: 16px; font-family: "Kaushan Script"; font-size: 58px; color: {PRUNE}; box-shadow: 0 16px 30px rgba(184,15,94,.25); }}
"""
    nb = int(max(1, (DUR[n] - t_num - 0.6) // 1.0))
    js = f"""
popIn("#__F__-ph", 0.0, {{ scale: 0.3 }});
popIn("#__F__-logo", 0.2, {{ scale: 0.3 }});
shine("#__F__-logo-f", 0.9);
levitate("#__F__-logo", 1.0, {DUR[n]}, 12);
tl.fromTo("#__F__-cm", {{ opacity: 0, y: 40 }}, {{ opacity: 1, y: 0, duration: 0.6, ease: "power3.out" }}, {t_con});
popIn("#__F__-wa", {t_wa}, {{ scale: 0.3 }});
burst("#__F__-b", {t_num});
{"".join(f'tl.fromTo("#__F__-wave", {{ opacity: 0.9, scale: 1 }}, {{ opacity: 0, scale: 1.15, duration: 0.9, ease: "power2.out", immediateRender: false }}, {t_num + 0.3 + k:.2f});' for k in range(nb))}
tl.fromTo("#__F__-hab", {{ opacity: 0, scaleX: 0 }}, {{ opacity: 1, scaleX: 1, duration: 0.7, ease: "expo.out" }}, {t_hab});
tl.fromTo("#__F__-ours", {{ opacity: 0, x: 200, rotation: 30 }}, {{ opacity: 1, x: 0, rotation: -6, duration: 0.8, ease: "back.out(1.5)" }}, {t_hab + 0.3:.2f});
tl.to(R, {{ opacity: 0, duration: 0.4, ease: "power2.in" }}, {DUR[n] - 0.42:.3f});
"""
    write_frame(n, "contact", radial("#FFF6FA", "#FFC2DC"), body, css, js, amb(1))


for fn in (frame1, frame2, frame3, frame4, frame5, frame6, frame7, frame8, frame9):
    fn()
