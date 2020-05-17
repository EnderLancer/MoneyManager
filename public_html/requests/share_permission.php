<?php
    $walletId = filter_var(trim($_GET['walletId']), FILTER_SANITIZE_STRING);
    $addUserId = filter_var(trim($_GET['addUserId']), FILTER_SANITIZE_STRING);
    $addUserAccessId = filter_var(trim($_GET['addUserAccessId']), FILTER_SANITIZE_STRING);
    $userId = filter_var(trim($_GET['userId']), FILTER_SANITIZE_STRING);
    $pass = filter_var(trim($_GET['pass']), FILTER_SANITIZE_STRING);
    
    require "../blocks/connect.php";
    
    $result = $mysql->query("SELECT `users`.* 
    FROM (`users` INNER JOIN `wallet_access` ON `users`.`user_id`=`wallet_access`.`user_id`)
    	INNER JOIN `wallet` ON `wallet_access`.`wallet_id`=`wallet`.`wallet_id`
    WHERE `users`.`user_id` = '$userId'
        AND `users`.`password` = '$pass'
    	AND `wallet_access`.`access_level_id` <= '$addUserAccessId'
        AND `wallet`.`wallet_id` = '$walletId'");
    
    $cart = array();
    $user = $result->fetch_assoc();
    if(count((array) $user) == 0) {
        $cart = array(
            "code" => "1",
            "msg" => "You don't have permission"
        );
    }
    else {
    
        $mysql->query( "INSERT INTO `wallet_access`(`wallet_id`, `user_id`, `access_level_id`) 
                        VALUES ('$walletId', '$addUserId', '$addUserAccessId')" );
        
        $userLogin = $mysql->query("SELECT `users`.`login` 
            FROM `users` 
            WHERE `users`.`user_id` = '$addUserId'");
        
        $cart = array(
          $userLogin->fetch_assoc()
        );
    }
    echo json_encode( $cart, JSON_UNESCAPED_UNICODE );   
    $mysql->close();
    
    //header('Location: /');
?>