"""Génère compositions/frames/NN-*.html pour la pub « Madame SIBABI ».

Chaque frame = un <template> autonome (styles + scripts dedans), timeline GSAP en pause
enregistrée sur window.__timelines[frame_id], 1080×1920, contenu au-dessus de y=1600.
Les apparitions sont calées sur les mots de la voix off (audio_meta.json).

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

VERT, VERT_F, JAUNE, ROUGE, CREME, BRUN = "#1F7A34", "#0E4A1E", "#FFD21F", "#D7192F", "#FFF8EC", "#2A160C"


def _norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", s.lower()).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9']", "", s)


def cue(n: int, mot: str, k: int = 0, avance: float = 0.08) -> float:
    """Instant (s) où la voix commence à dire `mot` (k-ième occurrence) dans la frame n."""
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
#root {{ position: absolute; inset: 0; width: 1080px; height: 1920px; overflow: hidden; font-family: "Poppins", sans-serif; color: {CREME}; }}
#root * {{ box-sizing: border-box; }}
.{P}-abs {{ position: absolute; }}
.{P}-bg {{ position: absolute; inset: 0; }}
.{P}-rays {{ position: absolute; left: -460px; top: -260px; width: 2000px; height: 2000px; opacity: .55; }}
.{P}-float {{ position: absolute; }}
/* logo */
.{P}-logo {{ position: absolute; width: 900px; height: 380px; }}
.{P}-madame {{ position: absolute; left: 70px; top: 0; font-family: "Kaushan Script", cursive; font-size: 128px; line-height: 1; color: #FFFFFF;
  -webkit-text-stroke: 16px {BRUN}; paint-order: stroke fill; text-shadow: 0 8px 0 rgba(42,22,12,.35); }}
.{P}-sib-back, .{P}-sib-front {{ position: absolute; left: 0; top: 118px; font-family: "Lilita One", sans-serif; font-size: 236px; line-height: 1; letter-spacing: .01em; }}
.{P}-sib-back {{ color: {BRUN}; -webkit-text-stroke: 30px {BRUN}; text-shadow: 0 16px 0 #5A2F14, 0 22px 30px rgba(0,0,0,.35); }}
.{P}-sib-front {{ background-image: linear-gradient(100deg, rgba(255,255,255,0) 40%, rgba(255,255,255,.95) 50%, rgba(255,255,255,0) 60%),
  linear-gradient(180deg, #FFF59A 0%, #FFE03A 38%, #FFC107 62%, #F59E00 100%);
  background-size: 300% 100%, 100% 100%; background-position: 120% 0, 0 0; -webkit-background-clip: text; background-clip: text; color: transparent; }}
.{P}-crown {{ position: absolute; left: 640px; top: -40px; width: 190px; height: 150px; }}
/* pastilles */
.{P}-pill {{ position: absolute; display: flex; align-items: center; gap: 18px; padding: 18px 30px 18px 18px; border-radius: 9999px;
  background: #FFFFFF; color: {BRUN}; font-weight: 600; font-size: 44px; box-shadow: 0 10px 24px rgba(0,0,0,.22); white-space: nowrap; }}
.{P}-pill svg {{ flex: 0 0 auto; }}
.{P}-title1 {{ position: absolute; left: 0; right: 0; text-align: center; font-family: "Kaushan Script", cursive; font-size: 92px; line-height: 1;
  color: #FFFFFF; -webkit-text-stroke: 10px {BRUN}; paint-order: stroke fill; }}
.{P}-title2 {{ position: absolute; left: 0; right: 0; text-align: center; font-family: "Lilita One", sans-serif; font-size: 200px; line-height: 1;
  color: #FFFFFF; -webkit-text-stroke: 22px {BRUN}; paint-order: stroke fill; text-shadow: 0 14px 0 rgba(42,22,12,.45); }}
.{P}-count {{ position: absolute; left: 60px; top: 120px; padding: 10px 26px; border-radius: 9999px; background: rgba(255,255,255,.92); color: {BRUN};
  font-family: "Lilita One", sans-serif; font-size: 44px; }}
.{P}-photo {{ position: absolute; background: #FFFFFF; padding: 14px 14px 58px; border-radius: 22px; box-shadow: 0 18px 40px rgba(0,0,0,.35); }}
.{P}-photo img {{ display: block; width: 100%; height: 100%; object-fit: cover; border-radius: 12px; }}
.{P}-photo span {{ position: absolute; left: 0; right: 0; bottom: 10px; text-align: center; font-weight: 600; font-size: 28px; color: {BRUN}; }}
.{P}-badge {{ position: absolute; border-radius: 50%; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center;
  font-family: "Lilita One", sans-serif; line-height: .95; box-shadow: 0 12px 30px rgba(0,0,0,.3); }}
"""


def rays_svg(P: str, couleur: str = "#FFE680", n: int = 18) -> str:
    c = 1000
    wedges = []
    for i in range(n):
        a0 = 2 * math.pi * i / n
        a1 = a0 + math.pi / n * 0.8
        wedges.append(f"M{c} {c} L{c + 1400 * math.cos(a0):.0f} {c + 1400 * math.sin(a0):.0f} "
                      f"L{c + 1400 * math.cos(a1):.0f} {c + 1400 * math.sin(a1):.0f} Z")
    return (f'<svg id="{P}-rays" class="{P}-rays" viewBox="0 0 2000 2000"><defs><radialGradient id="{P}-rg">'
            f'<stop offset="0" stop-color="{couleur}" stop-opacity=".55"/><stop offset="1" stop-color="{couleur}" stop-opacity="0"/>'
            f'</radialGradient></defs><path d="{" ".join(wedges)}" fill="url(#{P}-rg)"/></svg>')


def crown_svg(P: str) -> str:
    return (f'<svg class="{P}-crown" viewBox="0 0 190 150"><defs><linearGradient id="{P}-cg" x1="0" y1="0" x2="0" y2="1">'
            '<stop offset="0" stop-color="#FFF3A0"/><stop offset=".5" stop-color="#FFC81E"/><stop offset="1" stop-color="#D98E00"/></linearGradient></defs>'
            f'<path d="M14 120 L4 34 L52 74 L95 8 L138 74 L186 34 L176 120 Z" fill="url(#{P}-cg)" stroke="{BRUN}" stroke-width="8" stroke-linejoin="round"/>'
            f'<rect x="14" y="116" width="162" height="26" rx="6" fill="url(#{P}-cg)" stroke="{BRUN}" stroke-width="8"/>'
            f'<circle cx="95" cy="88" r="12" fill="{ROUGE}"/><circle cx="50" cy="96" r="8" fill="#2EA3F2"/><circle cx="140" cy="96" r="8" fill="#2EA3F2"/>'
            f'<circle cx="4" cy="34" r="9" fill="#FFF3A0" stroke="{BRUN}" stroke-width="5"/><circle cx="95" cy="8" r="9" fill="#FFF3A0" stroke="{BRUN}" stroke-width="5"/>'
            f'<circle cx="186" cy="34" r="9" fill="#FFF3A0" stroke="{BRUN}" stroke-width="5"/></svg>')


def logo(P: str, ident: str, x: int, y: int, scale: float = 1.0) -> str:
    return (f'<div id="{ident}" class="{P}-logo" style="left:{x}px;top:{y}px;transform-origin:50% 50%;scale:{scale}">'
            f'<div class="{P}-madame">Madame</div><div class="{P}-sib-back">SIBABI</div>'
            f'<div id="{ident}-front" class="{P}-sib-front">SIBABI</div>{crown_svg(P)}</div>')


def check_svg(couleur: str = VERT) -> str:
    return (f'<svg width="56" height="56" viewBox="0 0 56 56"><circle cx="28" cy="28" r="28" fill="{couleur}"/>'
            '<path d="M15 29 L24 38 L41 19" fill="none" stroke="#fff" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/></svg>')


def pill(P: str, ident: str, x: int, y: int, texte: str, couleur: str = VERT) -> str:
    return f'<div id="{ident}" class="{P}-pill" style="left:{x}px;top:{y}px">{check_svg(couleur)}<span>{texte}</span></div>'


def glass_svg(P: str, ident: str, haut: str, bas: str, paille: str, w: int = 460) -> str:
    """Gobelet à couvercle dôme : liquide (remplissage animé), glaçons, bulles, paille, reflet."""
    h = int(w * 1.75)
    cup = "M40 160 L360 160 L312 640 Q304 660 280 660 L120 660 Q96 660 88 640 Z"
    bubbles = "".join(f'<circle class="{ident}-bub" cx="{110 + (i * 37) % 190}" cy="{600 - (i * 23) % 80}" r="{5 + i % 4}" fill="#fff" fill-opacity=".55"/>' for i in range(10))
    ice = "".join(f'<rect class="{ident}-ice" x="{x}" y="{y}" width="78" height="70" rx="16" fill="#fff" fill-opacity=".38" stroke="#fff" stroke-opacity=".7" stroke-width="3" transform="rotate({r} {x + 39} {y + 35})"/>'
                  for x, y, r in ((95, 200, -14), (200, 230, 12), (140, 300, 26)))
    return f'''<svg id="{ident}" width="{w}" height="{h}" viewBox="0 -40 400 720" style="overflow:visible">
<defs><clipPath id="{ident}-clip"><path d="{cup}"/></clipPath>
<linearGradient id="{ident}-lq" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{haut}"/><stop offset="1" stop-color="{bas}"/></linearGradient></defs>
<ellipse cx="200" cy="676" rx="190" ry="26" fill="rgba(0,0,0,.25)"/>
<g clip-path="url(#{ident}-clip)">
  <path d="{cup}" fill="rgba(255,255,255,.18)"/>
  <g id="{ident}-liq"><rect x="0" y="150" width="400" height="520" fill="url(#{ident}-lq)"/>
  <path d="M0 150 Q100 130 200 150 T400 150 L400 175 L0 175 Z" fill="#fff" fill-opacity=".28"/>{ice}{bubbles}</g>
</g>
<g id="{ident}-straw"><rect x="228" y="-60" width="30" height="640" rx="15" fill="{paille}" transform="rotate(9 243 260)"/>
<rect x="228" y="-60" width="10" height="640" rx="5" fill="#fff" fill-opacity=".45" transform="rotate(9 243 260)"/></g>
<path d="{cup}" fill="none" stroke="#fff" stroke-opacity=".85" stroke-width="7"/>
<path d="M70 200 L108 610" stroke="#fff" stroke-opacity=".55" stroke-width="16" stroke-linecap="round"/>
<path d="M26 160 Q200 30 374 160 Z" fill="rgba(255,255,255,.22)" stroke="#fff" stroke-opacity=".85" stroke-width="7"/>
<rect x="18" y="148" width="364" height="26" rx="13" fill="rgba(255,255,255,.75)"/>
</svg>'''


def citron_svg(s: int = 150) -> str:
    seg = "".join(f'<path d="M50 50 L{50 + 34 * math.cos(a):.1f} {50 + 34 * math.sin(a):.1f} A34 34 0 0 1 {50 + 34 * math.cos(a + 0.9):.1f} {50 + 34 * math.sin(a + 0.9):.1f} Z" fill="#F7F59A"/>'
                  for a in [i * 2 * math.pi / 7 for i in range(7)])
    return (f'<svg width="{s}" height="{s}" viewBox="0 0 100 100"><circle cx="50" cy="50" r="48" fill="#C8DC2B"/>'
            f'<circle cx="50" cy="50" r="41" fill="#FFFBD0"/>{seg}<circle cx="50" cy="50" r="5" fill="#FFFBD0"/></svg>')


def hibiscus_svg(s: int = 170) -> str:
    pet = "".join(f'<ellipse cx="50" cy="26" rx="20" ry="26" fill="#E3173E" stroke="#A30D2B" stroke-width="2" transform="rotate({a} 50 50)"/>' for a in range(0, 360, 72))
    return (f'<svg width="{s}" height="{s}" viewBox="0 0 100 100">{pet}<circle cx="50" cy="50" r="12" fill="#7A0A22"/>'
            '<path d="M50 50 L72 22" stroke="#FFD21F" stroke-width="3"/><circle cx="73" cy="20" r="4" fill="#FFD21F"/></svg>')


def ananas_svg(s: int = 160) -> str:
    return (f'<svg width="{s}" height="{s}" viewBox="0 0 100 100"><path d="M50 4 L42 30 L50 22 L58 30 Z M50 10 L34 28 L50 26 Z M50 10 L66 28 L50 26 Z" fill="#3E9B3A"/>'
            '<ellipse cx="50" cy="62" rx="28" ry="34" fill="#F6B21B" stroke="#C87F0A" stroke-width="3"/>'
            '<path d="M28 48 L72 84 M28 64 L60 92 M36 34 L74 66 M72 48 L28 84 M72 64 L40 92 M64 34 L26 66" stroke="#C87F0A" stroke-width="2.5"/></svg>')


def tamarin_svg(s: int = 180) -> str:
    return (f'<svg width="{s}" height="{int(s * .45)}" viewBox="0 0 100 45"><path d="M6 24 Q10 8 24 14 Q34 4 46 14 Q58 4 70 14 Q84 6 94 22 Q90 38 76 32 Q64 42 52 32 Q40 42 28 32 Q14 40 6 24 Z" '
            'fill="#9A6A3C" stroke="#5E3A1A" stroke-width="3"/><path d="M20 22 Q50 16 84 22" stroke="#C9965E" stroke-width="3" fill="none"/></svg>')


def glacon_svg(s: int = 90) -> str:
    return (f'<svg width="{s}" height="{s}" viewBox="0 0 100 100"><rect x="10" y="10" width="80" height="80" rx="18" fill="#E8F7FF" fill-opacity=".75" stroke="#fff" stroke-width="4"/>'
            '<path d="M24 30 L44 24" stroke="#fff" stroke-width="7" stroke-linecap="round"/></svg>')


def feuille_svg(s: int = 120) -> str:
    return (f'<svg width="{s}" height="{s}" viewBox="0 0 100 100"><path d="M10 90 Q10 20 90 10 Q84 84 10 90 Z" fill="#3FA845" stroke="#1F6B2A" stroke-width="3"/>'
            '<path d="M14 86 Q46 48 84 16" stroke="#1F6B2A" stroke-width="3" fill="none"/></svg>')


def tomate_svg(s: int = 130) -> str:
    return (f'<svg width="{s}" height="{s}" viewBox="0 0 100 100"><circle cx="50" cy="50" r="46" fill="#E2302A"/><circle cx="50" cy="50" r="38" fill="#F25C4E"/>'
            '<g fill="#FFE2A8"><ellipse cx="34" cy="40" rx="7" ry="11"/><ellipse cx="66" cy="40" rx="7" ry="11"/><ellipse cx="50" cy="68" rx="11" ry="7"/></g></svg>')


def concombre_svg(s: int = 120) -> str:
    return (f'<svg width="{s}" height="{s}" viewBox="0 0 100 100"><circle cx="50" cy="50" r="46" fill="#2F7D32"/><circle cx="50" cy="50" r="39" fill="#D9F2B4"/>'
            '<g fill="#F7FCEB">' + "".join(f'<ellipse cx="{50 + 16 * math.cos(a):.1f}" cy="{50 + 16 * math.sin(a):.1f}" rx="5" ry="3"/>' for a in [i * math.pi / 3 for i in range(6)]) + '</g></svg>')


def phone_svg(s: int = 90, couleur: str = "#fff") -> str:
    return (f'<svg width="{s}" height="{s}" viewBox="0 0 100 100"><path d="M30 10 L44 34 L34 44 Q42 62 58 68 L68 58 L90 72 L82 88 Q74 96 60 92 Q22 80 10 40 Q6 26 14 18 Z" fill="{couleur}"/></svg>')


def pin_svg(s: int = 140) -> str:
    return (f'<svg width="{s}" height="{int(s * 1.3)}" viewBox="0 0 100 130"><path d="M50 126 Q14 78 10 48 A40 40 0 1 1 90 48 Q86 78 50 126 Z" fill="{ROUGE}" stroke="#fff" stroke-width="6"/>'
            '<circle cx="50" cy="46" r="16" fill="#fff"/></svg>')


def coeur_svg(s: int = 60, couleur: str = ROUGE) -> str:
    return (f'<svg width="{s}" height="{s}" viewBox="0 0 100 100"><path d="M50 88 L14 52 Q0 36 12 22 Q28 6 50 28 Q72 6 88 22 Q100 36 86 52 Z" fill="{couleur}"/></svg>')


def burst_svg(P: str, ident: str, cx: int, cy: int, r: int = 170, couleur: str = "#FFE680") -> str:
    lines = "".join(f'<line x1="{cx + r * 0.45 * math.cos(a):.0f}" y1="{cy + r * 0.45 * math.sin(a):.0f}" x2="{cx + r * math.cos(a):.0f}" y2="{cy + r * math.sin(a):.0f}" '
                    f'stroke="{couleur}" stroke-width="10" stroke-linecap="round"/>' for a in [i * 2 * math.pi / 12 for i in range(12)])
    return f'<svg id="{ident}" width="1080" height="1920" class="{P}-abs" style="left:0;top:0;overflow:visible;opacity:0">{lines}</svg>'


def floaters(P: str, items: list[tuple[str, int, int, float]], d: float) -> tuple[str, str]:
    """Objets flottants d'arrière-plan : (svg, x, y, profondeur 0..1)."""
    html, js = [], []
    for i, (svg, x, y, prof) in enumerate(items):
        fid = f"{P}-fl{i}"
        flou = 0 if prof > .7 else (2 if prof > .4 else 5)
        html.append(f'<div id="{fid}" class="{P}-float" style="left:{x}px;top:{y}px;filter:blur({flou}px);opacity:0">{svg}</div>')
        dy = -(40 + 30 * prof) * (1 if i % 2 else 0.7)
        dx = (-1) ** i * (14 + 10 * (i % 3))
        rot = (-1) ** (i + 1) * (12 + 6 * (i % 4))
        js.append(f'tl.fromTo("#{fid}", {{opacity: 0, scale: 0.6}}, {{opacity: {0.55 + 0.4 * prof:.2f}, scale: 1, duration: 0.8, ease: "power3.out"}}, {0.06 * i:.2f});')
        js.append(f'tl.fromTo("#{fid}", {{x: 0, y: 0, rotation: 0}}, {{x: {dx}, y: {dy:.0f}, rotation: {rot}, duration: {d:.3f}, ease: "sine.inOut", immediateRender: false}}, 0);')
    return "\n".join(html), "\n".join(js)


JS_HELPERS = """
const R = document.querySelector('[data-composition-id="__F__"]');
const q = (s) => R.querySelector(s);
const qa = (s) => Array.from(R.querySelectorAll(s));
function popIn(sel, at, from, to) {
  tl.fromTo(q(sel), Object.assign({ opacity: 0, scale: 0.6, y: 40 }, from || {}),
    Object.assign({ opacity: 1, scale: 1, y: 0, duration: 0.7, ease: "back.out(1.6)" }, to || {}), at);
}
function slideIn(sel, at, dx, dy) {
  tl.fromTo(q(sel), { opacity: 0, x: dx || 0, y: dy || 0 }, { opacity: 1, x: 0, y: 0, duration: 0.7, ease: "power3.out" }, at);
}
function levitate(sel, at, end, amp) {
  tl.fromTo(q(sel), { y: 0 }, { y: -(amp || 14), duration: Math.max(0.3, end - at), ease: "sine.inOut", immediateRender: false }, at);
}
function shine(sel, at) {
  tl.fromTo(q(sel), { backgroundPosition: "120% 0, 0 0" }, { backgroundPosition: "-20% 0, 0 0", duration: 1.1, ease: "power2.inOut", immediateRender: false }, at);
}
function burst(sel, at) {
  tl.fromTo(q(sel), { opacity: 0, scale: 0.4, transformOrigin: "50% 50%" }, { opacity: 1, scale: 1, duration: 0.25, ease: "power2.out", immediateRender: false }, at);
  tl.to(q(sel), { opacity: 0, scale: 1.35, duration: 0.45, ease: "power2.in" }, at + 0.25);
}
function fillGlass(id, at, dur) {
  tl.fromTo(q("#" + id + "-liq"), { scaleY: 0, svgOrigin: "200 660" }, { scaleY: 1, svgOrigin: "200 660", duration: dur || 1.2, ease: "power2.out" }, at);
  tl.fromTo(qa("." + id + "-ice"), { y: -260, opacity: 0 }, { y: 0, opacity: 1, duration: 0.6, ease: "bounce.out", stagger: 0.12 }, at + 0.35);
  tl.fromTo(q("#" + id + "-straw"), { y: -300, opacity: 0 }, { y: 0, opacity: 1, duration: 0.6, ease: "power3.out" }, at + 0.8);
  tl.fromTo(qa("." + id + "-bub"), { y: 0, opacity: 0 }, { y: -380, opacity: 0.9, duration: 2.6, ease: "power1.in", stagger: 0.18 }, at + 0.6);
}
"""


def write_frame(n: int, slug: str, bg_css: str, body: str, css: str, js: str, flot: list, rays: str | None = "#FFE680") -> None:
    f = f"{n:02d}-{slug}"
    P = "f" + f
    d = DUR[n]
    fl_html, fl_js = floaters(P, flot, d)
    rep = lambda s: s.replace("__F__", P)
    rays_html = rays_svg(P, rays) if rays else ""
    rays_js = (f'tl.fromTo("#{P}-rays", {{rotation: 0, svgOrigin: "1000 1000"}}, {{rotation: 28, svgOrigin: "1000 1000", duration: {d:.3f}, ease: "none"}}, 0);'
               if rays else "")
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


def radial(c1: str, c2: str) -> str:
    return f"background: radial-gradient(1200px 1400px at 50% 36%, {c1} 0%, {c2} 75%);"


# ─────────────────────────────── Frame 1 — numéro ───────────────────────────────
def frame1():
    n = 1
    t_ret, t_num, t_sib = cue(n, "retenez"), cue(n, "numero"), cue(n, "sibabi")
    groupes = ["93", "17", "05", "34"]
    nums = "".join(f'<span id="__F__-g{i}" class="__F__-grp">{g}</span>' for i, g in enumerate(groupes))
    body = f"""
<div id="__F__-kick" class="__F__-abs __F__-kick">{phone_svg(54)}<span>RETENEZ CE NUMÉRO</span></div>
<div id="__F__-num" class="__F__-abs __F__-num"><div id="__F__-ring" class="__F__-ring">{phone_svg(110)}</div>{nums}</div>
{burst_svg("__F__", "__F__-b1", 540, 760, 260)}
<div id="__F__-flash" class="__F__-abs" style="left:0;top:0;width:1080px;height:1920px;background:radial-gradient(600px 600px at 50% 62%, rgba(255,255,255,.95), rgba(255,255,255,0));opacity:0"></div>
<div id="__F__-chez" class="__F__-abs __F__-chez">chez</div>
{logo("__F__", "__F__-logo", 90, 1080, 1.0)}
{burst_svg("__F__", "__F__-b2", 540, 1250, 360, "#FFFFFF")}
"""
    css = """
.__F__-kick { left: 0; right: 0; top: 470px; display: flex; justify-content: center; align-items: center; gap: 16px; font-weight: 800; font-size: 44px; letter-spacing: .12em; color: #FFE680; }
.__F__-num { left: 40px; width: 1000px; top: 600px; height: 300px; border-radius: 60px; background: linear-gradient(180deg, #F0313F, #B30F22);
  border: 8px solid #FFFFFF; box-shadow: 0 24px 50px rgba(0,0,0,.4); display: flex; align-items: center; justify-content: center; gap: 22px; }
.__F__-grp { font-family: "Lilita One", sans-serif; font-size: 156px; color: #FFFFFF; text-shadow: 0 8px 0 rgba(90,8,18,.5); display: inline-block; }
.__F__-ring { width: 150px; height: 150px; border-radius: 50%; background: rgba(255,255,255,.18); display: flex; align-items: center; justify-content: center; margin-right: 6px; }
.__F__-chez { left: 0; right: 0; top: 960px; text-align: center; font-family: "Kaushan Script", cursive; font-size: 96px; color: #FFE680; }
"""
    js = f"""
tl.fromTo("#__F__-num", {{ opacity: 0, scaleX: 0.3 }}, {{ opacity: 1, scaleX: 1, duration: 0.5, ease: "expo.out" }}, 0.0);
tl.fromTo("#__F__-ring", {{ rotation: 0 }}, {{ keyframes: {{ rotation: [0, -14, 14, -10, 10, -6, 0] }}, duration: 0.8, ease: "none" }}, 0.25);
{"".join(f'tl.fromTo("#__F__-g{i}", {{ opacity: 0, y: -420, scale: 1.4 }}, {{ opacity: 1, y: 0, scale: 1, duration: 0.55, ease: "bounce.out" }}, {0.2 + i * 0.32:.2f});' for i in range(4))}
burst("#__F__-b1", 1.25);
tl.fromTo("#__F__-kick", {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.5, ease: "power3.out" }}, {t_ret});
tl.fromTo("#__F__-num", {{ scale: 1 }}, {{ keyframes: {{ scale: [1, 1.07, 1] }}, duration: 0.5, ease: "power2.out", immediateRender: false }}, {t_num});
{"".join(f'tl.fromTo("#__F__-g{i}", {{ y: 0 }}, {{ y: {(-1) ** i * 12}, duration: 2.4, ease: "sine.inOut", immediateRender: false }}, {1.6 + i * 0.1:.2f});' for i in range(4))}
tl.fromTo("#__F__-chez", {{ opacity: 0, scale: 0.6 }}, {{ opacity: 1, scale: 1, duration: 0.45, ease: "back.out(2)" }}, {t_sib - 0.35});
tl.fromTo("#__F__-flash", {{ opacity: 0 }}, {{ keyframes: {{ opacity: [0, 1, 0] }}, duration: 0.6, ease: "none" }}, {t_sib});
popIn("#__F__-logo", {t_sib + 0.05}, {{ scale: 0.3, y: 120 }}, {{ ease: "back.out(1.4)", duration: 0.8 }});
burst("#__F__-b2", {t_sib + 0.15});
shine("#__F__-logo-front", {t_sib + 0.7});
levitate("#__F__-logo", {t_sib + 0.9}, {DUR[n]}, 12);
"""
    flot = [(glacon_svg(110), 60, 230, .3), (citron_svg(150), 860, 260, .5), (glacon_svg(80), 900, 1000, .2),
            (hibiscus_svg(140), 40, 1470, .5), (citron_svg(110), 880, 1500, .3), (glacon_svg(120), 80, 940, .6)]
    write_frame(n, "numero", radial("#2E9A48", VERT_F), body, css, js, flot)


# ─────────────────────────────── Frame 2 — marque ───────────────────────────────
def mini_glass(P, ident, haut, bas, paille):
    return glass_svg(P, ident, haut, bas, paille, w=150)


def frame2():
    n = 2
    t_sib, t_jus, t_sal, t_gla = cue(n, "sibabi"), cue(n, "jus"), cue(n, "salade"), cue(n, "glace")
    minis = "".join(f'<div id="__F__-m{i}" class="__F__-abs" style="left:{110 + i * 225}px;top:1235px">{mini_glass("__F__", f"__F__-mg{i}", h, b, p)}</div>'
                    for i, (h, b, p) in enumerate([("#F2F7A0", "#C9DC3A", "#2FB24A"), ("#D2203E", "#6E0A1E", "#FF5FA2"),
                                                   ("#FFD34A", "#F29A0C", "#FFE14D"), ("#C98A4B", "#7A4A1F", "#FFC93C")]))
    body = f"""
{logo("__F__", "__F__-logo", 90, 120, 0.92)}
<div id="__F__-med" class="__F__-abs __F__-med"><img src="assets/portrait-sibabi-2.png" alt=""></div>
<div id="__F__-rib" class="__F__-abs __F__-rib">Jus naturels</div>
{minis}
<div id="__F__-sal" class="__F__-badge" style="left:760px;top:560px;width:270px;height:270px;background:#FFD21F;color:#C8102E;border:8px solid #fff;font-size:58px">Salade<br><span style="font-family:'Kaushan Script';font-size:52px">délicieuse</span>{coeur_svg(48)}</div>
<div id="__F__-gla" class="__F__-badge" style="left:40px;top:600px;width:260px;height:260px;background:#D7192F;color:#fff;border:8px solid #fff;font-size:56px">Tout bien<br><span style="color:#FFD21F;font-size:70px">glacé !</span></div>
<div id="__F__-ice" class="__F__-abs" style="left:60px;top:520px">{glacon_svg(80)}</div>
"""
    css = """
.__F__-med { left: 250px; top: 520px; width: 580px; height: 580px; border-radius: 50%; overflow: hidden; border: 14px solid #FFD21F;
  box-shadow: 0 0 0 10px #1F7A34, 0 30px 60px rgba(0,0,0,.4); background: #fff; }
.__F__-med img { width: 100%; height: 130%; object-fit: cover; object-position: 50% 0%; }
.__F__-rib { left: 170px; width: 740px; top: 1080px; height: 120px; border-radius: 26px; background: linear-gradient(180deg, #8B5A2B, #5E3A1A);
  border: 6px solid #FFD21F; display: flex; align-items: center; justify-content: center; font-family: "Lilita One", sans-serif; font-size: 76px; color: #FFFFFF;
  box-shadow: 0 14px 30px rgba(0,0,0,.35); }
"""
    js = f"""
popIn("#__F__-logo", 0.0, {{ scale: 0.45 }}, {{ scale: 0.92, ease: "back.out(1.4)" }});
shine("#__F__-logo-front", 0.6);
tl.fromTo("#__F__-med", {{ opacity: 0, scale: 0.4, rotation: -12 }}, {{ opacity: 1, scale: 1, rotation: 0, duration: 0.9, ease: "expo.out" }}, {t_sib - 0.2});
levitate("#__F__-med", {t_sib + 0.8}, {DUR[n]}, 10);
tl.fromTo("#__F__-rib", {{ opacity: 0, scaleX: 0 }}, {{ opacity: 1, scaleX: 1, duration: 0.6, ease: "expo.out" }}, {t_jus});
{"".join(f'tl.fromTo("#__F__-m{i}", {{ opacity: 0, y: 160 }}, {{ opacity: 1, y: 0, duration: 0.55, ease: "back.out(1.8)" }}, {t_jus + 0.25 + i * 0.12:.2f});' for i in range(4))}
{"".join(f'fillGlass("__F__-mg{i}", {t_jus + 0.4 + i * 0.12:.2f}, 0.9);' for i in range(4))}
popIn("#__F__-sal", {t_sal}, {{ scale: 0.2, rotation: 30 }}, {{ rotation: 8 }});
popIn("#__F__-gla", {t_gla}, {{ scale: 0.2, rotation: -30 }}, {{ rotation: -8 }});
tl.fromTo("#__F__-ice", {{ opacity: 0, y: -200, rotation: 0 }}, {{ opacity: 1, y: 40, rotation: 40, duration: 0.6, ease: "bounce.out" }}, {t_gla + 0.1});
"""
    flot = [(citron_svg(120), 900, 1420, .4), (hibiscus_svg(120), 40, 1400, .4), (glacon_svg(90), 950, 980, .3), (feuille_svg(110), 20, 980, .3)]
    write_frame(n, "marque", radial("#FFE680", "#F2A900"), body, css, js, flot, rays="#FFFFFF")


# ─────────────────────────────── Frames 3–6 — jus ───────────────────────────────
JUS = {
    3: dict(slug="citron", nom="CITRON", de="Jus de", idx="1/4", bg=radial("#E9F57A", "#7FB21E"), haut="#F6FAB0", bas="#CFE03A", paille="#2FB24A",
            q=[("frais", "Frais"), ("acidule", "Acidulé"), ("vitamine", "Vitamine C")], photo="photo-citron.png", fin="reveiller",
            flot=lambda: [(citron_svg(170), 40, 260, .6), (citron_svg(120), 900, 1180, .4), (feuille_svg(110), 870, 300, .5), (glacon_svg(90), 60, 1420, .3), (citron_svg(100), 520, 1500, .2)]),
    4: dict(slug="bissap", nom="BISSAP", de="Jus de", idx="2/4", bg=radial("#E5365A", "#5A0619"), haut="#E0244A", bas="#5C0418", paille="#FF6FB0",
            q=[("couleur", "Couleur rubis"), ("gout", "Goût doux"), ("desaltere", "Désaltérant")], photo="photo-bissap.png", fin="hibiscus",
            flot=lambda: [(hibiscus_svg(190), 30, 250, .6), (hibiscus_svg(130), 880, 1180, .4), (hibiscus_svg(110), 900, 300, .5), (glacon_svg(90), 60, 1420, .3), (hibiscus_svg(90), 520, 1500, .2)]),
    5: dict(slug="ananas", nom="ANANAS", de="Jus d'", idx="3/4", bg=radial("#FFE35A", "#E07A00"), haut="#FFE16A", bas="#F09A0E", paille="#FFF06A",
            q=[("dore", "Doré"), ("fruite", "Fruité"), ("soleil", "Plein de soleil")], photo="photo-ananas.png", fin="plaisir",
            flot=lambda: [(ananas_svg(180), 30, 240, .6), (ananas_svg(120), 900, 1180, .4), (feuille_svg(110), 880, 300, .5), (glacon_svg(90), 60, 1420, .3), (ananas_svg(90), 520, 1500, .2)]),
    6: dict(slug="tamarin", nom="TAMARIN", de="Jus de", idx="4/4", bg=radial("#D49A5C", "#4A2610"), haut="#D8995A", bas="#7A4419", paille="#FFC93C",
            q=[("acidule", "Acidulé"), ("parfume", "Parfumé"), ("chez", "Goût de chez nous")], photo="photo-tamarin.png", fin="rafraichit",
            flot=lambda: [(tamarin_svg(220), 20, 280, .6), (tamarin_svg(160), 860, 1200, .4), (feuille_svg(110), 880, 300, .5), (glacon_svg(90), 60, 1420, .3), (tamarin_svg(130), 480, 1510, .2)]),
}


def frame_jus(n):
    c = JUS[n]
    t_nom = cue(n, c["nom"].lower())
    tq = [cue(n, m) for m, _ in c["q"]]
    if n == 4:  # « fait avec la fleur d'hibiscus » : pastille dédiée sur « hibiscus »
        t_hib = cue(n, "hibiscus")
    t_fin = cue(n, c["fin"]) if n != 4 else cue(n, "desaltere")
    pills = "".join(pill("__F__", f"__F__-p{i}", 560, 640 + i * 150, label) for i, (_, label) in enumerate(c["q"]))
    extra = ""
    if n == 4:
        extra = pill("__F__", "__F__-ph", 560, 490, "Fleur d'hibiscus", ROUGE)
    body = f"""
<div id="__F__-count" class="__F__-count">{c["idx"]}</div>
<div id="__F__-t1" class="__F__-title1" style="top:150px">{c["de"]}</div>
<div id="__F__-t2" class="__F__-title2" style="top:240px">{c["nom"]}</div>
<div id="__F__-gl" class="__F__-abs" style="left:70px;top:520px">{glass_svg("__F__", "__F__-g", c["haut"], c["bas"], c["paille"], w=470)}</div>
{burst_svg("__F__", "__F__-b", 305, 900, 300, "#FFFFFF")}
{extra}{pills}
<div id="__F__-photo" class="__F__-photo" style="left:600px;top:1130px;width:420px;height:400px"><img src="assets/{c["photo"]}" alt=""><span>Photo réelle</span></div>
"""
    js = f"""
tl.fromTo("#__F__-count", {{ opacity: 0, x: -60 }}, {{ opacity: 1, x: 0, duration: 0.5, ease: "power3.out" }}, 0.0);
tl.fromTo("#__F__-t1", {{ opacity: 0, x: -200 }}, {{ opacity: 1, x: 0, duration: 0.6, ease: "power3.out" }}, 0.05);
tl.fromTo("#__F__-t2", {{ opacity: 0, scale: 1.6, filter: "blur(12px)" }}, {{ opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.6, ease: "expo.out" }}, {t_nom});
tl.fromTo("#__F__-gl", {{ opacity: 0, y: 300 }}, {{ opacity: 1, y: 0, duration: 0.7, ease: "power3.out" }}, 0.1);
fillGlass("__F__-g", 0.45, 1.3);
burst("#__F__-b", 1.5);
levitate("#__F__-gl", 1.8, {DUR[n]}, 16);
{"".join(f'popIn("#__F__-p{i}", {t:.3f}, {{ x: 120, scale: 0.7 }}, {{ x: 0 }});' for i, t in enumerate(tq))}
{('popIn("#__F__-ph", ' + str(t_hib) + ', { x: 120, scale: 0.7 }, { x: 0 });') if n == 4 else ''}
tl.fromTo("#__F__-photo", {{ opacity: 0, rotation: 18, scale: 0.6, y: 120 }}, {{ opacity: 1, rotation: 5, scale: 1, y: 0, duration: 0.7, ease: "back.out(1.4)" }}, {t_fin});
"""
    write_frame(n, c["slug"], c["bg"], body, "", js, c["flot"]())


# ─────────────────────────────── Frame 7 — salade ───────────────────────────────
def frame7():
    n = 7
    t_acc, t_sal = cue(n, "accompagner"), cue(n, "salade")
    tq = [cue(n, "fraiche"), cue(n, "croquante"), cue(n, "coloree")]
    body = f"""
<div id="__F__-t1" class="__F__-title2" style="top:150px;font-size:190px">SALADE</div>
<div id="__F__-t2" class="__F__-title1" style="top:360px;font-size:100px">délicieuse {coeur_svg(70)}</div>
<div id="__F__-ph" class="__F__-abs __F__-ph"><img src="assets/photo-salade.png" alt=""></div>
{pill("__F__", "__F__-p0", 70, 1270, "Fraîche")}
{pill("__F__", "__F__-p1", 380, 1400, "Croquante")}
{pill("__F__", "__F__-p2", 700, 1270, "Colorée", ROUGE)}
"""
    css = """
.__F__-ph { left: 210px; top: 540px; width: 660px; height: 660px; border-radius: 50%; overflow: hidden; border: 16px solid #FFFFFF; box-shadow: 0 0 0 10px #FFD21F, 0 30px 60px rgba(0,0,0,.35); }
.__F__-ph img { width: 100%; height: 100%; object-fit: cover; }
"""
    js = f"""
tl.fromTo("#__F__-t1", {{ opacity: 0, scale: 1.6, filter: "blur(12px)" }}, {{ opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.6, ease: "expo.out" }}, {max(0.0, t_acc - 0.2)});
tl.fromTo("#__F__-t2", {{ opacity: 0, y: 40 }}, {{ opacity: 1, y: 0, duration: 0.6, ease: "power3.out" }}, {t_sal});
tl.fromTo("#__F__-ph", {{ opacity: 0, scale: 0.3, rotation: -90 }}, {{ opacity: 1, scale: 1, rotation: 0, duration: 1.0, ease: "expo.out" }}, 0.1);
tl.fromTo("#__F__-ph", {{ rotation: 0 }}, {{ rotation: 8, duration: {DUR[n] - 1.1:.2f}, ease: "sine.inOut", immediateRender: false }}, 1.1);
{"".join(f'popIn("#__F__-p{i}", {t:.3f});' for i, t in enumerate(tq))}
"""
    flot = [(tomate_svg(150), 30, 560, .6), (concombre_svg(130), 900, 640, .5), (feuille_svg(130), 880, 1080, .4),
            (tomate_svg(100), 60, 1080, .3), (concombre_svg(90), 520, 1520, .2)]
    write_frame(n, "salade", radial("#8ED36B", "#2E7D32"), body, css, js, flot)


# ─────────────────────────────── Frame 8 — promesse ───────────────────────────────
def frame8():
    n = 8
    tq = [cue(n, "fraicheur"), cue(n, "gout"), cue(n, "satisfaction")]
    t_prio = cue(n, "priorite")
    lignes = [("Fraîcheur", VERT), ("Goût naturel", VERT), ("Votre satisfaction", ROUGE)]
    rows = "".join(f'<div id="__F__-r{i}" class="__F__-row">{check_svg(c)}<span>{t}</span></div>' for i, (t, c) in enumerate(lignes))
    body = f"""
<div id="__F__-ph" class="__F__-abs __F__-ph"><img src="assets/portrait-sibabi-2.png" alt=""></div>
<div id="__F__-name" class="__F__-abs __F__-name"><span style="font-family:'Kaushan Script'">Madame</span> SIBABI</div>
<div id="__F__-card" class="__F__-abs __F__-card">{rows}</div>
<div id="__F__-rib" class="__F__-abs __F__-rib">Votre satisfaction, notre priorité {coeur_svg(56, "#FFFFFF")}</div>
"""
    css = """
.__F__-ph { left: 200px; top: 130px; width: 680px; height: 820px; border-radius: 40px; overflow: hidden; border: 14px solid #FFD21F; box-shadow: 0 30px 60px rgba(0,0,0,.4); }
.__F__-ph img { width: 100%; height: 100%; object-fit: cover; object-position: 50% 10%; }
.__F__-name { left: 250px; width: 580px; top: 880px; height: 110px; border-radius: 9999px; background: #1F7A34; border: 6px solid #FFFFFF;
  display: flex; align-items: center; justify-content: center; gap: 14px; font-family: "Lilita One"; font-size: 64px; color: #FFD21F; }
.__F__-card { left: 120px; width: 840px; top: 1040px; padding: 30px 40px; border-radius: 34px; background: #FFF8EC; box-shadow: 0 20px 40px rgba(0,0,0,.3); }
.__F__-row { display: flex; align-items: center; gap: 22px; padding: 12px 0; font-weight: 800; font-size: 52px; color: #2A160C; }
.__F__-rib { left: 50px; width: 980px; top: 1430px; height: 120px; border-radius: 22px; background: linear-gradient(180deg, #E8283A, #B30F22);
  display: flex; align-items: center; justify-content: center; gap: 16px; font-family: "Kaushan Script"; font-size: 58px; color: #FFFFFF; box-shadow: 0 16px 30px rgba(0,0,0,.35); }
"""
    js = f"""
tl.fromTo("#__F__-ph", {{ opacity: 0, scale: 1.15 }}, {{ opacity: 1, scale: 1, duration: 0.9, ease: "power3.out" }}, 0.0);
tl.fromTo("#__F__-name", {{ opacity: 0, y: 60 }}, {{ opacity: 1, y: 0, duration: 0.6, ease: "back.out(1.6)" }}, 0.4);
tl.fromTo("#__F__-card", {{ opacity: 0, y: 80 }}, {{ opacity: 1, y: 0, duration: 0.6, ease: "power3.out" }}, {max(0.2, tq[0] - 0.3):.3f});
{"".join(f'tl.fromTo("#__F__-r{i}", {{ opacity: 0, x: -80 }}, {{ opacity: 1, x: 0, duration: 0.5, ease: "power3.out" }}, {t:.3f});' for i, t in enumerate(tq))}
tl.fromTo("#__F__-rib", {{ opacity: 0, scaleX: 0 }}, {{ opacity: 1, scaleX: 1, duration: 0.6, ease: "expo.out" }}, {t_prio});
levitate("#__F__-ph", 1.0, {DUR[n]}, 10);
"""
    flot = [(coeur_svg(70, "#FFD21F"), 70, 320, .4), (coeur_svg(50, "#FFFFFF"), 950, 600, .3), (feuille_svg(110), 930, 180, .5), (citron_svg(100), 40, 900, .3)]
    write_frame(n, "promesse", radial("#2E9A48", VERT_F), body, css, js, flot)


# ─────────────────────────────── Frame 9 — CTA ───────────────────────────────
def frame9():
    n = 9
    t_q, t_app, t_num, t_gou, t_sat = cue(n, "quartier"), cue(n, "appelez"), cue(n, "93"), cue(n, "gouter"), cue(n, "satisfait")
    body = f"""
<div id="__F__-etal" class="__F__-abs __F__-etal"><img src="assets/etal-jus-salade.png" alt=""></div>
<div id="__F__-pin" class="__F__-abs" style="left:110px;top:640px">{pin_svg(130)}</div>
<div id="__F__-loc" class="__F__-abs __F__-loc"><small>Située au</small>Quartier TCHITCHAO</div>
<div id="__F__-call" class="__F__-abs __F__-call"><div id="__F__-wave" class="__F__-wave"></div><div class="__F__-ic">{phone_svg(96, "#D7192F")}</div><span>93 17 05 34</span></div>
{logo("__F__", "__F__-logo", 90, 1150, 0.7)}
<div id="__F__-ban" class="__F__-abs __F__-ban">Venez goûter, vous serez toujours satisfait ! {coeur_svg(50)}</div>
{burst_svg("__F__", "__F__-b", 540, 1020, 330, "#FFE680")}
"""
    css = """
.__F__-etal { left: 60px; width: 960px; top: 110px; height: 500px; border-radius: 36px; overflow: hidden; border: 10px solid #FFFFFF; box-shadow: 0 24px 50px rgba(0,0,0,.4); }
.__F__-etal img { width: 100%; height: 100%; object-fit: cover; object-position: 50% 60%; }
.__F__-loc { left: 260px; top: 660px; font-family: "Lilita One"; font-size: 74px; line-height: 1; color: #FFD21F; -webkit-text-stroke: 10px #2A160C; paint-order: stroke fill; }
.__F__-loc small { display: block; font-family: "Poppins"; font-weight: 600; font-size: 38px; color: #FFFFFF; -webkit-text-stroke: 0; margin-bottom: 8px; }
.__F__-call { left: 60px; width: 960px; top: 890px; height: 230px; border-radius: 9999px; background: linear-gradient(180deg, #F0313F, #B30F22); border: 10px solid #FFFFFF;
  display: flex; align-items: center; justify-content: center; gap: 30px; box-shadow: 0 24px 50px rgba(0,0,0,.4); }
.__F__-call span { font-family: "Lilita One"; font-size: 140px; color: #FFFFFF; text-shadow: 0 8px 0 rgba(90,8,18,.5); }
.__F__-ic { width: 150px; height: 150px; border-radius: 50%; background: #FFFFFF; display: flex; align-items: center; justify-content: center; }
.__F__-wave { position: absolute; inset: -10px; border-radius: 9999px; border: 10px solid #FFD21F; opacity: 0; }
.__F__-ban { left: 40px; width: 1000px; top: 1468px; height: 120px; border-radius: 22px; background: #FFD21F; transform: rotate(-2deg);
  display: flex; align-items: center; justify-content: center; gap: 12px; font-family: "Kaushan Script"; font-size: 50px; color: #2A160C; box-shadow: 0 14px 30px rgba(0,0,0,.35); }
"""
    js = f"""
tl.fromTo("#__F__-etal", {{ opacity: 0, scale: 1.2 }}, {{ opacity: 1, scale: 1, duration: 0.8, ease: "power3.out" }}, 0.0);
tl.fromTo("#__F__-pin", {{ opacity: 0, y: -500 }}, {{ opacity: 1, y: 0, duration: 0.8, ease: "bounce.out" }}, {max(0.1, t_q - 0.3):.3f});
slideIn("#__F__-loc", {t_q}, 120, 0);
popIn("#__F__-call", {t_app}, {{ scale: 0.4 }}, {{ ease: "back.out(1.5)" }});
burst("#__F__-b", {t_num});
{"".join(f'tl.fromTo("#__F__-wave", {{ opacity: 0.9, scale: 1 }}, {{ opacity: 0, scale: 1.18, duration: 0.9, ease: "power2.out", immediateRender: false }}, {t_num + 0.3 + k * 1.0:.2f});' for k in range(int(max(1, (DUR[n] - t_num - 0.6) // 1.0))))}
tl.fromTo("#__F__-call", {{ scale: 1 }}, {{ keyframes: {{ scale: [1, 1.05, 1] }}, duration: 0.5, ease: "power2.out", immediateRender: false }}, {t_num + 0.2:.2f});
popIn("#__F__-logo", {t_gou - 0.3:.3f}, {{ scale: 0.25 }}, {{ scale: 0.7, ease: "back.out(1.4)" }});
shine("#__F__-logo-front", {t_gou + 0.4:.3f});
tl.fromTo("#__F__-ban", {{ opacity: 0, scaleX: 0 }}, {{ opacity: 1, scaleX: 1, duration: 0.6, ease: "expo.out" }}, {t_gou:.3f});
tl.to(R, {{ opacity: 0, duration: 0.4, ease: "power2.in" }}, {DUR[n] - 0.42:.3f});
"""
    flot = [(citron_svg(110), 930, 680, .4), (hibiscus_svg(110), 30, 1300, .4), (glacon_svg(90), 960, 1320, .3), (ananas_svg(110), 20, 840, .3)]
    write_frame(n, "cta", radial("#2E9A48", VERT_F), body, css, js, flot)


frame1()
frame2()
for k in (3, 4, 5, 6):
    frame_jus(k)
frame7()
frame8()
frame9()
