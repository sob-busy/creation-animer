"""Outils de l'agent : recherche web gratuite (DuckDuckGo) et lecture des cours en PDF."""

import io
import re

from pypdf import PdfReader


def recherche_web(question: str, nb_resultats: int = 5) -> str:
    """Cherche sur le web et renvoie les résultats sous forme de texte, ou '' en cas d'échec."""
    try:
        from ddgs import DDGS

        resultats = DDGS().text(question, region="fr-fr", max_results=nb_resultats)
    except Exception as erreur:  # pas d'Internet, site indisponible...
        print(f"[recherche web] échec : {erreur}")
        return ""
    return "\n\n".join(
        f"[{i}] {r.get('title', '')}\nLien : {r.get('href', '')}\n{r.get('body', '')}"
        for i, r in enumerate(resultats, start=1)
    )


def lire_pdf(contenu: bytes, nom: str, taille_morceau: int = 1200) -> list[dict]:
    """Découpe un PDF en morceaux de texte, en gardant le numéro de page de chaque morceau."""
    morceaux = []
    lecteur = PdfReader(io.BytesIO(contenu))
    for num_page, page in enumerate(lecteur.pages, start=1):
        texte = re.sub(r"\s+", " ", page.extract_text() or "").strip()
        for debut in range(0, len(texte), taille_morceau):
            morceaux.append({"source": f"{nom}, page {num_page}", "texte": texte[debut : debut + taille_morceau]})
    return morceaux


def _mots(texte: str) -> set[str]:
    # On ignore les petits mots (le, de, et...) qui ne disent rien du sujet
    return {m for m in re.findall(r"\w+", texte.lower()) if len(m) > 3}


def chercher_dans_cours(question: str, morceaux: list[dict], nb: int = 4) -> str:
    """Renvoie les passages du cours qui partagent le plus de mots avec la question."""
    mots_question = _mots(question)
    if not mots_question or not morceaux:
        return ""
    scores = [(len(mots_question & _mots(m["texte"])), m) for m in morceaux]
    meilleurs = [m for score, m in sorted(scores, key=lambda s: s[0], reverse=True)[:nb] if score > 0]
    return "\n\n".join(f"[{m['source']}]\n{m['texte']}" for m in meilleurs)
