<?php
    $userId = filter_var(trim($_GET['userId']), FILTER_SANITIZE_STRING);
    $pass = filter_var(trim($_GET['pass']), FILTER_SANITIZE_STRING);
    
    require "../blocks/connect.php";
    
    $resultAuth = $mysql->query("
    SELECT * 
    FROM `users` 
    WHERE `users`.`user_id` = '$userId' 
    AND `users`.`password` = '$pass' ");
    
    $user = $resultAuth->fetch_assoc();
    $availableWallets = array();
    if(count((array) $user) == 0) {
        $availableWallets = array(
          "code" => "1",
          "msg" => "Wrong user!"
        );
    }
    else {
        $result = $mysql->query("
        SELECT `wallet`.`wallet_id`, `wallet`.`wallet_name`, `wallet`.`wallet_owner_id`, `currency`.`currency_symbol` 
        FROM `wallet` INNER JOIN `currency` ON `wallet`.`wallet_currency_id`=`currency`.`currency_id`
        WHERE `wallet`.`wallet_id` IN 
        (   SELECT `wallet_id` 
            FROM `wallet_access`
            WHERE `user_id` = '$userId') ");
        
        while($wallet = $result->fetch_assoc())
        {
            $availableWallets[] = $wallet;
        }
    }
    echo json_encode( $availableWallets, JSON_UNESCAPED_UNICODE );
    $mysql->close();
    
    //header('Location: /');
?>