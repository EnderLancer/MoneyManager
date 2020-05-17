<?php
    $fName = filter_var(trim($_POST['first_name']), FILTER_SANITIZE_STRING);
    $lName = filter_var(trim($_POST['last_name']), FILTER_SANITIZE_STRING);
    $login = filter_var(trim($_POST['login']), FILTER_SANITIZE_STRING);
    $pass = filter_var(trim($_POST['pass']), FILTER_SANITIZE_STRING);
    
    if(mb_strlen($login) < 5 || mb_strlen($login) > 90) {
        echo "ERR LOGIN HHHHHHHHHH";
        exit();
    }
    
    $pass = md5($pass);
    
    require "../blocks/connect.php";
    
    $mysql->query("INSERT INTO `users` (`first_name`, `last_name`, `login`, `password`, `status_id`) 
    VALUES('$fName', '$lName', '$login', '$pass', '1')");
    
    setcookie('fName', $fName, time() + 3600 * 24, "/");
    setcookie('lName', $lName, time() + 3600 * 24, "/");
    
    $mysql->close();
    
    header('Location: /');
?>