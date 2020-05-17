<?php
    $walletId = filter_var(trim($_GET['walletId']), FILTER_SANITIZE_STRING);
    $userId = filter_var(trim($_GET['userId']), FILTER_SANITIZE_STRING);
    $pass = filter_var(trim($_GET['pass']), FILTER_SANITIZE_STRING);
    
    require "../blocks/connect.php";
    
    $result = $mysql->query("
    SELECT * 
    FROM `users` 
    WHERE `users`.`user_id` = '$userId' 
    AND `users`.`password` = '$pass' 
    AND (   SELECT `access_level_id` 
            FROM `wallet_access`
            WHERE `wallet_access`.`user_id` = '$userId'
            AND `wallet_access`.`wallet_id` = '$walletId') IN (1, 2)");
    
    $user = $result->fetch_assoc();
    $cart = array();
    if(count((array) $user) == 0) {
        $cart = array(
            "code" => 1,
            "msg" => "You don't have permission."
        );
    }
    else {
        $mysql->query( "DELETE FROM `wallet` WHERE `wallet_id` = '$walletId'" );
    }
    echo json_encode( $cart, JSON_UNESCAPED_UNICODE );
    $mysql->close();
    
    //header('Location: /');
?>