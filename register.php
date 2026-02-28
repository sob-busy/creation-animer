<?php
require 'config.php';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
  $nom = $_POST['nom'];
  $prenom = $_POST['prenom'];
  $genre = $_POST['genre'];
  $date_naissance = $_POST['date_naissance'];
  $lieu = $_POST['lieu'];
  $email = $_POST['email'];
  $password = password_hash($_POST['password'], PASSWORD_DEFAULT);

  $stmt = $pdo->prepare("INSERT INTO users (nom, prenom, genre, date_naissance, lieu, email, mot_de_passe) VALUES (?, ?, ?, ?, ?, ?, ?)");
  $stmt->execute([$nom, $prenom, $genre, $date_naissance, $lieu, $email, $password]);
  echo "Inscription réussie";
}
?>