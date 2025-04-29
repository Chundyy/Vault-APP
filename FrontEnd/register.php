<?php
require 'db.php';

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $username = trim($_POST["username"]);
    $password = $_POST["password"];
    $passwordHash = password_hash($password, PASSWORD_DEFAULT);

    $stmt = $conn->prepare("INSERT INTO users (username, password_hash) VALUES (?, ?)");
    $stmt->bind_param("ss", $username, $passwordHash);

    if ($stmt->execute()) {
        header("Location: login.php");
        exit();
    } else {
        echo "Erro ao registrar: " . $stmt->error;
    }
}
?>

<!-- HTML -->
<h2>Registro</h2>
<form method="post">
    Usuário: <input type="text" name="username" required><br><br>
    Senha: <input type="password" name="password" required><br><br>
    <input type="submit" value="Registrar">
</form>
<a class="link" href="login.php">Já tem conta? Faça login</a>
