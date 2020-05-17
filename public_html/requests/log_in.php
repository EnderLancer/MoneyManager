<?php
    $login = filter_var(trim($_GET['login']), FILTER_SANITIZE_STRING);
    $pass = filter_var(trim($_GET['pass']), FILTER_SANITIZE_STRING);
    
    require "../blocks/connect.php";
    
    $result = $mysql->query("SELECT `user_id` FROM `users` WHERE `login` = '$login' 
    AND `password` = '$pass'");
    
    $user = $result->fetch_assoc();
    if(count((array) $user) == 0) {
        $cart = array(
            "code" => 1,
            "msg" => "Wrong login or password"
        );
    }
    else {
        $cart = array(
            "userId" => $user["user_id"]
        );               
    }
    echo json_encode( $cart, JSON_UNESCAPED_UNICODE );
    $mysql->close();
?>