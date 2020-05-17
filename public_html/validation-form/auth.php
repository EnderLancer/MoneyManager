<?php
    $login = filter_var(trim($_POST['login']), FILTER_SANITIZE_STRING);
    $pass = filter_var(trim($_POST['pass']), FILTER_SANITIZE_STRING);
    
    $pass = md5($pass);
    
    require "../blocks/connect.php";
    
    $result = $mysql->query("SELECT * FROM `users` WHERE `login` = '$login' 
    AND `password` = '$pass'");
    
    $user = $result->fetch_assoc();
    if(count($user) == 0) {
        echo "None";
        exit();
    }
    
    setcookie('fName', $user['first_name'], time() + 3600 * 24, "/");
    setcookie('lName', $user['last_name'], time() + 3600 * 24, "/");
    
    
    $mysql->close();
    
    header('Location: /');
?>