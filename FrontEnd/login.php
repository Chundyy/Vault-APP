<?php
require 'db.php';
session_start();

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $username = trim($_POST["username"]);
    $password = $_POST["password"];

    $stmt = $conn->prepare("SELECT id, password_hash FROM users WHERE username = ?");
    $stmt->bind_param("s", $username);
    $stmt->execute();
    $stmt->store_result();

    if ($stmt->num_rows == 1) {
        $stmt->bind_result($id, $passwordHash);
        $stmt->fetch();

        if (password_verify($password, $passwordHash)) {
            $_SESSION["user_id"] = $id;
            $_SESSION["username"] = $username;
            header("Location: index.php");
            exit();
        } else {
            echo "Senha incorreta.";
        }
    } else {
        echo "Usuário não encontrado.";
    }
}
?>

<!-- HTML -->
<h2>Login</h2>
<form method="post">
    Usuário: <input type="text" name="username" required><br><br>
    Senha: <input type="password" name="password" required><br><br>
    <input type="submit" value="Entrar">
</form>
<a href="register.php">Não tem conta? Registre-se</a>
