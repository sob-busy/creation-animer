"""Génère compositions/frames/NN-*.html pour la vidéo « Créer des skills dans Claude Code ».

Chaque frame = un <template> autonome (styles + scripts dedans), timeline GSAP en pause
enregistrée sur window.__timelines[frame_id], 1080×1920, contenu au-dessus de y=1600.
"""

from __future__ import annotations

import json
import math
import re
import sys
from pathlib import Path

PROJ = Path(sys.argv[1])
OUT = PROJ / "compositions" / "frames"
OUT.mkdir(parents=True, exist_ok=True)

SB = (PROJ / "STORYBOARD.md").read_text(encoding="utf-8")
DUR = {int(n): float(d) for n, d in re.findall(r"## Frame (\d+) —.*?- duration: ([\d.]+)s", SB, re.S)}

C = dict(ink="#141413", cream="#FAF9F5", tile="#EFE9DE", tiles="#ECE3D4", coral="#CC785C",
         navy="#181715", navys="#1F1E1B", navye="#252320", teal="#5DB8A6", amber="#E8A55A")


def base_css(f: str) -> str:
    return f"""
@font-face {{ font-family: "EB Garamond"; src: url("assets/fonts/EBGaramond-400.woff2") format("woff2"); font-weight: 400; }}
@font-face {{ font-family: "Inter"; src: url("assets/fonts/Inter-400.woff2") format("woff2"); font-weight: 400; }}
@font-face {{ font-family: "Inter"; src: url("assets/fonts/Inter-700.woff2") format("woff2"); font-weight: 700; }}
@font-face {{ font-family: "JetBrains Mono"; src: url("assets/fonts/JetBrainsMono-400.woff2") format("woff2"); font-weight: 400; }}
@font-face {{ font-family: "JetBrains Mono"; src: url("assets/fonts/JetBrainsMono-700.woff2") format("woff2"); font-weight: 700; }}
#root {{ position: absolute; inset: 0; width: 1080px; height: 1920px; overflow: hidden; container-type: size;
  font-family: "Inter", sans-serif; color: {C['ink']}; }}
#root * {{ box-sizing: border-box; }}
.{f}-bg {{ position: absolute; inset: 0; background-color: {C['cream']};
  background-image: linear-gradient(rgba(20,20,19,.055) 1px, transparent 1px), linear-gradient(90deg, rgba(20,20,19,.055) 1px, transparent 1px);
  background-size: 72px 72px; background-position: 36px 36px; }}
.{f}-vignette {{ position: absolute; inset: 0; background: radial-gradient(900px 1100px at 50% 40%, rgba(250,249,245,0) 0%, rgba(239,233,222,.85) 100%); }}
.{f}-float {{ position: absolute; opacity: 0; filter: blur(1.2px); }}
.{f}-fcard {{ background: {C['tile']}; border: 1px solid rgba(20,20,19,.16); border-radius: 10px; padding: 14px 18px 16px;
  font-family: "JetBrains Mono", monospace; font-size: 22px; color: rgba(20,20,19,.6); box-shadow: 0 1px 3px rgba(20,20,19,.06), 0 4px 16px rgba(20,20,19,.04); }}
.{f}-fcard i {{ display: block; height: 7px; border-radius: 4px; background: rgba(20,20,19,.14); margin-top: 10px; }}
.{f}-fglyph {{ font-family: "JetBrains Mono", monospace; font-size: 64px; color: rgba(20,20,19,.22); }}
.{f}-fstar {{ font-family: "Inter", sans-serif; font-size: 70px; color: rgba(204,120,92,.35); }}
.{f}-kicker {{ position: absolute; left: 0; right: 0; text-align: center; font-family: "JetBrains Mono", monospace; font-size: 28px;
  letter-spacing: .16em; text-transform: uppercase; color: rgba(20,20,19,.7); }}
.{f}-kicker b {{ color: {C['coral']}; font-weight: 400; margin-right: 14px; }}
.{f}-title {{ position: absolute; left: 60px; right: 60px; text-align: center; font-family: "EB Garamond", serif; font-weight: 400;
  letter-spacing: -.02em; line-height: 1.02; color: {C['ink']}; }}
.{f}-w {{ display: inline-block; will-change: transform, opacity; }}
.{f}-badge {{ position: absolute; left: 50%; top: 150px; margin-left: -130px; width: 260px; height: 64px; border-radius: 9999px;
  background: {C['coral']}; color: {C['cream']}; font-family: "JetBrains Mono", monospace; font-size: 26px; letter-spacing: .18em;
  display: flex; align-items: center; justify-content: center; }}
.{f}-card {{ position: absolute; background: {C['tile']}; border: 1px solid rgba(20,20,19,.12); border-radius: 12px;
  box-shadow: 0 1px 3px rgba(20,20,19,.08), 0 4px 16px rgba(20,20,19,.04); }}
.{f}-navy {{ position: absolute; background: {C['navy']}; border: 1px solid rgba(250,249,245,.12); border-radius: 12px; color: {C['cream']};
  box-shadow: 0 2px 6px rgba(20,20,19,.18), 0 18px 48px rgba(20,20,19,.16); font-family: "JetBrains Mono", monospace; overflow: hidden; }}
.{f}-bar {{ height: 58px; background: {C['navye']}; border-bottom: 1px solid rgba(250,249,245,.1); display: flex; align-items: center; padding: 0 22px; gap: 10px; }}
.{f}-bar span.d {{ width: 14px; height: 14px; border-radius: 50%; background: rgba(250,249,245,.22); }}
.{f}-bar em {{ font-style: normal; margin-left: 14px; font-size: 22px; color: rgba(250,249,245,.62); letter-spacing: .04em; }}
.{f}-code {{ font-size: 33px; line-height: 1.62; padding: 26px 34px; white-space: pre; }}
.{f}-k {{ color: {C['teal']}; }} .{f}-v {{ color: {C['cream']}; }} .{f}-s {{ color: {C['amber']}; }} .{f}-m {{ color: rgba(250,249,245,.45); }}
.{f}-caret {{ display: inline-block; width: 16px; height: 36px; background: {C['coral']}; vertical-align: -6px; margin-left: 3px; }}
.{f}-mono {{ font-family: "JetBrains Mono", monospace; }}
"""


FLOAT_SETS = [
    # (type, x, y, contenu)
    [("card", 70, 300, "SKILL.md"), ("glyph", 900, 250, "/"), ("star", 140, 1180, "✱"), ("card", 820, 1300, ".md"),
     ("glyph", 60, 1500, "{ }"), ("folder", 860, 640, "")],
    [("glyph", 80, 220, "/"), ("card", 830, 330, ".md"), ("folder", 60, 1240, ""), ("star", 930, 1080, "✱"),
     ("card", 760, 1480, "SKILL.md"), ("glyph", 120, 700, "{ }")],
]


def floaters(f: str, n: int) -> tuple[str, str]:
    items = FLOAT_SETS[n % 2]
    html, js = [], []
    d = DUR[n]
    for i, (kind, x, y, txt) in enumerate(items):
        fid = f"{f}-fl{i}"
        ink = "rgba(20,20,19,.32)"
        if kind == "card":
            w = 150 if txt == "SKILL.md" else 110
            inner = (f'<svg width="{w}" height="{int(w*1.25)}" viewBox="0 0 {w} {int(w*1.25)}">'
                     f'<rect x="1" y="1" width="{w-2}" height="{int(w*1.25)-2}" rx="10" fill="{C["tile"]}" stroke="{ink}" stroke-width="2"/>'
                     + "".join(f'<rect x="16" y="{22+i*18}" width="{(w-32)*(1-0.2*(i%3))}" height="7" rx="3.5" fill="rgba(20,20,19,.22)"/>' for i in range(4))
                     + (f'<rect x="16" y="{int(w*1.25)-30}" width="40" height="12" rx="6" fill="rgba(204,120,92,.55)"/>' if txt == "SKILL.md" else "")
                     + '</svg>')
        elif kind == "glyph" and txt == "/":
            inner = f'<svg width="60" height="90" viewBox="0 0 60 90"><path d="M44 6 L16 84" stroke="{ink}" stroke-width="9" stroke-linecap="round"/></svg>'
        elif kind == "glyph":
            inner = (f'<svg width="110" height="90" viewBox="0 0 110 90"><path d="M34 6 q-14 0 -14 14 v14 q0 10 -12 11 q12 1 12 11 v14 q0 14 14 14 '
                     f'M76 6 q14 0 14 14 v14 q0 10 12 11 q-12 1 -12 11 v14 q0 14 -14 14" fill="none" stroke="{ink}" stroke-width="7" stroke-linecap="round"/></svg>')
        elif kind == "star":
            inner = ('<svg width="80" height="80" viewBox="-40 -40 80 80">'
                     + "".join(f'<rect x="-5" y="-36" width="10" height="72" rx="5" fill="rgba(204,120,92,.45)" transform="rotate({a})"/>' for a in (0, 60, 120))
                     + '</svg>')
        else:
            inner = folder_svg(f, 150, 112, opacity=0.55)
        html.append(f'<div id="{fid}" class="{f}-float" style="left:{x}px;top:{y}px">{inner}</div>')
        dx = (-1) ** i * (10 + 4 * (i % 3))
        dy = -(22 + 7 * ((i * 5) % 4))
        rot = (-1) ** (i + 1) * (3 + i % 3)
        js.append(f'tl.fromTo("#{fid}", {{opacity: 0}}, {{opacity: {0.45 + 0.08 * (i % 3):.2f}, duration: 0.9, ease: "power2.out"}}, {0.05 * i:.2f});')
        js.append(f'tl.fromTo("#{fid}", {{x: 0, y: 0, rotation: {-rot / 2}}}, {{x: {dx}, y: {dy}, rotation: {rot}, duration: {d:.3f}, ease: "sine.inOut"}}, 0);')
    return "\n".join(html), "\n".join(js)


def folder_svg(f: str, w: int, h: int, opacity: float = 1.0, label: str = "", ident: str = "") -> str:
    lab = (f'<text x="{w * 0.5}" y="{h * 0.64}" text-anchor="middle" font-family="JetBrains Mono" font-size="{h * 0.11:.0f}" '
           f'fill="rgba(20,20,19,.72)">{label}</text>') if label else ""
    idattr = f' id="{ident}"' if ident else ""
    return (f'<svg{idattr} width="{w}" height="{h}" viewBox="0 0 {w} {h}" style="opacity:{opacity};overflow:visible">'
            f'<path d="M4 {h * 0.14} q0 -{h * 0.1} {w * 0.04} -{h * 0.1} h{w * 0.3} l{w * 0.06} {h * 0.1} h{w * 0.54} '
            f'q{w * 0.04} 0 {w * 0.04} {h * 0.06} v{h * 0.74} q0 {h * 0.06} -{w * 0.04} {h * 0.06} h-{w * 0.9} '
            f'q-{w * 0.04} 0 -{w * 0.04} -{h * 0.06} z" fill="{C["tiles"]}" stroke="rgba(20,20,19,.22)" stroke-width="2"/>'
            f'<path d="M4 {h * 0.3} h{w - 8}" stroke="rgba(20,20,19,.14)" stroke-width="2"/>{lab}</svg>')


def words(f: str, text: str, cls_extra: str = "", ids: str = "") -> str:
    out = []
    for i, w in enumerate(text.split(" ")):
        out.append(f'<span class="{f}-w {cls_extra}" data-wi="{ids}{i}">{w}</span>')
    return " ".join(out)


JS_HELPERS = """
const R = document.querySelector('[data-composition-id="__F__"]');
const q = (s) => R.querySelector(s);
const qa = (s) => Array.from(R.querySelectorAll(s));
function typeOn(el, text, at, dur) {
  const o = { n: 0 };
  el.textContent = "";
  tl.fromTo(o, { n: 0 }, { n: text.length, duration: dur, ease: "none",
    onUpdate: () => { el.textContent = text.slice(0, Math.round(o.n)); } }, at);
}
function caretBlink(el, from, to) {
  for (let t = from, k = 0; t < to; t += 0.5, k++) tl.set(el, { opacity: k % 2 ? 1 : 0.15 }, t);
}
function wordsIn(sel, at, gap, y) {
  tl.fromTo(qa(sel), { opacity: 0, y: y || 60, filter: "blur(8px)" },
    { opacity: 1, y: 0, filter: "blur(0px)", duration: 0.7, ease: "power3.out", stagger: gap }, at);
}
function popIn(sel, at, opts) {
  tl.fromTo(q(sel), Object.assign({ opacity: 0, scale: 0.86, y: 40 }, (opts && opts.from) || {}),
    Object.assign({ opacity: 1, scale: 1, y: 0, duration: 0.8, ease: "power3.out" }, (opts && opts.to) || {}), at);
}
function levitate(sel, at, end, amp) {
  tl.fromTo(q(sel), { y: 0 }, { y: -(amp || 12), immediateRender: false, duration: Math.max(0.3, end - at), ease: "sine.inOut" }, at);
}
"""


def write_frame(n: int, slug: str, body: str, css: str, js: str) -> None:
    f = f"{n:02d}-{slug}"
    P = "f" + f  # préfixe d'id/classe : un id CSS ne peut pas commencer par un chiffre
    d = DUR[n]
    fl_html, fl_js = floaters(P, n)
    body = body.replace("__F__", P)
    css = css.replace("__F__", P)
    js = js.replace("__F__", P)
    html = f"""<template>
<script src="assets/vendor/gsap.min.js"></script>
<style>{base_css(P)}
{css}
</style>
<div id="root" data-composition-id="{f}" data-width="1080" data-height="1920" data-duration="{d}">
  <div id="{P}-bg" class="{P}-bg clip" data-start="0" data-duration="{d}" data-track-index="0"></div>
  <div id="{P}-vignette" class="{P}-vignette clip" data-start="0" data-duration="{d}" data-track-index="1"></div>
  <div id="{P}-floaters" class="clip" data-start="0" data-duration="{d}" data-track-index="2" style="position:absolute;inset:0">
{fl_html}
  </div>
  <div id="{P}-stage" class="clip" data-start="0" data-duration="{d}" data-track-index="3" style="position:absolute;inset:0">
{body}
  </div>
</div>
<script>
(function () {{
window.__timelines = window.__timelines || {{}};
const tl = gsap.timeline({{ paused: true }});
{JS_HELPERS.replace("__F__", f)}
{fl_js}
{js}
tl.set({{}}, {{}}, {d});
window.__timelines["{f}"] = tl;
}})();
</script>
</template>
"""
    (OUT / f"{f}.html").write_text(html, encoding="utf-8")
    print("écrit", f, d)


# ───────────────────────── Frame 1 — hook ─────────────────────────
def bubble(f, ident, top, text, extra=""):
    return (f'<div id="{ident}" class="{f}-card {f}-bubble" data-layout-allow-overlap data-layout-allow-occlusion style="left:130px;top:{top}px;width:820px;{extra}">'
            f'<div class="{f}-who">Toi → Claude</div><div class="{f}-btxt">{text}</div></div>')


F1_CSS = """
.__F__-bubble { padding: 30px 36px 34px; border-radius: 28px 28px 28px 8px; }
.__F__-who { font-family: "JetBrains Mono", monospace; font-size: 22px; letter-spacing: .12em; text-transform: uppercase; color: rgba(20,20,19,.5); margin-bottom: 12px; }
.__F__-btxt { font-size: 40px; line-height: 1.32; color: #141413; }
.__F__-count { position: absolute; right: 90px; top: 1130px; font-family: "EB Garamond", serif; font-size: 150px; letter-spacing: -.03em; color: #141413; }
.__F__-count small { font-family: "JetBrains Mono", monospace; font-size: 30px; letter-spacing: .1em; color: rgba(20,20,19,.55); display: block; text-align: right; margin-top: -8px; }
.__F__-q { color: #CC785C; }
"""
F1_BODY = """
<div id="__F__-kick" class="__F__-kicker" style="top:150px"><b>✱</b>Claude Code</div>
<div id="__F__-title" class="__F__-title" style="top:225px;font-size:190px">Encore<span class="__F__-q"> ?</span></div>
""" + "\n".join([
    bubble("__F__", "__F__-b2", 870, "Rappelle-toi : réponds en français, ton direct, pas de jargon…", "opacity:0"),
    bubble("__F__", "__F__-b1", 700, "Rappelle-toi : réponds en français, ton direct, pas de jargon…", "opacity:0"),
    bubble("__F__", "__F__-b0", 530, "Rappelle-toi : réponds en français, ton direct, pas de jargon…"),
]) + """
<div id="__F__-count" class="__F__-count"><span id="__F__-cnum">×1</span><small>même consigne</small></div>
"""
F1_JS = """
tl.fromTo("#__F__-kick", { opacity: 0, y: -20 }, { opacity: 1, y: 0, duration: 0.6, ease: "power3.out" }, 0.0);
popIn("#__F__-b0", 0.05);
tl.fromTo("#__F__-count", { opacity: 0, x: 40 }, { opacity: 1, x: 0, duration: 0.6, ease: "power3.out" }, 0.5);
tl.fromTo("#__F__-b1", { opacity: 0, y: -120, scale: 0.97 }, { opacity: 0.85, y: 0, scale: 1, duration: 0.6, ease: "power3.out" }, 1.0);
tl.fromTo("#__F__-b2", { opacity: 0, y: -120, scale: 0.94 }, { opacity: 0.7, y: 0, scale: 1, duration: 0.6, ease: "power3.out" }, 1.5);
tl.set("#__F__-b1", { filter: "blur(1px)" }, 1.0);
tl.set("#__F__-b2", { filter: "blur(2px)" }, 1.5);
const num = q("#__F__-cnum");
tl.call(() => { num.textContent = "×1"; }, null, 0.0);
[[1.0, "×2"], [1.5, "×3"], [2.2, "×12"], [2.6, "×47"]].forEach(([t, v], i) => {
  tl.set(num, { textContent: v }, t);
  tl.fromTo("#__F__-cnum", { scale: 1.18 }, { immediateRender: i === 0, scale: 1, duration: 0.3, ease: "power3.out" }, t);
});
tl.fromTo("#__F__-title", { opacity: 0, scale: 1.25, filter: "blur(14px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.45, ease: "expo.out" }, 2.15);
tl.fromTo(["#__F__-b0", "#__F__-b1", "#__F__-b2"], { x: 0 }, { immediateRender: false, keyframes: { x: [0, -10, 9, -6, 4, 0] }, duration: 0.45, ease: "none" }, 2.6);
levitate("#__F__-title", 2.6, 3.38, 6);
"""

# ───────────────────────── Frame 2 — concept ─────────────────────────
F2_CSS = """
.__F__-hero { color: #141413; }
.__F__-hero .__F__-sk { color: #CC785C; }
.__F__-skill { position: absolute; left: 610px; top: 980px; width: 380px; transform-origin: 0% 100%; }
.__F__-skill .__F__-code { font-size: 26px; padding: 18px 24px; line-height: 1.7; }
.__F__-ok { position: absolute; left: 50%; top: 1390px; margin-left: -250px; width: 500px; height: 92px; border-radius: 9999px;
  background: #FAF9F5; border: 1px solid rgba(20,20,19,.2); display: flex; align-items: center; justify-content: center; gap: 18px;
  font-family: "JetBrains Mono", monospace; font-size: 30px; letter-spacing: .06em; color: #141413; }
"""
F2_BODY = f"""
<div id="__F__-kick" class="__F__-kicker" style="top:170px"><b>✱</b>La solution</div>
<div id="__F__-hero" class="__F__-title __F__-hero" style="top:250px;font-size:230px">{words('__F__', 'Un skill.', '', 'h')}</div>
<div id="__F__-folder" style="position:absolute;left:150px;top:640px;width:560px;height:430px">{folder_svg('__F__', 560, 430, 1, 'mon-skill/', '__F__-fsvg')}</div>
<div id="__F__-skill" class="__F__-navy __F__-skill">
  <div class="__F__-bar"><span class="d"></span><span class="d"></span><span class="d"></span><em>SKILL.md</em></div>
  <div class="__F__-code"><span class="__F__-m">---</span>
<span class="__F__-k">name:</span> <span class="__F__-v">mon-skill</span>
<span class="__F__-k">description:</span> <span class="__F__-s">…</span>
<span class="__F__-m">---</span></div>
</div>
<div id="__F__-ok" class="__F__-ok"><svg width="40" height="40" viewBox="0 0 40 40"><path id="__F__-check" d="M8 21 l8 8 l16 -18" fill="none" stroke="#141413" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/></svg><span>Claude sait faire</span></div>
"""
F2_JS = """
tl.fromTo("#__F__-kick", { opacity: 0, y: -20 }, { opacity: 1, y: 0, duration: 0.6, ease: "power3.out" }, 0.3);
const hw = qa("#__F__-hero .__F__-w");
hw[1].classList.add("__F__-sk");
tl.fromTo(hw[0], { opacity: 0, y: 70, filter: "blur(10px)" }, { opacity: 1, y: 0, filter: "blur(0px)", duration: 0.6, ease: "power3.out" }, 1.45);
tl.fromTo(hw[1], { opacity: 0, scale: 1.3, filter: "blur(16px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.7, ease: "expo.out" }, 1.65);
tl.fromTo("#__F__-folder", { opacity: 0, y: 260, rotation: -3 }, { opacity: 1, y: 0, rotation: 0, duration: 0.9, ease: "power3.out" }, 2.5);
levitate("#__F__-folder", 3.4, 7.8, 14);
tl.fromTo("#__F__-skill", { opacity: 0, x: -260, y: 60, scale: 0.4, rotation: 0 }, { opacity: 1, x: 0, y: -250, scale: 1, rotation: -4, duration: 1.0, ease: "power3.out" }, 3.85);
tl.fromTo("#__F__-skill", { y: -250 }, { y: -268, immediateRender: false, duration: 2.9, ease: "sine.inOut" }, 4.9);
tl.fromTo("#__F__-ok", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.6, ease: "power3.out" }, 5.9);
const ck = q("#__F__-check");
tl.fromTo(ck, { strokeDasharray: 40, strokeDashoffset: 40 }, { strokeDashoffset: 0, duration: 0.5, ease: "power2.out" }, 6.5);
"""

# ───────────────────────── Frame 3 — dossier ─────────────────────────
F3_CSS = """
.__F__-term { left: 80px; top: 470px; width: 920px; }
.__F__-term .__F__-code { font-size: 36px; min-height: 190px; padding-top: 34px; }
.__F__-path { position: absolute; left: 110px; width: 860px; padding: 30px 36px; }
.__F__-path h4 { margin: 0 0 10px; font-family: "JetBrains Mono", monospace; font-weight: 400; font-size: 24px; letter-spacing: .18em; color: rgba(20,20,19,.55); }
.__F__-path .p { font-family: "JetBrains Mono", monospace; font-size: 38px; color: #141413; }
.__F__-path .n { margin-top: 10px; font-size: 30px; color: rgba(20,20,19,.62); }
"""
F3_BODY = f"""
<div id="__F__-badge" class="__F__-badge">ÉTAPE 01</div>
<div id="__F__-title" class="__F__-title" style="top:250px;font-size:150px">{words('__F__', 'Le dossier', '', 't')}</div>
<div id="__F__-term" class="__F__-navy __F__-term">
  <div class="__F__-bar"><span class="d"></span><span class="d"></span><span class="d"></span><em>terminal</em></div>
  <div class="__F__-code"><span class="__F__-m">$ </span><span id="__F__-c1" class="__F__-v"></span><span id="__F__-c2" class="__F__-s"></span><span id="__F__-c3" class="__F__-k"></span><span id="__F__-c4" class="__F__-v"></span><span id="__F__-caret" class="__F__-caret"></span></div>
</div>
<div id="__F__-proj" class="__F__-card __F__-path" style="top:860px"><h4>PROJET · PARTAGÉ AVEC L'ÉQUIPE</h4><div class="p">.claude/skills/mon-skill/</div></div>
<div id="__F__-perso" class="__F__-card __F__-path" style="top:1130px"><h4>PERSO · TOUS TES PROJETS</h4><div class="p">~/.claude/skills/mon-skill/</div></div>
"""
F3_JS = """
tl.fromTo("#__F__-badge", { opacity: 0, scale: 0.8 }, { opacity: 1, scale: 1, duration: 0.5, ease: "power3.out" }, 0.0);
wordsIn("#__F__-title .__F__-w", 0.2, 0.12);
popIn("#__F__-term", 1.0);
typeOn(q("#__F__-c1"), "mkdir -p ", 1.3, 0.5);
typeOn(q("#__F__-c2"), ".claude", 2.4, 0.45);
typeOn(q("#__F__-c3"), "/skills", 3.2, 0.45);
typeOn(q("#__F__-c4"), "/mon-skill", 3.7, 0.5);
caretBlink("#__F__-caret", 0, 7.3);
levitate("#__F__-term", 4.3, 7.3, 10);
tl.fromTo("#__F__-proj", { opacity: 0, x: -380 }, { opacity: 1, x: 0, duration: 0.8, ease: "power3.out" }, 4.3);
tl.fromTo("#__F__-perso", { opacity: 0, x: 380 }, { opacity: 1, x: 0, duration: 0.8, ease: "power3.out" }, 5.85);
levitate("#__F__-proj", 5.1, 7.3, 8);
"""

# ───────────────────────── Frame 4 — en-tête ─────────────────────────
EDITOR = """
<div id="__F__-ed" class="__F__-navy __F__-ed">
  <div class="__F__-bar"><span class="d"></span><span class="d"></span><span class="d"></span><em>SKILL.md</em></div>
  <div class="__F__-code" id="__F__-code">__LINES__</div>
</div>
"""
F4_CSS = """
.__F__-ed { left: 70px; top: 470px; width: 940px; }
.__F__-ed .__F__-code { font-size: 34px; min-height: 470px; }
.__F__-ln { display: block; min-height: 55px; }
.__F__-hl { position: absolute; left: 22px; right: 22px; top: 0; height: 120px; border-radius: 8px; background: rgba(204,120,92,.22); border-left: 4px solid #CC785C; transform-origin: 0 50%; }
.__F__-lab { position: absolute; padding: 20px 28px; font-size: 32px; color: #141413; display: flex; align-items: center; gap: 16px; }
.__F__-lab .__F__-mono { font-size: 26px; color: rgba(20,20,19,.6); }
"""
F4_LINES = ('<div id="__F__-hl" class="__F__-hl" style="top:202px"></div>'
            '<span class="__F__-ln"><span id="__F__-l1" class="__F__-m"></span></span>'
            '<span class="__F__-ln"><span id="__F__-l2k" class="__F__-k"></span><span id="__F__-l2v" class="__F__-v"></span><span id="__F__-ghost2" class="__F__-m">░░░░░░░░</span></span>'
            '<span class="__F__-ln"><span id="__F__-l3k" class="__F__-k"></span><span id="__F__-l3v" class="__F__-s"></span><span id="__F__-ghost3" class="__F__-m">░░░░░░░░░░░░░</span></span>'
            '<span class="__F__-ln"><span id="__F__-l3w" class="__F__-s"></span></span>'
            '<span class="__F__-ln"><span id="__F__-l4" class="__F__-m"></span><span id="__F__-caret" class="__F__-caret"></span></span>')
F4_BODY = f"""
<div id="__F__-badge" class="__F__-badge">ÉTAPE 02</div>
<div id="__F__-title" class="__F__-title" style="top:250px;font-size:120px">{words('__F__', 'Le fichier', '', 't')} <span class="__F__-w __F__-mono" style="font-size:96px;letter-spacing:-.02em">SKILL.md</span></div>
""" + EDITOR.replace("__LINES__", F4_LINES) + """
<div id="__F__-lab1" class="__F__-card __F__-lab" style="left:110px;top:1080px">
  <svg width="40" height="40" viewBox="0 0 40 40"><path id="__F__-a1" d="M20 36 V6 M8 18 L20 6 L32 18" fill="none" stroke="#141413" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
  <span><b style="font-weight:700">name</b> — le nom <span class="__F__-mono">→ /mon-skill</span></span></div>
<div id="__F__-lab2" class="__F__-card __F__-lab" style="left:110px;top:1240px">
  <svg width="40" height="40" viewBox="0 0 40 40"><path id="__F__-a2" d="M20 36 V6 M8 18 L20 6 L32 18" fill="none" stroke="#141413" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
  <span><b style="font-weight:700">description</b> — quoi + quand</span></div>
"""
F4_JS = """
tl.fromTo("#__F__-badge", { opacity: 0, scale: 0.8 }, { opacity: 1, scale: 1, duration: 0.5, ease: "power3.out" }, 0.0);
wordsIn("#__F__-title .__F__-w", 0.25, 0.14);
tl.fromTo("#__F__-ed", { opacity: 0, scale: 0.6, y: 120 }, { opacity: 1, scale: 1, y: 0, duration: 0.9, ease: "expo.out" }, 1.6);
tl.fromTo(["#__F__-ghost2", "#__F__-ghost3"], { opacity: 0 }, { opacity: 0.5, duration: 0.4, stagger: 0.2 }, 4.0);
typeOn(q("#__F__-l1"), "---", 3.1, 0.3);
typeOn(q("#__F__-l4"), "---", 4.4, 0.3);
tl.set("#__F__-ghost2", { display: "none" }, 5.6);
typeOn(q("#__F__-l2k"), "name: ", 5.6, 0.35);
typeOn(q("#__F__-l2v"), "mon-skill", 6.0, 0.5);
tl.fromTo("#__F__-lab1", { opacity: 0, y: 50 }, { opacity: 1, y: 0, duration: 0.7, ease: "power3.out" }, 7.4);
tl.fromTo("#__F__-a1", { strokeDasharray: 60, strokeDashoffset: 60 }, { strokeDashoffset: 0, duration: 0.5, ease: "power2.out" }, 7.7);
tl.set("#__F__-ghost3", { display: "none" }, 10.5);
typeOn(q("#__F__-l3k"), "description: ", 10.5, 0.45);
typeOn(q("#__F__-l3v"), "Rédige un post LinkedIn.", 11.0, 0.7);
typeOn(q("#__F__-l3w"), "  À utiliser quand on demande un post.", 11.75, 0.75);
tl.fromTo("#__F__-hl", { scaleX: 0, opacity: 0 }, { scaleX: 1, opacity: 1, duration: 0.55, ease: "power3.out" }, 12.4);
tl.fromTo("#__F__-lab2", { opacity: 0, y: 50 }, { opacity: 1, y: 0, duration: 0.7, ease: "power3.out" }, 12.5);
tl.fromTo("#__F__-a2", { strokeDasharray: 60, strokeDashoffset: 60 }, { strokeDashoffset: 0, duration: 0.5, ease: "power2.out" }, 12.8);
caretBlink("#__F__-caret", 0, 13.6);
levitate("#__F__-ed", 2.6, 13.66, 10);
"""

# ───────────────────────── Frame 5 — instructions ─────────────────────────
F5_CSS = """
.__F__-ed { left: 70px; top: 430px; width: 940px; }
.__F__-ed .__F__-code { font-size: 32px; height: 300px; }
.__F__-ln { display: block; min-height: 52px; }
.__F__-dim { opacity: .45; }
.__F__-tag { position: absolute; left: 780px; top: 262px; padding: 8px 18px; border-radius: 9999px; border: 1px solid rgba(20,20,19,.3); background: #FAF9F5;
  font-family: "JetBrains Mono", monospace; font-size: 30px; color: #141413; }
.__F__-quote { position: absolute; left: 120px; right: 120px; top: 1345px; padding: 30px 40px; text-align: center; font-family: "EB Garamond", serif; font-style: italic;
  font-size: 58px; line-height: 1.12; color: #141413; }
.__F__-quote small { display: block; margin-top: 12px; font-family: "Inter", sans-serif; font-style: normal; font-size: 22px; letter-spacing: .18em; text-transform: uppercase; color: rgba(20,20,19,.55); }
"""
F5_LINES = ('<span class="__F__-ln __F__-dim __F__-m">---</span>'
            '<span class="__F__-ln __F__-dim"><span class="__F__-k">name: </span><span class="__F__-v">mon-skill</span></span>'
            '<span class="__F__-ln __F__-dim"><span class="__F__-k">description: </span><span class="__F__-s">Rédige un post…</span></span>'
            '<span class="__F__-ln __F__-dim __F__-m">---</span>'
            '<span class="__F__-ln"></span>'
            '<span class="__F__-ln"><span id="__F__-b1" class="__F__-s"></span></span>'
            '<span class="__F__-ln"><span id="__F__-b2" class="__F__-v"></span></span>'
            '<span class="__F__-ln"><span id="__F__-b3" class="__F__-v"></span></span>'
            '<span class="__F__-ln"><span id="__F__-b4" class="__F__-v"></span><span id="__F__-caret" class="__F__-caret"></span></span>')
F5_BODY = f"""
<div id="__F__-badge" class="__F__-badge">ÉTAPE 03</div>
<div id="__F__-title" class="__F__-title" style="top:240px;font-size:118px;left:40px;right:300px;text-align:left;padding-left:30px">{words('__F__', 'Les instructions', '', 't')}</div>
<div id="__F__-tag" class="__F__-tag">.md</div>
""" + EDITOR.replace("__LINES__", F5_LINES) + """
<div id="__F__-quote" class="__F__-card __F__-quote">“comme un brief à un collègue”<small>Markdown · langage naturel</small></div>
"""
F5_JS = """
tl.fromTo("#__F__-badge", { opacity: 0, scale: 0.8 }, { opacity: 1, scale: 1, duration: 0.5, ease: "power3.out" }, 0.0);
wordsIn("#__F__-title .__F__-w", 0.2, 0.14);
tl.fromTo("#__F__-ed", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.6, ease: "power3.out" }, 0.0);
tl.fromTo("#__F__-ed .__F__-code", { height: 300 }, { height: 560, immediateRender: false, duration: 0.9, ease: "power3.inOut" }, 1.3);
typeOn(q("#__F__-b1"), "# Instructions", 2.2, 0.45);
typeOn(q("#__F__-b2"), "1. Lis le sujet donné", 2.75, 0.5);
typeOn(q("#__F__-b3"), "2. Écris 5 lignes, ton direct", 3.3, 0.6);
typeOn(q("#__F__-b4"), "3. Finis par une question", 4.0, 0.55);
tl.fromTo("#__F__-tag", { opacity: 0, scale: 0.5, rotation: -12 }, { opacity: 1, scale: 1, rotation: -6, duration: 0.6, ease: "power3.out" }, 3.85);
caretBlink("#__F__-caret", 0, 6.6);
tl.fromTo("#__F__-quote", { opacity: 0, y: 60, filter: "blur(8px)" }, { opacity: 1, y: 0, filter: "blur(0px)", duration: 0.8, ease: "power3.out" }, 4.7);
levitate("#__F__-quote", 5.5, 6.68, 8);
levitate("#__F__-ed", 2.2, 6.68, 8);
"""

# ───────────────────────── Frame 6 — description ─────────────────────────
SKILLS = [("traduire", "Traduit un texte"), ("post-linkedin", "Rédige un post LinkedIn"), ("revue-code", "Relit une PR"),
          ("resume", "Résume un document"), ("emails", "Répond aux emails")]
F6_CSS = """
.__F__-hub { left: 290px; top: 870px; width: 500px; padding: 26px 30px; font-family: "Inter", sans-serif; font-size: 32px; line-height: 1.3; border-radius: 26px 26px 8px 26px; }
.__F__-hub small { display: block; font-family: "JetBrains Mono", monospace; font-size: 20px; letter-spacing: .14em; color: rgba(250,249,245,.5); margin-bottom: 8px; }
.__F__-sc { position: absolute; width: 300px; padding: 20px 22px; }
.__F__-sc b { display: block; font-family: "JetBrains Mono", monospace; font-weight: 400; font-size: 26px; color: #141413; }
.__F__-sc span { display: block; margin-top: 6px; font-size: 22px; color: rgba(20,20,19,.6); }
.__F__-on { border: 2px solid #CC785C !important; }
.__F__-load { position: absolute; left: 50%; top: 1440px; margin-left: -170px; width: 340px; height: 76px; border-radius: 9999px; background: #FAF9F5; border: 1px solid rgba(20,20,19,.25);
  display: flex; align-items: center; justify-content: center; font-family: "JetBrains Mono", monospace; font-size: 28px; letter-spacing: .06em; }
"""
cx, cy, rx, ry = 540, 960, 370, 330
pos = []
for i in range(5):
    a = -math.pi / 2 + i * 2 * math.pi / 5 + 0.35
    pos.append((cx + rx * math.cos(a) - 150, cy + ry * math.sin(a) - 55))
F6_BODY = f"""
<div id="__F__-kick" class="__F__-kicker" style="top:150px"><b>✱</b>Le secret</div>
<div id="__F__-title" class="__F__-title" style="top:220px;font-size:150px">{words('__F__', 'La description.', '', 't')}</div>
<svg width="1080" height="1920" style="position:absolute;left:0;top:0;overflow:visible"><path id="__F__-link" d="M0 0" fill="none" stroke="#141413" stroke-width="3" stroke-dasharray="10 10"/></svg>
""" + "\n".join(
    f'<div id="__F__-s{i}" class="__F__-card __F__-sc" data-layout-allow-overlap data-layout-allow-occlusion style="left:{x:.0f}px;top:{y:.0f}px"><b>/{n}</b><span>{d}</span></div>'
    for i, ((n, d), (x, y)) in enumerate(zip(SKILLS, pos))) + """
<div id="__F__-hub" class="__F__-navy __F__-hub"><small>TA DEMANDE</small>« Écris un post LinkedIn sur mon lancement »</div>
<div id="__F__-load" class="__F__-load">skill chargé ✓</div>
"""
F6_JS = f"""
tl.fromTo("#__F__-kick", {{ opacity: 0, y: -20 }}, {{ opacity: 1, y: 0, duration: 0.6, ease: "power3.out" }}, 0.1);
wordsIn("#__F__-title .__F__-w", 0.9, 0.18);
popIn("#__F__-hub", 1.4);
const POS = {json.dumps([[round(x), round(y)] for x, y in pos])};
for (let i = 0; i < 5; i++) {{
  tl.fromTo("#__F__-s" + i, {{ opacity: 0, rotationY: -80, scale: 0.7, transformPerspective: 900 }},
    {{ opacity: 1, rotationY: 0, scale: 1, duration: 0.7, ease: "power3.out" }}, 1.9 + i * 0.16);
  // dérive orbitale finie et douce
  const a0 = -Math.PI / 2 + i * 2 * Math.PI / 5 + 0.35;
  const o = {{ a: 0 }};
  tl.fromTo(o, {{ a: 0 }}, {{ a: 0.16, duration: 4.6, ease: "sine.inOut", onUpdate: () => {{
    if (i === 1 && tl.time() > 4.0) return;
    const el = q("#__F__-s" + i);
    el.style.left = ({cx} + {rx} * Math.cos(a0 + o.a) - 150).toFixed(1) + "px";
    el.style.top = ({cy} + {ry} * Math.sin(a0 + o.a) - 55).toFixed(1) + "px";
  }} }}, 2.0);
  tl.fromTo("#__F__-s" + i, {{ backgroundColor: "#EFE9DE" }}, {{ immediateRender: false, keyframes: {{ backgroundColor: ["#EFE9DE", "#FAF9F5", "#EFE9DE"] }}, duration: 0.35, ease: "none" }}, 3.3 + i * 0.12);
}}
// la carte post-linkedin s'allume et rejoint la demande
tl.set("#__F__-s1", {{ attr: {{ class: "__F__-card __F__-sc __F__-on" }} }}, 4.0);
tl.fromTo("#__F__-s1", {{ x: 0, y: 0, scale: 1 }}, {{ immediateRender: false, x: () => 390 - parseFloat(q("#__F__-s1").style.left), y: () => 640 - parseFloat(q("#__F__-s1").style.top), scale: 1.18, duration: 0.9, ease: "power3.inOut" }}, 4.0);
[0, 2, 3, 4].forEach((i) => tl.fromTo("#__F__-s" + i, {{ filter: "blur(0px)", opacity: 1 }}, {{ immediateRender: false, filter: "blur(5px)", opacity: 0.4, duration: 0.7, ease: "power2.out" }}, 4.1));
tl.set("#__F__-link", {{ attr: {{ d: "M540 790 L540 870" }} }}, 0);
tl.fromTo("#__F__-link", {{ opacity: 0, strokeDashoffset: 80 }}, {{ opacity: 1, strokeDashoffset: 0, duration: 0.5, ease: "power2.out" }}, 5.6);
tl.fromTo("#__F__-load", {{ opacity: 0, y: 40 }}, {{ opacity: 1, y: 0, duration: 0.6, ease: "power3.out" }}, 5.85);
"""

# ───────────────────────── Frame 7 — slash ─────────────────────────
F7_CSS = """
.__F__-cmd { left: 90px; top: 600px; width: 900px; height: 130px; display: flex; align-items: center; padding: 0 40px; font-size: 40px; border-radius: 9999px; }
.__F__-ph { color: rgba(250,249,245,.38); font-family: "Inter", sans-serif; font-size: 36px; }
.__F__-menu { left: 130px; top: 770px; width: 820px; padding: 14px; transform-origin: 50% 0; }
.__F__-row { display: flex; justify-content: space-between; align-items: center; padding: 22px 26px; border-radius: 8px; font-size: 26px; color: rgba(20,20,19,.6); }
.__F__-row b { font-family: "JetBrains Mono", monospace; font-weight: 400; font-size: 34px; color: #141413; }
.__F__-row.on { background: rgba(204,120,92,.16); box-shadow: inset 4px 0 0 #CC785C; }
.__F__-key { position: absolute; left: 430px; top: 1210px; width: 220px; height: 220px; border-radius: 34px; background: #FAF9F5; border: 1px solid rgba(20,20,19,.2);
  box-shadow: 0 10px 0 #ECE3D4, 0 12px 0 rgba(20,20,19,.2), 0 24px 40px rgba(20,20,19,.12); display: flex; align-items: center; justify-content: center;
  font-family: "JetBrains Mono", monospace; font-size: 130px; color: #141413; }
.__F__-go { position: absolute; left: 50%; top: 1250px; margin-left: -190px; width: 380px; height: 84px; border-radius: 9999px; background: #FAF9F5; border: 1px solid rgba(20,20,19,.25);
  display: flex; align-items: center; justify-content: center; font-family: "JetBrains Mono", monospace; font-size: 30px; }
"""
F7_BODY = f"""
<div id="__F__-kick" class="__F__-kicker" style="top:170px"><b>✱</b>Raccourci</div>
<div id="__F__-title" class="__F__-title" style="top:240px;font-size:128px">{words('__F__', 'Appelle-le toi-même', '', 't')}</div>
<div id="__F__-cmd" class="__F__-navy __F__-cmd"><span id="__F__-ph" class="__F__-ph">Demande à Claude Code…</span><span id="__F__-sl" class="__F__-s"></span><span id="__F__-nm" class="__F__-v"></span><span id="__F__-caret" class="__F__-caret"></span></div>
<div id="__F__-menu" class="__F__-card __F__-menu">
  <div id="__F__-r0" class="__F__-row"><b>/mon-skill</b><span>post LinkedIn</span></div>
  <div class="__F__-row"><b>/revue-code</b><span>relire une PR</span></div>
  <div class="__F__-row"><b>/resume</b><span>résumer</span></div>
</div>
<div id="__F__-key" class="__F__-key">/</div>
<div id="__F__-go" class="__F__-go">↵ lancé</div>
"""
F7_JS = """
tl.fromTo("#__F__-kick", { opacity: 0, y: -20 }, { opacity: 1, y: 0, duration: 0.6, ease: "power3.out" }, 0.05);
wordsIn("#__F__-title .__F__-w", 0.6, 0.15);
popIn("#__F__-cmd", 0.3);
caretBlink("#__F__-caret", 0, 6.2);
tl.fromTo("#__F__-key", { opacity: 0, y: -260, rotation: -8 }, { opacity: 1, y: 0, rotation: 0, duration: 0.8, ease: "power3.out" }, 1.9);
tl.fromTo("#__F__-key", { scale: 1 }, { immediateRender: false, keyframes: { scale: [1, 0.9, 1] }, duration: 0.35, ease: "power2.out" }, 3.0);
tl.set("#__F__-ph", { display: "none" }, 3.1);
typeOn(q("#__F__-sl"), "/", 3.1, 0.05);
tl.fromTo("#__F__-menu", { opacity: 0, scaleY: 0.6, y: -20 }, { opacity: 1, scaleY: 1, y: 0, duration: 0.6, ease: "power3.out" }, 3.2);
tl.fromTo("#__F__-key", { opacity: 1 }, { immediateRender: false, opacity: 0.0, y: 60, duration: 0.5, ease: "power2.in" }, 4.6);
typeOn(q("#__F__-nm"), "mon-skill", 4.85, 0.55);
tl.set("#__F__-r0", { attr: { class: "__F__-row on" } }, 5.2);
tl.fromTo("#__F__-menu", { opacity: 1, scaleY: 1 }, { immediateRender: false, opacity: 0, scaleY: 0.7, duration: 0.4, ease: "power2.in" }, 5.6);
tl.fromTo("#__F__-go", { opacity: 0, scale: 0.8 }, { opacity: 1, scale: 1, duration: 0.5, ease: "power3.out" }, 5.7);
tl.fromTo("#__F__-cmd", { boxShadow: "0 0 0 0 rgba(204,120,92,0)" }, { keyframes: { boxShadow: ["0 0 0 0 rgba(204,120,92,0)", "0 0 0 18px rgba(204,120,92,.25)", "0 0 0 30px rgba(204,120,92,0)"] }, duration: 0.6, ease: "none" }, 5.65);
"""

# ───────────────────────── Frame 8 — fichiers ─────────────────────────
F8_CSS = """
.__F__-row { position: absolute; display: flex; align-items: center; gap: 22px; padding: 22px 30px; font-family: "JetBrains Mono", monospace; font-size: 38px; color: #141413; }
.__F__-row i { font-style: normal; font-size: 26px; color: rgba(20,20,19,.5); font-family: "Inter", sans-serif; }
.__F__-ico { width: 46px; height: 56px; border-radius: 6px; border: 2px solid rgba(20,20,19,.35); background: #FAF9F5; position: relative; }
.__F__-ico::after { content: ""; position: absolute; left: 9px; right: 9px; top: 16px; height: 4px; background: rgba(20,20,19,.25); box-shadow: 0 10px 0 rgba(20,20,19,.25), 0 20px 0 rgba(20,20,19,.25); }
.__F__-skillrow { left: 230px; top: 690px; width: 600px; }
.__F__-wait { border-style: dashed !important; }
.__F__-tree { position: absolute; left: 0; top: 0; overflow: visible; }
"""
F8_BODY = f"""
<div id="__F__-title" class="__F__-title" style="top:200px;font-size:140px">{words('__F__', 'Besoin de plus ?', '', 't')}</div>
<div id="__F__-folder" style="position:absolute;left:110px;top:470px;width:220px;height:170px">{folder_svg('__F__', 220, 170)}</div>
<div id="__F__-fname" class="__F__-mono" style="position:absolute;left:360px;top:530px;font-size:44px">mon-skill/</div>
<svg class="__F__-tree" width="1080" height="1920"><path id="__F__-tr" d="M200 640 V1300 M200 760 H230 M200 940 H230 M200 1120 H230 M200 1300 H230" fill="none" stroke="rgba(20,20,19,.3)" stroke-width="3"/></svg>
<div id="__F__-f0" class="__F__-navy __F__-row" style="left:230px;top:715px;color:#FAF9F5"><span class="__F__-ico" style="background:#252320;border-color:rgba(250,249,245,.4)"></span>SKILL.md</div>
<div id="__F__-f1" class="__F__-card __F__-row" style="left:230px;top:895px"><span class="__F__-ico"></span>exemples.md <i>cas concrets</i></div>
<div id="__F__-f2" class="__F__-card __F__-row" style="left:230px;top:1075px"><span class="__F__-ico"></span>reference.md <i>détails</i></div>
<div id="__F__-f3" class="__F__-card __F__-row" style="left:230px;top:1255px"><span class="__F__-ico" style="border-radius:50%"></span>scripts/ <i>outils</i></div>
<div id="__F__-kick" class="__F__-kicker" style="top:1450px"><b>✱</b>Chargés à la demande</div>
"""
F8_JS = """
wordsIn("#__F__-title .__F__-w", 0.1, 0.13);
popIn("#__F__-folder", 0.2);
tl.fromTo("#__F__-fname", { opacity: 0, x: -30 }, { opacity: 1, x: 0, duration: 0.6, ease: "power3.out" }, 0.4);
tl.fromTo("#__F__-f0", { opacity: 0, x: -40 }, { opacity: 1, x: 0, duration: 0.6, ease: "power3.out" }, 0.6);
tl.fromTo("#__F__-tr", { strokeDasharray: 1200, strokeDashoffset: 1200 }, { strokeDashoffset: 0, duration: 1.4, ease: "power2.inOut" }, 1.0);
[[1, 2.45], [2, 3.75], [3, 4.55]].forEach(([i, t]) => {
  tl.fromTo("#__F__-f" + i, { opacity: 0, x: -120, y: -160 * i, scale: 0.6 }, { opacity: 1, x: 0, y: 0, scale: 1, duration: 0.8, ease: "power3.out" }, t);
});
levitate("#__F__-folder", 1.0, 8.4, 10);
[1, 2, 3].forEach((i) => {
  tl.set("#__F__-f" + i, { attr: { class: "__F__-card __F__-row __F__-wait" } }, 6.2);
  tl.fromTo("#__F__-f" + i, { opacity: 1 }, { immediateRender: false, opacity: 0.5, duration: 0.5, ease: "power2.out" }, 6.2);
});
tl.fromTo("#__F__-kick", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.6, ease: "power3.out" }, 6.4);
tl.fromTo("#__F__-f2", { opacity: 0.5, scale: 1 }, { immediateRender: false, opacity: 1, scale: 1.05, duration: 0.45, ease: "power3.out" }, 7.65);
"""

# ───────────────────────── Frame 9 — CTA ─────────────────────────
F9_CSS = """
.__F__-l { position: absolute; left: 60px; right: 60px; text-align: center; font-family: "EB Garamond", serif; letter-spacing: -.02em; line-height: 1.02; color: #141413; }
.__F__-glow { position: absolute; left: 290px; top: 830px; width: 500px; height: 400px; border-radius: 50%; background: radial-gradient(closest-side, rgba(204,120,92,.28), rgba(204,120,92,0)); }
.__F__-cta { position: absolute; left: 50%; top: 1290px; margin-left: -270px; width: 540px; height: 110px; border-radius: 9999px; background: #CC785C; color: #FAF9F5;
  display: flex; align-items: center; justify-content: center; font-size: 44px; font-weight: 700; letter-spacing: -.01em; }
.__F__-cmdline { position: absolute; left: 0; right: 0; top: 1440px; text-align: center; font-family: "JetBrains Mono", monospace; font-size: 30px; color: rgba(20,20,19,.7); }
.__F__-mini { position: absolute; left: 460px; top: 640px; width: 160px; padding: 12px 14px; font-size: 20px; border-radius: 8px; }
"""
F9_BODY = f"""
<div id="__F__-l1" class="__F__-l" style="top:200px;font-size:140px">1 dossier</div>
<div id="__F__-l2" class="__F__-l" style="top:350px;font-size:140px">+ 1 fichier</div>
<div id="__F__-l3" class="__F__-l" style="top:520px;font-size:96px;font-style:italic">{words('__F__', '= un nouveau talent', '', 'x')}</div>
<div id="__F__-glow" class="__F__-glow"></div>
<div id="__F__-folder" style="position:absolute;left:340px;top:870px;width:400px;height:310px">{folder_svg('__F__', 400, 310, 1, 'ton-skill/')}</div>
<div id="__F__-mini" class="__F__-navy __F__-mini">SKILL.md</div>
<div id="__F__-cta" class="__F__-cta">À toi de jouer →</div>
<div class="__F__-cmdline"><span id="__F__-cmd"></span><span id="__F__-caret" class="__F__-caret"></span></div>
"""
F9_JS = """
popIn("#__F__-folder", 0.2);
tl.fromTo("#__F__-l1", { opacity: 0, y: 60, filter: "blur(8px)" }, { opacity: 1, y: 0, filter: "blur(0px)", duration: 0.7, ease: "power3.out" }, 0.35);
tl.fromTo("#__F__-l2", { opacity: 0, y: 60, filter: "blur(8px)" }, { opacity: 1, y: 0, filter: "blur(0px)", duration: 0.7, ease: "power3.out" }, 1.5);
tl.fromTo("#__F__-mini", { opacity: 0, y: -40 }, { opacity: 1, y: 0, duration: 0.4, ease: "power3.out" }, 1.6);
tl.fromTo("#__F__-mini", { y: 0, scale: 1 }, { immediateRender: false, y: 330, scale: 0.6, duration: 0.6, ease: "power3.in" }, 2.0);
tl.set("#__F__-mini", { opacity: 0 }, 2.6);
tl.fromTo("#__F__-folder", { scale: 1 }, { immediateRender: false, keyframes: { scale: [1, 1.05, 1] }, duration: 0.4, ease: "power2.out" }, 2.6);
wordsIn("#__F__-l3 .__F__-w", 2.7, 0.28, 40);
tl.fromTo("#__F__-glow", { opacity: 0, scale: 0.7 }, { opacity: 1, scale: 1.1, duration: 1.6, ease: "power2.out" }, 2.7);
tl.fromTo("#__F__-cta", { opacity: 0, scale: 0.85, y: 30 }, { opacity: 1, scale: 1, y: 0, duration: 0.7, ease: "power3.out" }, 4.4);
typeOn(q("#__F__-cmd"), "mkdir -p ~/.claude/skills/ton-skill", 5.0, 1.0);
caretBlink("#__F__-caret", 0, 6.1);
levitate("#__F__-folder", 3.0, 6.1, 10);
tl.to(R, { opacity: 0, duration: 0.35, ease: "power2.in" }, 6.14);
"""

FRAMES = [
    (1, "hook", F1_BODY, F1_CSS, F1_JS),
    (2, "concept", F2_BODY, F2_CSS, F2_JS),
    (3, "dossier", F3_BODY, F3_CSS, F3_JS),
    (4, "entete", F4_BODY, F4_CSS, F4_JS),
    (5, "instructions", F5_BODY, F5_CSS, F5_JS),
    (6, "description", F6_BODY, F6_CSS, F6_JS),
    (7, "slash", F7_BODY, F7_CSS, F7_JS),
    (8, "fichiers", F8_BODY, F8_CSS, F8_JS),
    (9, "cta", F9_BODY, F9_CSS, F9_JS),
]
only = set(map(int, sys.argv[2:])) if len(sys.argv) > 2 else None
for n, slug, body, css, js in FRAMES:
    if only and n not in only:
        continue
    write_frame(n, slug, body, css, js)
