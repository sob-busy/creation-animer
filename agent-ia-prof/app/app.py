"""Prof IA : agent local (Ollama) pour expliquer les cours, traiter les exercices et préparer les examens.

Lancement : streamlit run app.py
"""

import ollama
import streamlit as st

from outils import chercher_dans_cours, lire_pdf, recherche_web
from prompts import MODES, PROF_IA

MODELES_CONSEILLES = ["qwen3-vl:4b", "qwen3:4b", "qwen2.5:3b", "qwen2.5:1.5b"]

st.set_page_config(page_title="Prof IA", page_icon="🎓")


def modeles_installes() -> list[str]:
    try:
        return [m.model for m in ollama.list().models]
    except Exception:
        return []


# ---------- Barre latérale : réglages ----------
with st.sidebar:
    st.title("🎓 Prof IA")

    modeles = modeles_installes()
    if not modeles:
        st.error(
            "Ollama ne répond pas ou aucun modèle n'est installé.\n\n"
            "1. Ouvre l'application Ollama\n"
            "2. Dans un terminal : `ollama pull qwen2.5:3b`\n"
            "3. Recharge cette page"
        )
        st.stop()
    # On présélectionne le premier modèle conseillé qui est installé
    defaut = next((i for i, m in enumerate(modeles) if m in MODELES_CONSEILLES), 0)
    modele = st.selectbox("Modèle", modeles, index=defaut)

    mode = st.radio("Que veux-tu faire ?", list(MODES))
    web = st.toggle("🔎 Recherche sur Internet", help="Ajoute des résultats DuckDuckGo à la question")

    fichiers = st.file_uploader("📚 Mes cours (PDF)", type="pdf", accept_multiple_files=True)
    image = st.file_uploader(
        "📷 Photo d'un exercice", type=["png", "jpg", "jpeg"], help="Seulement avec un modèle « vl » (vision)"
    )

    if st.button("🗑️ Nouvelle conversation"):
        st.session_state.messages = []
        st.rerun()

# Les PDF sont lus une seule fois puis gardés en mémoire
if "cours" not in st.session_state:
    st.session_state.cours = {}
for f in fichiers or []:
    if f.name not in st.session_state.cours:
        with st.spinner(f"Lecture de {f.name}..."):
            st.session_state.cours[f.name] = lire_pdf(f.getvalue(), f.name)
noms_actifs = {f.name for f in fichiers or []}
morceaux = [m for nom, ms in st.session_state.cours.items() if nom in noms_actifs for m in ms]

# ---------- Conversation ----------
if "messages" not in st.session_state:
    st.session_state.messages = []

st.caption(f"Modèle : `{modele}` · Mode : {mode}" + (f" · {len(noms_actifs)} cours chargé(s)" if noms_actifs else ""))

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["affichage"])

question = st.chat_input("Pose ta question, colle ton exercice...")
if question:
    with st.chat_message("user"):
        st.markdown(question)
        if image:
            st.image(image, width=250)

    # On enrichit la question avec le cours et le web, sans l'afficher à l'élève
    contexte = []
    if morceaux:
        extraits = chercher_dans_cours(question, morceaux)
        if extraits:
            contexte.append(f"EXTRAITS DU COURS DE L'ÉLÈVE :\n{extraits}")
    if web:
        with st.spinner("Recherche sur Internet..."):
            resultats = recherche_web(question)
        if resultats:
            contexte.append(f"RÉSULTATS DE RECHERCHE WEB :\n{resultats}")
        else:
            st.warning("La recherche web n'a rien donné (pas d'Internet ?). Je réponds sans.")
    contenu = "\n\n".join(contexte + [f"QUESTION DE L'ÉLÈVE :\n{question}"]) if contexte else question

    nouveau = {"role": "user", "content": contenu, "affichage": question}
    if image:
        nouveau["images"] = [image.getvalue()]
    st.session_state.messages.append(nouveau)

    consignes = PROF_IA + ("\n\n" + MODES[mode] if MODES[mode] else "")
    historique = [{"role": "system", "content": consignes}] + [
        {k: v for k, v in m.items() if k != "affichage"} for m in st.session_state.messages[-12:]
    ]

    with st.chat_message("assistant"):
        try:
            flux = ollama.chat(model=modele, messages=historique, stream=True, options={"temperature": 0.3})
            reponse = st.write_stream(morceau.message.content or "" for morceau in flux)
        except ollama.ResponseError as erreur:
            reponse = f"⚠️ Erreur d'Ollama : {erreur.error}"
            st.error(reponse)
        except Exception as erreur:
            reponse = f"⚠️ Impossible de joindre Ollama : {erreur}. Vérifie que l'application Ollama est ouverte."
            st.error(reponse)

    st.session_state.messages.append({"role": "assistant", "content": reponse, "affichage": reponse})
