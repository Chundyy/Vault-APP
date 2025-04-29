<?php require 'auth.php'; ?>
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>Upload de Arquivo</title>
    <style>
        body {
            background: #f0f4f8;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }

        .upload-container {
            background: #ffffff;
            padding: 30px 40px;
            border-radius: 12px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.1);
            text-align: center;
            width: 100%;
            max-width: 400px;
        }

        h2 {
            margin-bottom: 20px;
            color: #333;
        }

        input[type="file"] {
            margin: 20px 0;
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 6px;
            background-color: #fafafa;
        }

        input[type="submit"] {
            background-color: #007bff;
            color: white;
            border: none;
            padding: 12px 20px;
            border-radius: 8px;
            font-size: 16px;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }

        input[type="submit"]:hover {
            background-color: #0056b3;
        }

        label {
            font-size: 15px;
            color: #555;
        }
    </style>
</head>
<body>

    <div class="upload-container">
        <h2>📤 Enviar Arquivo</h2>
        <form action="upload.php" method="post" enctype="multipart/form-data">
            <label for="uploaded_file">Escolha o arquivo:</label><br>
            <input type="file" name="uploaded_file" id="uploaded_file" required><br><br>
            <input type="submit" value="Enviar">
        </form>
    </div>

</body>
</html>
