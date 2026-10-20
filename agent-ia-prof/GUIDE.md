# Créer « Prof IA » : un agent IA gratuit et local (Windows 8 Go + Android)

Tout ce qui suit est **gratuit** et fonctionne **sans abonnement**. Une fois les
modèles téléchargés, l'agent marche **même sans Internet** (sauf la recherche web).

## Étape 1 : installer Ollama (le moteur qui fait tourner l'IA)
1. Va sur https://ollama.com/download et télécharge la version Windows.
2. Installe-la normalement, puis ouvre l'**Invite de commandes** (touche Windows, tape `cmd`).
3. Télécharge le modèle de base (~2 Go) :
   ```
   ollama pull qwen2.5:3b
   ```

> Avec 8 Go de RAM, reste sur des modèles de 1,5 à 4 milliards de paramètres.
> Ferme ton navigateur et les autres programmes lourds pendant l'utilisation.
> Autres modèles à essayer : `phi4-mini` (bon en maths, un peu plus lourd),
> `qwen2.5:1.5b` (plus rapide si ton PC rame), `deepseek-r1:1.5b` (raisonne étape par étape).
> La liste complète : https://ollama.com/library

## Étape 2 : créer ton agent « Prof IA »
1. Copie le fichier `Modelfile` de ce dossier dans un dossier, par exemple `C:\prof-ia\`.
2. Dans l'invite de commandes :
   ```
   cd C:\prof-ia
   ollama create prof-ia -f Modelfile
   ollama run prof-ia
   ```
3. Pose ta question. Tape `/bye` pour quitter.

Tu peux modifier le texte après `SYSTEM` dans le `Modelfile` (par exemple ajouter
ton niveau : « L'élève est en licence 2 de maths ») puis relancer `ollama create`.

## Étape 3 : une vraie interface + recherche web + tes PDF de cours
On utilise **Page Assist**, une extension gratuite et légère (mieux qu'Open WebUI sur 8 Go).
1. Dans Chrome, Edge ou Brave, installe l'extension **Page Assist** depuis le Chrome Web Store.
2. Clique sur son icône : elle détecte Ollama tout seul.
3. En haut, choisis le modèle **prof-ia**.
4. **Recherche web** : active l'interrupteur « Search Internet » sous la zone de texte
   (DuckDuckGo par défaut, gratuit, sans clé).
5. **Tes cours** : menu Paramètres → *Manage Knowledge* → ajoute tes PDF / fichiers texte.
   Ensuite, dans le chat, sélectionne cette base de connaissances : l'agent répond à partir de ton cours.
   (Il faut aussi installer le modèle d'embedding demandé, par ex. `ollama pull nomic-embed-text`.)

## Étape 4 : sur ton téléphone Android
**Option A — l'IA directement dans le téléphone (hors ligne)**
1. Installe **PocketPal AI** (gratuit, Play Store).
2. Télécharge dans l'appli un petit modèle (Qwen 2.5 1.5B ou Gemma de taille 1-2B).
3. Dans les réglages du modèle, colle le texte du `SYSTEM` du Modelfile comme « system prompt ».
   Les petits modèles sur téléphone sont moins forts : bien pour les explications, à vérifier pour les calculs.

**Option B — le téléphone utilise l'agent de ton PC (plus puissant)**
1. Sur le PC : Paramètres Windows → Variables d'environnement → nouvelle variable
   `OLLAMA_HOST` = `0.0.0.0`, puis redémarre Ollama. Autorise Ollama dans le pare-feu (réseau privé).
2. Trouve l'adresse IP du PC : `ipconfig` → « Adresse IPv4 » (ex. `192.168.1.20`).
3. Sur le téléphone (même Wi-Fi), installe une appli cliente Ollama gratuite
   (ex. **Ollama App** / « Reins » sur F-Droid ou Play Store) et mets l'adresse `http://192.168.1.20:11434`.
4. Choisis le modèle **prof-ia**. Le PC doit rester allumé.

## Exemples de demandes
- « Explique-moi les intégrales par parties comme si c'était la première fois. »
- « Voici mon exercice : ... Donne-moi seulement un indice. »
- « Prépare-moi un plan de révision sur 7 jours pour mon examen d'algèbre linéaire. »
- « Fais-moi un QCM de 10 questions sur les graphes, puis corrige mes réponses. »
- « Explique ce code Python et sa complexité : ... »

## À savoir (honnêtement)
- Un petit modèle local sur 8 Go est **moins fort que ChatGPT ou Claude** et peut se tromper
  en calcul. Demande-lui toujours de vérifier son résultat, et vérifie toi-même les points importants.
- Pour vérifier un calcul gratuitement : demande à l'agent d'écrire le code Python correspondant
  (avec `sympy`), ou utilise GeoGebra / WolframAlpha.
- Si c'est lent : passe à `qwen2.5:1.5b`, et baisse `num_ctx` à 2048 dans le Modelfile.
- Pour savoir si tu as une carte NVIDIA : Gestionnaire des tâches → onglet Performances → « GPU ».
  Si tu en as une, Ollama l'utilise automatiquement et c'est bien plus rapide.
