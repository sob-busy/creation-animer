/* Mercerie Incha Allahou — interactions du site (sans dépendance). */
(() => {
  "use strict";

  const B = window.BOUTIQUE;
  const PRODUITS = window.PRODUITS;
  const CATS = window.CATEGORIES;
  const $ = (s, el = document) => el.querySelector(s);
  const $$ = (s, el = document) => [...el.querySelectorAll(s)];
  const parId = Object.fromEntries(PRODUITS.map((p) => [p.id, p]));
  const nomCat = Object.fromEntries(CATS.map((c) => [c.id, c.nom]));

  const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  const lienWa = (texte) => `https://wa.me/${B.whatsapp}${texte ? "?text=" + encodeURIComponent(texte) : ""}`;
  // Ouvre WhatsApp tout de suite (appli sur téléphone, WhatsApp Web sur ordinateur).
  const ouvrirWa = (texte) => {
    const url = lienWa(texte);
    const w = window.open(url, "_blank");
    if (w) w.opener = null; else location.href = url;
  };

  // Tous les liens WhatsApp « génériques » de la page
  $$("[data-wa]").forEach((a) => {
    a.href = lienWa(`Bonjour ${B.nom}, je souhaite avoir des renseignements.`);
    a.target = "_blank";
    a.rel = "noopener";
  });

  // Infos boutique
  $("#adresse").textContent = B.adresse;
  $("#horaires").innerHTML = B.horaires.map(([j, h]) => `<span><strong>${esc(j)}</strong> · ${esc(h)}</span>`).join("");
  $("#paiement").textContent = B.paiement;
  $("#livraison").textContent = B.livraison;
  $("#annee").textContent = new Date().getFullYear();

  // ---------- Stockage (protégé : peut être indisponible) ----------
  const stock = {
    lire(k, d) { try { const v = localStorage.getItem(k); return v ? JSON.parse(v) : d; } catch { return d; } },
    ecrire(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch { /* ignoré */ } },
  };

  // ---------- Catalogue ----------
  const etat = { cat: "tous", q: "" };
  const puces = $("#puces");
  const grille = $("#grille");

  function rendrePuces() {
    const liste = [{ id: "tous", nom: "Tout voir", n: PRODUITS.length }, ...CATS.map((c) => ({ ...c, n: PRODUITS.filter((p) => p.categorie === c.id).length }))];
    puces.innerHTML = liste.map((c) =>
      `<button class="puce" type="button" data-cat="${c.id}" aria-pressed="${c.id === etat.cat}">${esc(c.nom)} <span class="puce__n">${c.n}</span></button>`
    ).join("");
  }
  puces.addEventListener("click", (e) => {
    const b = e.target.closest(".puce");
    if (!b) return;
    etat.cat = b.dataset.cat;
    $$(".puce", puces).forEach((p) => p.setAttribute("aria-pressed", p === b));
    rendreGrille();
  });

  const normal = (s) => s.toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "");
  $("#recherche").addEventListener("input", (e) => { etat.q = normal(e.target.value.trim()); rendreGrille(); });

  function rendreGrille() {
    const liste = PRODUITS.filter((p) =>
      (etat.cat === "tous" || p.categorie === etat.cat) &&
      (!etat.q || normal(`${p.nom} ${p.description} ${nomCat[p.categorie]}`).includes(etat.q))
    );
    grille.innerHTML = liste.map((p, i) => `
      <article class="carte" style="--i:${i}">
        <div class="carte__visuel">
          <img src="${esc(p.image)}" alt="${esc(p.nom)}" width="600" height="600" loading="lazy" decoding="async">
          ${p.badge ? `<span class="carte__badge">${esc(p.badge)}</span>` : ""}
          <span class="carte__voir" aria-hidden="true">Voir le détail</span>
        </div>
        <div class="carte__corps">
          <span class="carte__cat">${esc(nomCat[p.categorie])}</span>
          <h3 class="carte__nom"><a class="carte__lien" href="#produit-${p.id}" data-produit="${p.id}">${esc(p.nom)}</a></h3>
          <div class="carte__bas">
            <p class="prix">Prix à discuter<small>${esc(p.unite)}</small></p>
            <button class="btn-ajout" type="button" data-ajout="${p.id}" aria-label="Ajouter ${esc(p.nom)} à ma sélection">
              <svg class="ic"><use href="#i-plus"/></svg>
            </button>
          </div>
        </div>
      </article>`).join("");
    $("#vide").hidden = liste.length > 0;
    $("#resultat").textContent = liste.length
      ? `${liste.length} article${liste.length > 1 ? "s" : ""}${etat.cat !== "tous" ? " · " + nomCat[etat.cat] : ""}`
      : "";
  }

  grille.addEventListener("click", (e) => {
    const ajout = e.target.closest("[data-ajout]");
    if (ajout) {
      ajouter(ajout.dataset.ajout, 1);
      ajout.classList.add("ok");
      ajout.innerHTML = '<svg class="ic" viewBox="0 0 24 24"><path d="M5 12.5l4.5 4.5L19 7.5" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>';
      setTimeout(() => { ajout.classList.remove("ok"); ajout.innerHTML = '<svg class="ic"><use href="#i-plus"/></svg>'; }, 1200);
      return;
    }
    const lien = e.target.closest("[data-produit]");
    if (lien) { e.preventDefault(); ouvrirFiche(lien.dataset.produit); }
  });
  $$(".echantillon").forEach((b) => b.addEventListener("click", () => ouvrirFiche(b.dataset.produit)));

  // ---------- Fiche produit ----------
  const fiche = $("#fiche");
  let courant = null, qte = 1;

  function majQte() {
    $("#qte").textContent = qte;
    $("#qte-moins").disabled = qte <= 1;
    const p = courant;
    $("#fiche-wa").href = lienWa(
      `Bonjour ${B.nom},\nJe suis intéressé(e) par :\n• ${qte} × ${p.nom} — ${p.unite}\nQuel est votre prix ? Est-ce disponible ? Merci !`
    );
  }
  function ouvrirFiche(id) {
    const p = parId[id];
    if (!p) return;
    courant = p; qte = 1;
    $("#fiche-img").src = p.image;
    $("#fiche-img").alt = p.nom;
    $("#fiche-cat").textContent = nomCat[p.categorie];
    $("#fiche-nom").textContent = p.nom;
    $("#fiche-unite").textContent = p.unite;
    $("#fiche-desc").textContent = p.description;
    $("#fiche-details").innerHTML = (p.details || []).map((d) => `<li>${esc(d)}</li>`).join("");
    majQte();
    if (typeof fiche.showModal === "function") fiche.showModal(); else fiche.setAttribute("open", "");
  }
  const fermerFiche = () => (fiche.close ? fiche.close() : fiche.removeAttribute("open"));
  $("#qte-plus").addEventListener("click", () => { qte = Math.min(99, qte + 1); majQte(); });
  $("#qte-moins").addEventListener("click", () => { qte = Math.max(1, qte - 1); majQte(); });
  $("#fiche-ajouter").addEventListener("click", () => { fermerFiche(); ajouter(courant.id, qte); });
  fiche.addEventListener("click", (e) => {
    if (e.target === fiche || e.target.closest("[data-fermer]")) fermerFiche();
  });

  // ---------- Sélection (panier) ----------
  let panier = stock.lire("mi-selection", {});
  panier = Object.fromEntries(Object.entries(panier).filter(([id, n]) => parId[id] && n > 0));
  const tiroir = $("#tiroir"), voile = $("#voile");

  function ajouter(id, n) {
    panier[id] = Math.min(99, (panier[id] || 0) + n);
    sauver();
    const c = $("#compteur");
    c.classList.remove("tape"); void c.offsetWidth; c.classList.add("tape");
    toast(`${parId[id].nom} ajouté${n > 1 ? ` (×${n})` : ""}`);
  }
  function sauver() { stock.ecrire("mi-selection", panier); rendrePanier(); }
  const nbArticles = () => Object.values(panier).reduce((a, b) => a + b, 0);

  function rendrePanier() {
    const lignes = Object.entries(panier);
    $("#compteur").textContent = nbArticles();
    tiroir.classList.toggle("est-vide", lignes.length === 0);
    $("#lignes").innerHTML = lignes.map(([id, n]) => {
      const p = parId[id];
      return `<li class="ligne">
        <img src="${esc(p.image)}" alt="" width="64" height="64">
        <div><p class="ligne__nom">${esc(p.nom)}</p><p class="ligne__prix">${esc(p.unite)}</p></div>
        <div class="ligne__droite">
          <div class="stepper stepper--petit" role="group" aria-label="Quantité ${esc(p.nom)}">
            <button class="stepper__b" type="button" data-moins="${id}" aria-label="Diminuer"><svg class="ic"><use href="#i-moins"/></svg></button>
            <output class="stepper__v">${n}</output>
            <button class="stepper__b" type="button" data-plus="${id}" aria-label="Augmenter"><svg class="ic"><use href="#i-plus"/></svg></button>
          </div>
        </div>
      </li>`;
    }).join("");
  }
  $("#lignes").addEventListener("click", (e) => {
    const plus = e.target.closest("[data-plus]"), moins = e.target.closest("[data-moins]");
    if (plus) panier[plus.dataset.plus] = Math.min(99, panier[plus.dataset.plus] + 1);
    else if (moins) { const id = moins.dataset.moins; panier[id] -= 1; if (panier[id] <= 0) delete panier[id]; }
    else return;
    sauver();
  });
  $("#vider").addEventListener("click", () => { panier = {}; sauver(); });

  function ouvrirTiroir() {
    $("#toast").classList.remove("visible");
    voile.hidden = false;
    tiroir.classList.add("ouvert");
    tiroir.setAttribute("aria-hidden", "false");
    document.body.style.overflow = "hidden";
    setTimeout(() => $("#fermer-selection").focus(), 50);
  }
  function fermerTiroir() {
    voile.hidden = true;
    tiroir.classList.remove("ouvert");
    tiroir.setAttribute("aria-hidden", "true");
    document.body.style.overflow = "";
  }
  $("#ouvrir-selection").addEventListener("click", ouvrirTiroir);
  $("#fermer-selection").addEventListener("click", fermerTiroir);
  voile.addEventListener("click", fermerTiroir);
  $$("[data-fermer-tiroir]").forEach((a) => a.addEventListener("click", fermerTiroir));
  document.addEventListener("keydown", (e) => { if (e.key === "Escape" && tiroir.classList.contains("ouvert")) fermerTiroir(); });

  $("#form-commande").addEventListener("submit", (e) => {
    e.preventDefault();
    const f = new FormData(e.target);
    const lignes = Object.entries(panier).map(([id, n]) => {
      const p = parId[id];
      return `• ${n} × ${p.nom} — ${p.unite}`;
    });
    const nom = (f.get("nom") || "").trim(), quartier = (f.get("quartier") || "").trim();
    const msg = [
      `Bonjour ${B.nom},`,
      "Je souhaite commander les articles suivants :",
      ...lignes,
      "",
      nom ? `Nom : ${nom}` : null,
      quartier ? `Quartier : ${quartier}` : null,
      "",
      "Pouvez-vous me donner vos prix et me confirmer la disponibilité ? Merci !",
    ].filter((l) => l !== null).join("\n");
    ouvrirWa(msg);
  });

  // ---------- Toast ----------
  let minuteur;
  function toast(txt) {
    const t = $("#toast");
    t.innerHTML = `<span>${esc(txt)}</span><button type="button">Voir</button>`;
    $("button", t).onclick = () => { t.classList.remove("visible"); ouvrirTiroir(); };
    t.classList.add("visible");
    clearTimeout(minuteur);
    minuteur = setTimeout(() => t.classList.remove("visible"), 2800);
  }

  // ---------- Messagerie ----------
  const chat = $("#chat"), lanceur = $("#lanceur"), fil = $("#chat-fil"), rapides = $("#chat-rapides");
  const REPONSES = {
    "Les prix": () => `Nos prix se discutent directement avec l'équipe sur WhatsApp : ils dépendent de la qualité, du motif et de la quantité. Ajoutez vos articles à « Ma sélection » et envoyez-la, on vous répond avec les prix.`,
    "Livraison": () => B.livraison,
    "Horaires & adresse": () => `${B.adresse}. ${B.horaires.map(([j, h]) => `${j} : ${h}`).join(" · ")}.`,
    "Paiement": () => B.paiement,
    "Commander": () => `Ajoutez vos articles à « Ma sélection », puis cliquez sur « Envoyer ma commande sur WhatsApp ». Vous pouvez aussi nous écrire directement ici : votre message part sur notre WhatsApp.`,
    "Parler à quelqu'un": () => `Avec plaisir ! Un membre de l'équipe vous répond sur WhatsApp au <a href="${lienWa(`Bonjour ${B.nom}, j'aimerais parler à quelqu'un.`)}" target="_blank" rel="noopener">${B.whatsappAffiche}</a>.`,
  };
  let demarre = false;

  function bulle(html, qui = "bot") {
    const m = document.createElement("div");
    m.className = `msg msg--${qui}`;
    m.innerHTML = html;
    fil.appendChild(m);
    fil.scrollTop = fil.scrollHeight;
  }
  function repondre(html) {
    const f = document.createElement("div");
    f.className = "msg msg--bot msg--frappe";
    f.innerHTML = "<i></i><i></i><i></i>";
    fil.appendChild(f);
    fil.scrollTop = fil.scrollHeight;
    setTimeout(() => { f.remove(); bulle(html); }, 650);
  }
  function rendreRapides() {
    rapides.innerHTML = Object.keys(REPONSES).map((k) => `<button class="rapide" type="button">${esc(k)}</button>`).join("");
  }
  rapides.addEventListener("click", (e) => {
    const b = e.target.closest(".rapide");
    if (!b) return;
    bulle(esc(b.textContent), "moi");
    repondre(REPONSES[b.textContent]());
  });
  fil.addEventListener("click", (e) => { if (e.target.closest("[data-fermer-chat]")) basculerChat(false); });

  function basculerChat(ouvrir) {
    const o = ouvrir ?? chat.hidden;
    chat.hidden = !o;
    lanceur.setAttribute("aria-expanded", o);
    lanceur.classList.add("vu");
    stock.ecrire("mi-chat-vu", true);
    if (o && !demarre) {
      demarre = true;
      bulle(`Bonjour et bienvenue chez <strong>${esc(B.nom)}</strong> 👋`);
      repondre("Je peux vous renseigner sur nos tissus, les prix, la livraison à Lomé… Pour commander ou poser une question précise, on continue sur WhatsApp avec l'équipe.");
      rendreRapides();
    }
    if (o) setTimeout(() => $("#chat-texte").focus({ preventScroll: true }), 80);
  }
  lanceur.addEventListener("click", () => basculerChat());
  $("#fermer-chat").addEventListener("click", () => basculerChat(false));
  $("#chat-form").addEventListener("submit", (e) => {
    e.preventDefault();
    const champ = $("#chat-texte");
    const txt = champ.value.trim();
    if (!txt) return;
    bulle(esc(txt), "moi");
    champ.value = "";
    ouvrirWa(`Bonjour ${B.nom}, ${txt}`);
    repondre(`Votre message part sur notre WhatsApp (${esc(B.whatsappAffiche)}). Si rien ne s'ouvre, touchez « Continuer sur WhatsApp » ci-dessous.`);
  });
  if (stock.lire("mi-chat-vu", false)) lanceur.classList.add("vu");
  setTimeout(() => $("#lanceur-bulle").classList.add("cache"), 12000);

  // ---------- Entête & apparitions ----------
  const entete = $("#entete");
  const surDefil = () => entete.classList.toggle("est-defile", window.scrollY > 10);
  window.addEventListener("scroll", surDefil, { passive: true });
  surDefil();

  if ("IntersectionObserver" in window) {
    const obs = new IntersectionObserver((ents) => ents.forEach((en) => {
      if (en.isIntersecting) { en.target.classList.add("vu"); obs.unobserve(en.target); }
    }), { threshold: 0.12 });
    $$(".section__tete, .etape, .maison__visuel, .maison__texte, .carte-info, .carte-wa").forEach((el) => { el.classList.add("revele"); obs.observe(el); });
  }

  // Lien direct vers un produit : #produit-<id>
  const depuisHash = () => { const m = location.hash.match(/^#produit-(.+)$/); if (m && parId[m[1]]) ouvrirFiche(m[1]); };

  rendrePuces();
  rendreGrille();
  rendrePanier();
  depuisHash();
})();
