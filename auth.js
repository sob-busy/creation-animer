const USERS_KEY = 'creation_animer_users';
const SESSION_KEY = 'creation_animer_session';

const getUsers = () => JSON.parse(localStorage.getItem(USERS_KEY) || '[]');
const saveUsers = (users) => localStorage.setItem(USERS_KEY, JSON.stringify(users));
const setSession = (session) => localStorage.setItem(SESSION_KEY, JSON.stringify(session));

const messageEl = document.getElementById('auth-message');

const setMessage = (message, isError = false) => {
  if (!messageEl) return;
  messageEl.textContent = message;
  messageEl.classList.toggle('error', isError);
  messageEl.classList.toggle('success', !isError);
};

const registerForm = document.getElementById('register-form');
if (registerForm) {
  registerForm.addEventListener('submit', (event) => {
    event.preventDefault();
    const data = new FormData(registerForm);

    const user = {
      nom: data.get('nom').trim(),
      prenom: data.get('prenom').trim(),
      genre: data.get('genre'),
      date_naissance: data.get('date_naissance'),
      lieu: data.get('lieu').trim(),
      email: data.get('email').trim().toLowerCase(),
      mot_de_passe: data.get('password')
    };

    const users = getUsers();
    const alreadyExists = users.some((savedUser) => savedUser.email === user.email);

    if (alreadyExists) {
      setMessage('Cet email existe déjà. Connectez-vous directement.', true);
      return;
    }

    users.push(user);
    saveUsers(users);
    setSession({ email: user.email, prenom: user.prenom });
    setMessage('Compte créé avec succès. Redirection vers le studio...');

    setTimeout(() => {
      window.location.href = 'index.html';
    }, 700);
  });
}

const loginForm = document.getElementById('login-form');
if (loginForm) {
  loginForm.addEventListener('submit', (event) => {
    event.preventDefault();
    const data = new FormData(loginForm);
    const email = data.get('email').trim().toLowerCase();
    const password = data.get('password');

    const users = getUsers();
    const foundUser = users.find((savedUser) => savedUser.email === email);

    if (!foundUser || foundUser.mot_de_passe !== password) {
      setMessage('Email ou mot de passe incorrect.', true);
      return;
    }

    setSession({ email: foundUser.email, prenom: foundUser.prenom });
    setMessage('Connexion réussie. Redirection vers le studio...');

    setTimeout(() => {
      window.location.href = 'index.html';
    }, 500);
  });
}
