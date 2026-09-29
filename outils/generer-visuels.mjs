// Génère les visuels vectoriels des produits dans assets/produits/.
// Usage : node outils/generer-visuels.mjs
// Pour utiliser de vraies photos, déposez simplement un .jpg/.webp dans
// assets/produits/ et changez le champ `image` du produit dans assets/js/donnees.js.

import { writeFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const OUT = join(dirname(fileURLToPath(import.meta.url)), "..", "assets", "produits");
mkdirSync(OUT, { recursive: true });

// Générateur pseudo-aléatoire déterministe : les visuels restent identiques d'une génération à l'autre.
function rng(seed) {
  let s = seed >>> 0;
  return () => ((s = (s * 1664525 + 1013904223) >>> 0) / 2 ** 32);
}

const frame = (bg1, bg2, body, defs = "") => `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 600" width="600" height="600">
<defs>
<radialGradient id="bg" cx="50%" cy="36%" r="78%"><stop offset="0" stop-color="${bg1}"/><stop offset="1" stop-color="${bg2}"/></radialGradient>
<linearGradient id="table" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".12"/></linearGradient>
<filter id="flou" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="16"/></filter>
<filter id="flou2" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="5"/></filter>
<linearGradient id="volH" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".22"/><stop offset=".35" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".32"/></linearGradient>
<linearGradient id="cyl" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#000" stop-opacity=".38"/><stop offset=".32" stop-color="#fff" stop-opacity=".22"/><stop offset=".5" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".42"/></linearGradient>
<linearGradient id="cylV" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#000" stop-opacity=".30"/><stop offset=".3" stop-color="#fff" stop-opacity=".20"/><stop offset=".55" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".45"/></linearGradient>
<linearGradient id="metal" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f4f4f2"/><stop offset=".45" stop-color="#b9bcc0"/><stop offset=".55" stop-color="#8d9196"/><stop offset="1" stop-color="#d9dadc"/></linearGradient>
${defs}
</defs>
<rect width="600" height="600" fill="url(#bg)"/>
<rect y="380" width="600" height="220" fill="url(#table)"/>
${body}
</svg>`;

const ombre = (cx, cy, rx, ry, o = 0.28) =>
  `<ellipse cx="${cx}" cy="${cy}" rx="${rx}" ry="${ry}" fill="#1a1208" opacity="${o}" filter="url(#flou)"/>`;

// ---------- Motifs de pagne ----------
const motifs = {
  cercles: (id, [a, b, c, d]) => `<pattern id="${id}" width="64" height="64" patternUnits="userSpaceOnUse">
<rect width="64" height="64" fill="${a}"/><circle cx="32" cy="32" r="27" fill="${b}"/><circle cx="32" cy="32" r="19" fill="${c}"/>
<circle cx="32" cy="32" r="11" fill="${d}"/><circle cx="32" cy="32" r="4" fill="${a}"/>
<circle cx="0" cy="0" r="6" fill="${d}"/><circle cx="64" cy="0" r="6" fill="${d}"/><circle cx="0" cy="64" r="6" fill="${d}"/><circle cx="64" cy="64" r="6" fill="${d}"/></pattern>`,
  eventail: (id, [a, b, c, d]) => `<pattern id="${id}" width="56" height="36" patternUnits="userSpaceOnUse">
<rect width="56" height="36" fill="${a}"/>
<path d="M0 36 A28 28 0 0 1 56 36Z" fill="${b}"/><path d="M8 36 A20 20 0 0 1 48 36Z" fill="${c}"/><path d="M16 36 A12 12 0 0 1 40 36Z" fill="${d}"/>
<path d="M-28 18 A28 28 0 0 1 28 18" fill="none" stroke="${d}" stroke-width="2"/><path d="M28 18 A28 28 0 0 1 84 18" fill="none" stroke="${d}" stroke-width="2"/></pattern>`,
  losanges: (id, [a, b, c, d]) => `<pattern id="${id}" width="52" height="52" patternUnits="userSpaceOnUse">
<rect width="52" height="52" fill="${a}"/><path d="M26 2 L50 26 L26 50 L2 26Z" fill="${b}"/><path d="M26 12 L40 26 L26 40 L12 26Z" fill="${c}"/>
<circle cx="26" cy="26" r="4" fill="${d}"/><circle cx="0" cy="0" r="4" fill="${d}"/><circle cx="52" cy="0" r="4" fill="${d}"/><circle cx="0" cy="52" r="4" fill="${d}"/><circle cx="52" cy="52" r="4" fill="${d}"/></pattern>`,
  kente: (id, [a, b, c, d]) => `<pattern id="${id}" width="96" height="96" patternUnits="userSpaceOnUse">
<rect width="96" height="96" fill="${a}"/>
<rect x="0" y="0" width="48" height="48" fill="${b}"/><rect x="48" y="48" width="48" height="48" fill="${b}"/>
<rect x="0" y="20" width="48" height="8" fill="${c}"/><rect x="48" y="68" width="48" height="8" fill="${c}"/>
<rect x="68" y="0" width="8" height="48" fill="${d}"/><rect x="20" y="48" width="8" height="48" fill="${d}"/>
<rect x="0" y="44" width="96" height="3" fill="${d}"/><rect x="0" y="92" width="96" height="3" fill="${c}"/>
<rect x="8" y="6" width="6" height="6" fill="${d}"/><rect x="56" y="54" width="6" height="6" fill="${d}"/></pattern>`,
  feuilles: (id, [a, b, c, d]) => `<pattern id="${id}" width="70" height="70" patternUnits="userSpaceOnUse">
<rect width="70" height="70" fill="${a}"/>
<ellipse cx="20" cy="20" rx="17" ry="7" transform="rotate(-35 20 20)" fill="${b}"/><path d="M7 29 L33 11" stroke="${c}" stroke-width="2"/>
<ellipse cx="52" cy="52" rx="17" ry="7" transform="rotate(35 52 52)" fill="${c}"/><path d="M39 43 L65 61" stroke="${b}" stroke-width="2"/>
<circle cx="52" cy="17" r="5" fill="${d}"/><circle cx="17" cy="53" r="5" fill="${d}"/></pattern>`,
  damas: (id, [a, b]) => `<pattern id="${id}" width="60" height="60" patternUnits="userSpaceOnUse">
<rect width="60" height="60" fill="${a}"/>
<path d="M30 6 C40 18 40 24 30 30 C20 24 20 18 30 6Z M30 54 C40 42 40 36 30 30 C20 36 20 42 30 54Z M6 30 C18 20 24 20 30 30 C24 40 18 40 6 30Z M54 30 C42 20 36 20 30 30 C36 40 42 40 54 30Z" fill="${b}" opacity=".55"/>
<circle cx="0" cy="0" r="5" fill="${b}" opacity=".45"/><circle cx="60" cy="0" r="5" fill="${b}" opacity=".45"/><circle cx="0" cy="60" r="5" fill="${b}" opacity=".45"/><circle cx="60" cy="60" r="5" fill="${b}" opacity=".45"/></pattern>`,
  serge: (id, [a, b]) => `<pattern id="${id}" width="10" height="10" patternUnits="userSpaceOnUse">
<rect width="10" height="10" fill="${a}"/><path d="M-2 12 L12 -2 M-7 7 L7 -7 M3 17 L17 3" stroke="${b}" stroke-width="2.2" opacity=".55"/></pattern>`,
  toile: (id, [a, b]) => `<pattern id="${id}" width="6" height="6" patternUnits="userSpaceOnUse">
<rect width="6" height="6" fill="${a}"/><path d="M0 3 H6 M3 0 V6" stroke="${b}" stroke-width=".8" opacity=".35"/></pattern>`,
  points: (id, [a, b]) => `<pattern id="${id}" width="9" height="9" patternUnits="userSpaceOnUse">
<rect width="9" height="9" fill="${a}"/><circle cx="4.5" cy="4.5" r="1.3" fill="${b}"/></pattern>`,
};

// Pile de pagnes pliés, vue de face.
function pile(couches, { x = 105, w = 390, h = 78, base = 440 } = {}) {
  let out = ombre(300, base + 26, w / 2 + 10, 26);
  couches.forEach((fill, i) => {
    const y = base - (i + 1) * h + i * 4;
    const dx = i % 2 ? 14 : -6;
    const X = x + dx, W = w - 12 * i * 0;
    const r = h / 2;
    // Bord plié arrondi à gauche, tranche en couches à droite
    const d = `M${X + r} ${y} H${X + W - 8} Q${X + W} ${y} ${X + W} ${y + 8} V${y + h - 8} Q${X + W} ${y + h} ${X + W - 8} ${y + h} H${X + r} A${r} ${r} 0 0 1 ${X + r} ${y}Z`;
    out += `<path d="${d}" fill="url(#${fill})"/>`;
    out += `<path d="${d}" fill="url(#volH)"/>`;
    // pli
    out += `<path d="M${X + r} ${y + 3} A${r - 3} ${r - 3} 0 0 0 ${X + r} ${y + h - 3}" fill="none" stroke="#000" stroke-opacity=".28" stroke-width="3"/>`;
    out += `<path d="M${X + r + 10} ${y + 6} A${r - 8} ${r - 8} 0 0 0 ${X + r + 10} ${y + h - 6}" fill="none" stroke="#fff" stroke-opacity=".18" stroke-width="2"/>`;
    // tranche
    for (let k = 1; k < 5; k++) {
      const yy = y + (h * k) / 5;
      out += `<path d="M${X + W - 60} ${yy} H${X + W - 2}" stroke="#000" stroke-opacity=".22" stroke-width="1.5"/>`;
    }
  });
  return out;
}

function etiquette(x, y, texte, rot = -8) {
  return `<g transform="rotate(${rot} ${x} ${y})">
<path d="M${x - 70} ${y - 20} Q${x - 110} ${y - 50} ${x - 140} ${y - 30}" fill="none" stroke="#5a4630" stroke-width="2"/>
<path d="M${x - 70} ${y - 26} H${x + 40} V${y + 26} H${x - 70} L${x - 86} ${y}Z" fill="#f6efe2" stroke="#d8ccb6" stroke-width="1.5"/>
<circle cx="${x - 68}" cy="${y}" r="5" fill="none" stroke="#5a4630" stroke-width="2"/>
<text x="${x - 16}" y="${y + 8}" text-anchor="middle" font-family="Georgia, 'Times New Roman', serif" font-size="22" font-style="italic" fill="#2b2118">${texte}</text></g>`;
}

// Rouleau de tissu couché avec un pan déroulé devant.
function rouleau(fill, { teinteBout = "#00000055" } = {}) {
  const x1 = 130, x2 = 470, yT = 210, yB = 320, ry = (yB - yT) / 2, rx = 24;
  let out = ombre(300, 470, 230, 26);
  // pan déroulé
  out += `<path d="M${x1 + 6} ${yB - 6} H${x2} C${x2 + 6} 380 ${x2 + 18} 420 ${x2 + 10} 462 H${x1 + 20} C${x1 + 26} 420 ${x1 + 10} 380 ${x1 + 6} ${yB - 6}Z" fill="url(#${fill})"/>`;
  out += `<path d="M${x1 + 6} ${yB - 6} H${x2} C${x2 + 6} 380 ${x2 + 18} 420 ${x2 + 10} 462 H${x1 + 20} C${x1 + 26} 420 ${x1 + 10} 380 ${x1 + 6} ${yB - 6}Z" fill="url(#pan)"/>`;
  out += `<path d="M${x1 + 20} 462 H${x2 + 10}" stroke="#000" stroke-opacity=".25" stroke-width="3"/>`;
  // corps
  const corps = `M${x1} ${yT} H${x2} A${rx} ${ry} 0 0 1 ${x2} ${yB} H${x1}Z`;
  out += `<path d="${corps}" fill="url(#${fill})"/><path d="${corps}" fill="url(#cylV)"/>`;
  // bout avec spirale
  out += `<ellipse cx="${x1}" cy="${(yT + yB) / 2}" rx="${rx}" ry="${ry}" fill="url(#${fill})"/>`;
  out += `<ellipse cx="${x1}" cy="${(yT + yB) / 2}" rx="${rx}" ry="${ry}" fill="${teinteBout}"/>`;
  for (let k = 1; k <= 6; k++) {
    out += `<ellipse cx="${x1 + k * 0.4}" cy="${(yT + yB) / 2}" rx="${rx - k * 3}" ry="${ry - k * 7}" fill="none" stroke="#000" stroke-opacity=".22" stroke-width="1.2"/>`;
  }
  out += `<ellipse cx="${x1 + 3}" cy="${(yT + yB) / 2}" rx="7" ry="13" fill="#caa877"/><ellipse cx="${x1 + 4}" cy="${(yT + yB) / 2}" rx="4" ry="8" fill="#3b2b1a"/>`;
  return out;
}
const defPan = `<linearGradient id="pan" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#000" stop-opacity=".35"/><stop offset=".25" stop-color="#000" stop-opacity=".05"/><stop offset="1" stop-color="#fff" stop-opacity=".08"/></linearGradient>`;

// Bobine de fil debout.
function bobine(x, yb, w, h, couleur) {
  const fl = w / 2 + 12;
  let out = ombre(x + 10, yb + 8, fl + 10, 14, 0.3);
  out += `<ellipse cx="${x}" cy="${yb}" rx="${fl}" ry="12" fill="#8a5f34"/>`;
  out += `<rect x="${x - fl}" y="${yb - 10}" width="${fl * 2}" height="10" fill="#b98753"/>`;
  out += `<ellipse cx="${x}" cy="${yb - 10}" rx="${fl}" ry="12" fill="#d3a570"/>`;
  out += `<rect x="${x - w / 2}" y="${yb - 10 - h}" width="${w}" height="${h}" fill="${couleur}"/>`;
  for (let yy = yb - 10 - h + 4; yy < yb - 12; yy += 4) {
    out += `<path d="M${x - w / 2} ${yy} Q${x} ${yy + 3} ${x + w / 2} ${yy}" stroke="#000" stroke-opacity=".13" fill="none"/>`;
  }
  out += `<rect x="${x - w / 2}" y="${yb - 10 - h}" width="${w}" height="${h}" fill="url(#cyl)"/>`;
  const yt = yb - 10 - h;
  out += `<rect x="${x - fl}" y="${yt - 10}" width="${fl * 2}" height="10" fill="#b98753"/>`;
  out += `<ellipse cx="${x}" cy="${yt}" rx="${fl}" ry="12" fill="#a8763f"/>`;
  out += `<ellipse cx="${x}" cy="${yt - 10}" rx="${fl}" ry="12" fill="#e2b882"/>`;
  out += `<ellipse cx="${x}" cy="${yt - 10}" rx="9" ry="4" fill="#4a3320"/>`;
  return out;
}

function bouton(cx, cy, r, c, trous = 4, rot = 0) {
  let out = `<ellipse cx="${cx + 5}" cy="${cy + 7}" rx="${r}" ry="${r * 0.9}" fill="#1a1208" opacity=".28" filter="url(#flou2)"/>`;
  out += `<g transform="rotate(${rot} ${cx} ${cy})">`;
  out += `<circle cx="${cx}" cy="${cy}" r="${r}" fill="${c}"/>`;
  out += `<circle cx="${cx}" cy="${cy}" r="${r}" fill="url(#bomb)"/>`;
  out += `<circle cx="${cx}" cy="${cy}" r="${r * 0.72}" fill="#000" opacity=".12"/>`;
  out += `<circle cx="${cx}" cy="${cy}" r="${r * 0.7}" fill="none" stroke="#fff" stroke-opacity=".25" stroke-width="1.5"/>`;
  const d = r * 0.22, hr = Math.max(2.5, r * 0.09);
  const pts = trous === 4 ? [[-d, -d], [d, -d], [-d, d], [d, d]] : [[-d, 0], [d, 0]];
  pts.forEach(([a, b]) => (out += `<circle cx="${cx + a}" cy="${cy + b}" r="${hr}" fill="#1c140c" opacity=".75"/>`));
  out += `<path d="M${cx - r * 0.7} ${cy - r * 0.45} A${r * 0.85} ${r * 0.85} 0 0 1 ${cx + r * 0.2} ${cy - r * 0.82}" fill="none" stroke="#fff" stroke-opacity=".45" stroke-width="${r * 0.08}" stroke-linecap="round"/>`;
  out += `</g>`;
  return out;
}
const defBomb = `<radialGradient id="bomb" cx="35%" cy="30%" r="80%"><stop offset="0" stop-color="#fff" stop-opacity=".30"/><stop offset=".6" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".3"/></radialGradient>`;

function fermeture(x, y, long, couleur, rot) {
  let out = `<g transform="rotate(${rot} ${x} ${y})">`;
  out += `<rect x="${x - 34}" y="${y + 8}" width="70" height="${long}" rx="4" fill="#1a1208" opacity=".22" filter="url(#flou2)"/>`;
  out += `<rect x="${x - 32}" y="${y}" width="64" height="${long}" rx="3" fill="${couleur}"/>`;
  out += `<rect x="${x - 32}" y="${y}" width="64" height="${long}" rx="3" fill="url(#bande)"/>`;
  out += `<path d="M${x - 26} ${y} V${y + long} M${x + 26} ${y} V${y + long}" stroke="#000" stroke-opacity=".2" stroke-dasharray="4 4"/>`;
  for (let t = y + 70; t < y + long - 8; t += 9) {
    out += `<rect x="${x - 9}" y="${t}" width="10" height="5" rx="1.5" fill="url(#metal)"/>`;
    out += `<rect x="${x - 1}" y="${t + 4.5}" width="10" height="5" rx="1.5" fill="url(#metal)"/>`;
  }
  // partie ouverte
  out += `<path d="M${x - 5} ${y + 70} L${x - 12} ${y}" stroke="#888" stroke-width="7" stroke-dasharray="4 4"/>`;
  out += `<path d="M${x + 5} ${y + 70} L${x + 12} ${y}" stroke="#888" stroke-width="7" stroke-dasharray="4 4" stroke-dashoffset="4"/>`;
  // curseur
  out += `<path d="M${x - 14} ${y + 60} H${x + 14} L${x + 10} ${y + 92} H${x - 10}Z" fill="url(#metal)" stroke="#6d7075"/>`;
  out += `<rect x="${x - 7}" y="${y + 84}" width="14" height="46" rx="7" fill="url(#metal)" stroke="#6d7075"/>`;
  out += `<rect x="${x - 3}" y="${y + 104}" width="6" height="18" rx="3" fill="#6d7075"/>`;
  out += `</g>`;
  return out;
}
const defBande = `<linearGradient id="bande" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#000" stop-opacity=".25"/><stop offset=".5" stop-color="#fff" stop-opacity=".12"/><stop offset="1" stop-color="#000" stop-opacity=".25"/></linearGradient>`;

// ---------- Produits ----------
const P = {};

P["pagne-wax-cercles"] = frame("#f3e3c8", "#d9bf98",
  pile(["m1", "m2", "m3"]) + etiquette(430, 205, "6 yards"),
  motifs.cercles("m1", ["#1f3a6b", "#e0a526", "#c2402a", "#f6ead2"]) +
  motifs.cercles("m2", ["#c2402a", "#f6ead2", "#1f3a6b", "#e0a526"]) +
  motifs.cercles("m3", ["#e0a526", "#1f3a6b", "#f6ead2", "#c2402a"]));

P["pagne-wax-eventail"] = frame("#e6ecd9", "#b9c6a1",
  pile(["m1", "m2", "m3"]) + etiquette(430, 205, "6 yards"),
  motifs.eventail("m1", ["#23553f", "#f0c24b", "#e8702a", "#fbf2dc"]) +
  motifs.eventail("m2", ["#e8702a", "#23553f", "#fbf2dc", "#7a2e1d"]) +
  motifs.eventail("m3", ["#fbf2dc", "#e8702a", "#23553f", "#f0c24b"]));

P["pagne-wax-premium"] = frame("#f1dccd", "#caa28a",
  pile(["m1", "m2", "m3", "m4"], { h: 66, base: 450 }) + etiquette(430, 190, "Premium"),
  motifs.feuilles("m1", ["#5b1f3c", "#f2b33d", "#2b6f8f", "#f7e9d4"]) +
  motifs.losanges("m2", ["#1d2c52", "#d8452e", "#f2b33d", "#f7e9d4"]) +
  motifs.feuilles("m3", ["#f2b33d", "#5b1f3c", "#1d2c52", "#d8452e"]) +
  motifs.losanges("m4", ["#2b6f8f", "#f7e9d4", "#5b1f3c", "#f2b33d"]));

P["pagne-kente"] = frame("#f4e7c4", "#d4b574",
  pile(["m1", "m2", "m3"]) + etiquette(430, 205, "6 yards"),
  motifs.kente("m1", ["#e3b21f", "#1e6b3a", "#c4322b", "#111"]) +
  motifs.kente("m2", ["#1e6b3a", "#e3b21f", "#111", "#c4322b"]) +
  motifs.kente("m3", ["#c4322b", "#e3b21f", "#1e6b3a", "#111"]));

P["bazin-riche"] = frame("#e7e4f1", "#b1aacb",
  pile(["m1", "m2", "m3"]) +
  `<path d="M140 190 Q300 170 460 200" stroke="#fff" stroke-opacity=".25" stroke-width="18" fill="none" filter="url(#flou2)"/>` +
  etiquette(430, 205, "Riche"),
  motifs.damas("m1", ["#2346a8", "#5f82e0"]) + motifs.damas("m2", ["#b8237a", "#e56cae"]) + motifs.damas("m3", ["#d99a14", "#f5d173"]));

P["kaki-uniforme"] = frame("#ebe5d3", "#c0b48f", rouleau("m1"), motifs.serge("m1", ["#a8905a", "#6f5c33"]) + defPan);

P["coton-popeline"] = frame("#f3ece4", "#d3c4b0", rouleau("m1"), motifs.toile("m1", ["#2f7d6d", "#0f3b32"]) + defPan);

P["doublure-satinee"] = frame("#f3e5e5", "#cfa7a7",
  rouleau("m1") + `<path d="M150 240 H460" stroke="#fff" stroke-opacity=".45" stroke-width="10" filter="url(#flou2)"/><path d="M160 360 C260 350 360 380 470 360" stroke="#fff" stroke-opacity=".3" stroke-width="16" fill="none" filter="url(#flou2)"/>`,
  `<pattern id="m1" width="10" height="10" patternUnits="userSpaceOnUse"><rect width="10" height="10" fill="#8e1f2f"/></pattern>` + defPan);

P["dentelle-brodee"] = (() => {
  const r = rng(7);
  let trous = "";
  const bande = (y0, rot, fill) => {
    let s = `<g transform="rotate(${rot} 300 ${y0})">`;
    s += `<rect x="40" y="${y0 + 10}" width="520" height="120" fill="#000" opacity=".25" filter="url(#flou2)"/>`;
    let bord = `M30 ${y0} H570 V${y0 + 100}`;
    for (let xx = 570; xx > 30; xx -= 30) bord += ` A15 15 0 0 1 ${xx - 30} ${y0 + 100}`;
    bord += "Z";
    s += `<path d="${bord}" fill="${fill}"/>`;
    for (let xx = 45; xx < 560; xx += 30) {
      s += `<circle cx="${xx}" cy="${y0 + 100}" r="6" fill="#6b2a3a"/>`;
      s += `<g transform="translate(${xx + 15} ${y0 + 50})">`;
      for (let k = 0; k < 6; k++) s += `<ellipse cx="0" cy="-9" rx="3.5" ry="7" transform="rotate(${k * 60})" fill="#6b2a3a"/>`;
      s += `<circle r="2.5" fill="${fill}"/></g>`;
      s += `<circle cx="${xx}" cy="${y0 + 18}" r="3" fill="#6b2a3a"/>`;
    }
    s += `<path d="M30 ${y0 + 6} H570" stroke="#fff" stroke-opacity=".6" stroke-width="2"/>`;
    s += `</g>`;
    return s;
  };
  trous += bande(150, -6, "#f7f1e6") + bande(330, 5, "#efe0cb");
  void r;
  return frame("#8a3b4e", "#4d1c29", trous);
})();

P["fil-polyester"] = frame("#f1e9df", "#cdbca6",
  bobine(190, 450, 110, 190, "#c23a2b") + bobine(330, 470, 110, 220, "#1f3f7a") + bobine(455, 440, 96, 170, "#e2a82a") +
  `<path d="M385 262 C420 330 360 380 420 440 S520 470 560 520" stroke="#1f3f7a" stroke-width="2" fill="none"/>`);

P["cone-fil"] = frame("#e4ecef", "#a9bdc4", (() => {
  const c = (x, yb, coul) => {
    let s = ombre(x + 10, yb + 6, 110, 16, 0.3);
    s += `<path d="M${x - 30} ${yb - 250} H${x + 30} L${x + 88} ${yb} H${x - 88}Z" fill="${coul}"/>`;
    for (let k = 0; k < 40; k++) {
      const t = k / 40, yy = yb - 250 + t * 250, hw = 30 + t * 58;
      s += `<path d="M${x - hw} ${yy} Q${x} ${yy + 6} ${x + hw} ${yy}" stroke="#000" stroke-opacity=".10" fill="none"/>`;
    }
    s += `<path d="M${x - 30} ${yb - 250} H${x + 30} L${x + 88} ${yb} H${x - 88}Z" fill="url(#cyl)"/>`;
    s += `<ellipse cx="${x}" cy="${yb}" rx="88" ry="14" fill="#e9e1d2"/><ellipse cx="${x}" cy="${yb}" rx="30" ry="6" fill="#b8ab93"/>`;
    s += `<path d="M${x - 14} ${yb - 250} H${x + 14} L${x + 10} ${yb - 285} H${x - 10}Z" fill="#e9e1d2"/><ellipse cx="${x}" cy="${yb - 285}" rx="10" ry="3" fill="#8f836e"/>`;
    return s;
  };
  return c(210, 480, "#f2efe8") + c(390, 500, "#23232a");
})());

P["boutons-assortis"] = frame("#efe3d3", "#c9ae8c", (() => {
  const r = rng(42);
  const cols = ["#b3342b", "#1f3f7a", "#e0a526", "#2f6b4f", "#f3ece0", "#5a2d1a", "#111418", "#8e5aa8"];
  let s = "";
  const pos = [[180, 200, 58], [330, 170, 44], [450, 250, 52], [250, 330, 66], [410, 390, 48], [150, 420, 40], [320, 460, 36], [500, 430, 30], [120, 290, 28], [540, 170, 26], [260, 110, 24]];
  pos.forEach(([x, y, rr], i) => (s += bouton(x, y, rr, cols[i % cols.length], r() > 0.35 ? 4 : 2, Math.floor(r() * 90))));
  return s;
})(), defBomb);

P["fermeture-eclair"] = frame("#e9ebf1", "#aeb4c6",
  fermeture(200, 120, 360, "#1b2a55", -12) + fermeture(310, 100, 380, "#b7302a", 4) + fermeture(420, 130, 340, "#e0a526", 16),
  defBande);

P["elastique"] = frame("#eef1ea", "#b9c2ae", (() => {
  let s = ombre(290, 450, 170, 30);
  s += `<ellipse cx="290" cy="410" rx="160" ry="60" fill="#d8d4c9"/>`;
  s += `<rect x="130" y="370" width="320" height="40" fill="#e9e5da"/>`;
  s += `<rect x="130" y="370" width="320" height="40" fill="url(#cyl)" opacity=".6"/>`;
  s += `<ellipse cx="290" cy="370" rx="160" ry="60" fill="#f7f5ef"/>`;
  for (let k = 1; k < 14; k++) s += `<ellipse cx="290" cy="370" rx="${160 - k * 8}" ry="${60 - k * 3}" fill="none" stroke="#000" stroke-opacity=".08"/>`;
  s += `<ellipse cx="290" cy="370" rx="44" ry="17" fill="#c4b59a"/><ellipse cx="290" cy="372" rx="30" ry="11" fill="#5b4a33"/>`;
  s += `<path d="M448 380 C520 380 540 300 470 260 C420 232 380 250 360 210" stroke="#f7f5ef" stroke-width="34" fill="none"/>`;
  s += `<path d="M448 380 C520 380 540 300 470 260 C420 232 380 250 360 210" stroke="#000" stroke-opacity=".10" stroke-width="34" stroke-dasharray="2 5" fill="none"/>`;
  return s;
})());

P["entoilage-thermocollant"] = frame("#e8eef3", "#a8b8c6",
  pile(["m1", "m2", "m3"]) + etiquette(430, 205, "Thermo"),
  motifs.points("m1", ["#f8f7f3", "#d7d2c4"]) + motifs.points("m2", ["#2a2a2e", "#46464c"]) + motifs.points("m3", ["#f1efe8", "#d0cabb"]));

P["ciseaux-tailleur"] = frame("#e9e5e0", "#b2a79b", `
${ombre(310, 360, 220, 30)}
<g transform="rotate(-18 300 300)">
  <path d="M300 288 L540 270 Q556 274 540 282 L304 312Z" fill="url(#metal)" stroke="#6d7075" stroke-width="1.5"/>
  <path d="M300 312 L545 322 Q556 318 540 312 L298 290Z" fill="url(#metal)" stroke="#6d7075" stroke-width="1.5" opacity=".95"/>
  <path d="M320 296 L530 280" stroke="#fff" stroke-opacity=".6" stroke-width="2"/>
  <path d="M300 290 C270 280 250 250 222 238" stroke="#141414" stroke-width="22" fill="none" stroke-linecap="round"/>
  <path d="M300 310 C270 320 250 350 222 364" stroke="#141414" stroke-width="22" fill="none" stroke-linecap="round"/>
  <ellipse cx="180" cy="228" rx="52" ry="34" fill="none" stroke="#141414" stroke-width="20"/>
  <ellipse cx="170" cy="380" rx="68" ry="40" fill="none" stroke="#141414" stroke-width="20"/>
  <ellipse cx="176" cy="220" rx="44" ry="26" fill="none" stroke="#fff" stroke-opacity=".12" stroke-width="3"/>
  <ellipse cx="166" cy="372" rx="60" ry="32" fill="none" stroke="#fff" stroke-opacity=".12" stroke-width="3"/>
  <circle cx="302" cy="300" r="12" fill="url(#metal)" stroke="#555"/><path d="M296 300 H308" stroke="#555" stroke-width="2"/>
</g>`);

P["metre-ruban"] = frame("#f3ecd6", "#cdb982", (() => {
  let s = ombre(290, 430, 220, 30);
  // ruban déroulé
  s += `<g transform="rotate(8 400 400)"><rect x="250" y="385" width="320" height="44" fill="#f2d14a"/>`;
  for (let k = 0; k <= 64; k++) {
    const xx = 255 + k * 5;
    const h = k % 10 === 0 ? 18 : k % 5 === 0 ? 12 : 7;
    s += `<path d="M${xx} 385 V${385 + h}" stroke="#1a1a1a" stroke-width="1"/>`;
    if (k % 10 === 0 && k > 0) s += `<text x="${xx}" y="421" font-family="Arial, sans-serif" font-size="11" fill="#b8231c" text-anchor="middle">${140 + k / 10}</text>`;
  }
  s += `<rect x="250" y="385" width="320" height="44" fill="url(#volH)"/></g>`;
  // bobine du mètre
  s += `<circle cx="250" cy="300" r="140" fill="#f2d14a"/>`;
  for (let k = 1; k < 26; k++) s += `<circle cx="250" cy="300" r="${140 - k * 4.4}" fill="none" stroke="#7a5d0e" stroke-opacity="${0.1 + (k % 3) * 0.05}"/>`;
  s += `<circle cx="250" cy="300" r="26" fill="#e7c238"/><circle cx="250" cy="300" r="26" fill="none" stroke="#7a5d0e" stroke-opacity=".3"/>`;
  s += `<circle cx="250" cy="300" r="140" fill="url(#bomb)" opacity=".7"/>`;
  s += `<rect x="238" y="392" width="30" height="46" rx="3" fill="url(#metal)" stroke="#777"/>`;
  return s;
})(), defBomb);

P["pelote-epingles"] = frame("#f0e6e2", "#c9a79c", (() => {
  const r = rng(11);
  let s = ombre(300, 440, 170, 28);
  s += `<ellipse cx="300" cy="420" rx="150" ry="30" fill="#8a5f34"/><rect x="150" y="395" width="300" height="25" fill="#b98753"/><ellipse cx="300" cy="395" rx="150" ry="30" fill="#d3a570"/>`;
  s += `<path d="M160 390 C150 250 450 250 440 390 Z" fill="#c23a2b"/>`;
  for (let k = -3; k <= 3; k++) s += `<path d="M300 268 C${300 + k * 38} 300 ${300 + k * 46} 360 ${300 + k * 44} 392" stroke="#7a1d14" stroke-opacity=".35" stroke-width="2" fill="none"/>`;
  s += `<path d="M160 390 C150 250 450 250 440 390 Z" fill="url(#bomb)"/>`;
  s += `<path d="M300 272 l-24 -14 l18 -2 l-10 -16 l16 10 l0 -18 l8 18 l12 -14 l-2 18 l20 -4 l-16 14Z" fill="#2f6b4f"/>`;
  const tetes = ["#e0a526", "#1f3f7a", "#f3ece0", "#2f6b4f", "#8e5aa8", "#111418", "#e8702a"];
  for (let k = 0; k < 14; k++) {
    const a = Math.PI * (0.12 + 0.76 * r());
    const bx = 300 - Math.cos(a) * 120, by = 390 - Math.sin(a) * 100;
    const L = 40 + r() * 30;
    const ex = bx - Math.cos(a) * L * 0.6 + (r() - 0.5) * 20, ey = by - Math.sin(a) * L;
    s += `<path d="M${bx} ${by} L${ex} ${ey}" stroke="#9aa0a6" stroke-width="2.4"/>`;
    s += `<circle cx="${ex}" cy="${ey}" r="8" fill="${tetes[k % tetes.length]}"/><circle cx="${ex - 2.5}" cy="${ey - 2.5}" r="2.5" fill="#fff" opacity=".6"/>`;
  }
  return s;
})(), defBomb);

P["craie-tailleur"] = frame("#e7e9ee", "#9ea5b5", (() => {
  const tri = (x, y, c, rot) =>
    `<g transform="rotate(${rot} ${x} ${y})"><path d="M${x - 62} ${y + 42} L${x + 70} ${y + 50} L${x} ${y - 66}Z" fill="#1a1208" opacity=".25" filter="url(#flou2)" transform="translate(6 10)"/>
<path d="M${x - 62} ${y + 36} L${x + 62} ${y + 36} L${x} ${y - 70}Z" fill="${c}" stroke="${c}" stroke-width="26" stroke-linejoin="round"/>
<path d="M${x - 62} ${y + 36} L${x + 62} ${y + 36} L${x} ${y - 70}Z" fill="url(#bomb)" stroke-width="0"/>
<path d="M${x - 60} ${y + 48} L${x + 60} ${y + 48}" stroke="#000" stroke-opacity=".18" stroke-width="3"/></g>`;
  let s = tri(200, 270, "#f4f1ea", -12) + tri(390, 250, "#3b67c4", 14) + tri(290, 400, "#e2b93b", 4) + tri(470, 420, "#c9433a", -20);
  const r = rng(3);
  for (let k = 0; k < 40; k++) s += `<circle cx="${120 + r() * 380}" cy="${460 + r() * 70}" r="${1 + r() * 2}" fill="#fff" opacity=".7"/>`;
  return s;
})(), defBomb);

// Vignette d'accueil (Open Graph / partage) et favicon
for (const [nom, svg] of Object.entries(P)) {
  writeFileSync(join(OUT, `${nom}.svg`), svg.replace(/\n\s*/g, "\n"));
}
console.log(`${Object.keys(P).length} visuels générés dans ${OUT}`);
