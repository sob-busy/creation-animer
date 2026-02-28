<?php
require 'config.php';
require 'vendor/autoload.php';

use PHPMailer\PHPMailer\PHPMailer;

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
  $email = $_POST['email'];
  $token = bin2hex(random_bytes(16));

  $stmt = $pdo->prepare("UPDATE users SET token_recuperation = ? WHERE email = ?");
  $stmt->execute([$token, $email]);

  $resetLink = "http://votre-site.com/reset_form.php?token=$token";

  $mail = new PHPMailer();
  $mail->isSMTP();
  $mail->Host = 'smtp.gmail.com';
  $mail->SMTPAuth = true;
  $mail->Username = 'votre-email@gmail.com';
  $mail->Password = 'votre-mot-de-passe-app';
  $mail->SMTPSecure = 'tls';
  $mail->Port = 587;

  $mail->setFrom('votre-email@gmail.com', 'Création d\'Animer');
  $mail->addAddress($email);
  $mail->Subject = 'Réinitialisation de mot de passe';
  $mail->Body = "Cliquez ici pour réinitialiser : $resetLink";

  if ($mail->send()) {
    echo "Un lien de réinitialisation a été envoyé.";
  } else {
    echo "Erreur : " . $mail->ErrorInfo;
  }
}
?>