const generatorForm = document.getElementById('generator-form');
const preview = document.getElementById('preview');
const metadata = document.getElementById('metadata');
const chatForm = document.getElementById('chat-form');
const chatInput = document.getElementById('chat-input');
const chatWindow = document.getElementById('chat-window');
const generateBtn = document.getElementById('generate-btn');
const chatSendBtn = document.getElementById('chat-send-btn');
const authActions = document.getElementById('auth-actions');
const authStatus = document.getElementById('auth-status');

const SESSION_KEY = 'creation_animer_session';
let hasGeneration = false;

const getSession = () => {
  const sessionRaw = localStorage.getItem(SESSION_KEY);
  return sessionRaw ? JSON.parse(sessionRaw) : null;
};

const removeSession = () => localStorage.removeItem(SESSION_KEY);

const addMessage = (role, text) => {
  const bubble = document.createElement('div');
  bubble.className = `message ${role}`;
  bubble.textContent = text;
  chatWindow.appendChild(bubble);
  chatWindow.scrollTop = chatWindow.scrollHeight;
};

const lockChatUntilGeneration = () => {
  chatInput.disabled = true;
  chatSendBtn.disabled = true;
  chatInput.placeholder = 'Générez d\'abord un visuel pour activer le chatbot...';
};

const unlockChat = () => {
  chatInput.disabled = false;
  chatSendBtn.disabled = false;
  chatInput.placeholder = 'Décrivez la modification à appliquer...';
};

const renderAuthActions = () => {
  const session = getSession();
  if (!session) {
    authStatus.textContent = 'Connectez-vous pour sauvegarder vos briefs et vos rendus.';
    return;
  }

  authActions.innerHTML = `
    <span class="hello-user">Bonjour ${session.prenom || session.email}</span>
    <button id="logout-btn" class="btn secondary" type="button">Déconnexion</button>
  `;
  authStatus.textContent = 'Session active : vos actions sont maintenant disponibles.';

  const logoutBtn = document.getElementById('logout-btn');
  logoutBtn.addEventListener('click', () => {
    removeSession();
    window.location.reload();
  });
};

lockChatUntilGeneration();
renderAuthActions();

if (generatorForm) {
  generatorForm.addEventListener('submit', (event) => {
    event.preventDefault();
    const prompt = document.getElementById('prompt').value.trim();
    const type = document.getElementById('content-type').value;
    const style = document.getElementById('style').value;

    if (!prompt) return;

    generateBtn.disabled = true;
    generateBtn.textContent = 'Génération en cours...';

    window.setTimeout(() => {
      const date = new Date().toLocaleString('fr-FR');
      preview.classList.remove('empty');
      preview.innerHTML = `<div><strong>Rendu ${type === 'video' ? 'vidéo' : 'image'} prêt</strong><br><small>${prompt}</small></div>`;

      metadata.innerHTML = `
        <li>Type: ${type}</li>
        <li>Style: ${style}</li>
        <li>Résolution: ${type === 'video' ? '4K UHD / 24fps' : '6144 x 6144'}</li>
        <li>Généré le: ${date}</li>
      `;

      hasGeneration = true;
      unlockChat();
      addMessage('bot', `Votre ${type} a été généré. Donnez-moi une instruction pour l'améliorer.`);

      generateBtn.disabled = false;
      generateBtn.textContent = 'Lancer la génération';
    }, 450);
  });
}

if (chatForm) {
  chatForm.addEventListener('submit', (event) => {
    event.preventDefault();
    const request = chatInput.value.trim();
    if (!request) return;

    if (!hasGeneration) {
      addMessage('bot', 'Veuillez lancer une génération avant de demander une modification.');
      return;
    }

    addMessage('user', request);

    const suggestions = [
      "Modification appliquée: contraste augmenté et lumière retravaillée.",
      "C'est fait: j'ai renforcé le rendu premium et la lisibilité des éléments clés.",
      "Version alternative prête: palette plus chaude + cadrage optimisé pour les réseaux sociaux.",
      "Ajustement terminé: timing plus dynamique et transition d'ouverture améliorée."
    ];

    const answer = suggestions[Math.floor(Math.random() * suggestions.length)];
    setTimeout(() => addMessage('bot', answer), 350);

    chatInput.value = '';
  });
}

addMessage('bot', 'Bienvenue 👋 Décrivez votre contenu, générez-le, puis demandez vos modifications ici.');
