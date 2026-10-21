# Prof IA : l'application

Interface de chat locale (Streamlit + Ollama) avec :
- 6 modes : discussion, expliquer le cours, résoudre un exercice, indice seulement, préparer l'examen, quiz ;
- tes cours en PDF : l'agent répond à partir des passages pertinents ;
- la recherche web gratuite (DuckDuckGo) ;
- la photo d'un exercice (avec un modèle « vl », par ex. `qwen3-vl:4b`) ;
- l'accès depuis le téléphone, sur le même Wi-Fi.

## Installation avec VS Code (Windows)

### 1. Les logiciels (une seule fois)
1. **Python** : https://www.python.org/downloads/ → à l'installation, **coche « Add python.exe to PATH »**.
2. **VS Code** : https://code.visualstudio.com/
3. Dans VS Code : onglet Extensions (Ctrl+Maj+X) → installe **Python** (de Microsoft).
4. **Ollama** à jour (https://ollama.com/download) et au moins un modèle :
   `ollama pull qwen2.5:3b`

### 2. Récupérer le code
Télécharge le ZIP et décompresse-le, par exemple dans `C:\prof-ia` :
https://github.com/sob-busy/creation-animer/archive/refs/heads/ccr-9d22fdf3-smahgn.zip

Dans VS Code : **Fichier → Ouvrir le dossier** → choisis le dossier `agent-ia-prof\app`.

### 3. Installer et lancer
Ouvre le terminal de VS Code (**Terminal → Nouveau terminal**) et tape :
```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```
Le navigateur s'ouvre sur http://localhost:8501 : ton agent est prêt.

Les fois suivantes : `.venv\Scripts\activate` puis `streamlit run app.py`,
ou double-clique simplement sur **`lancer.bat`**.

> Si PowerShell refuse `activate` (« l'exécution de scripts est désactivée ») :
> `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`, puis réessaie.

### 4. Sur le téléphone Android
Lance avec `lancer.bat` (ou `streamlit run app.py --server.address 0.0.0.0`).
Le terminal affiche une **Network URL** du type `http://192.168.1.20:8501` :
ouvre-la dans Chrome sur ton téléphone, connecté au même Wi-Fi.
Si Windows demande l'autorisation du pare-feu, accepte pour les réseaux privés.

## Les fichiers
| Fichier | Rôle |
|---|---|
| `app.py` | L'interface et la conversation avec le modèle |
| `prompts.py` | La personnalité de Prof IA et les modes ; modifie-le pour l'adapter à ton niveau |
| `outils.py` | Recherche web et lecture des PDF |
| `lancer.bat` | Installe (la première fois) puis lance l'appli d'un double-clic |
