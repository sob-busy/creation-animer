<?php
require 'config.php';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
  $email = $_POST['email'];
  $password = $_POST['password'];

  $stmt = $pdo->prepare("SELECT * FROM users WHERE email = ?");
  $stmt->execute([$email]);
  $user = $stmt->fetch();

  if ($user && password_verify($password, $user['mot_de_passe'])) {
    echo "Connexion réussie";
  } else {
    echo "Email ou mot de passe incorrect";
  }
}
?>