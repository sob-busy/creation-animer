CREATE DATABASE IF NOT EXISTS creation_animer;
USE creation_animer;

CREATE TABLE IF NOT EXISTS users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nom VARCHAR(100),
  prenom VARCHAR(100),
  genre VARCHAR(10),
  date_naissance DATE,
  lieu VARCHAR(100),
  email VARCHAR(150) UNIQUE,
  mot_de_passe VARCHAR(255),
  token_recuperation VARCHAR(64)
);