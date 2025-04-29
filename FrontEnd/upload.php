<?php
$host = "localhost";
$user = "root";
$pass = "";
$db = "file_upload_db";

$conn = new mysqli($host, $user, $pass, $db);
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

if (isset($_FILES['uploaded_file'])) {
    $fileName = $_FILES['uploaded_file']['name'];
    $fileType = $_FILES['uploaded_file']['type'];
    $fileSize = $_FILES['uploaded_file']['size'];
    $fileData = file_get_contents($_FILES['uploaded_file']['tmp_name']);

    // 🔐 Gerar hash SHA-256 do nome do arquivo
    $fileNameHashed = hash('sha256', $fileName);

    // Inserir no banco
    $stmt = $conn->prepare("INSERT INTO uploads (filename, filetype, filesize, filedata) VALUES (?, ?, ?, ?)");
    $stmt->bind_param("ssis", $fileNameHashed, $fileType, $fileSize, $fileData);

    if ($stmt->execute()) {
        echo "✅ Upload feito com sucesso!";
    } else {
        echo "❌ Falha ao fazer upload: " . $stmt->error;
    }

    $stmt->close();
} else {
    echo "Nenhum arquivo enviado.";
}

$conn->close();
?>
