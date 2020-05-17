<?php
    $walletCurrId = filter_var(trim($_GET['currId']), FILTER_SANITIZE_STRING);
    $walletName = filter_var(trim($_GET['name']), FILTER_SANITIZE_STRING);
    $userId = filter_var(trim($_GET['userId']), FILTER_SANITIZE_STRING);
    $pass = filter_var(trim($_GET['pass']), FILTER_SANITIZE_STRING);
    
    require "../blocks/connect.php";
    
    $result = $mysql->query("SELECT * FROM `users` WHERE `user_id` = '$userId' 
    AND `password` = '$pass'");
    
    $user = $result->fetch_assoc();
    if(count((array) $user) == 0) {
        echo "ERR by create wallet";
        exit();
    }
    else {
    
    $mysql->query( "INSERT INTO `wallet`(`wallet_name`, `wallet_owner_id`, `wallet_currency_id`) 
                    VALUES ('$walletName', '$userId', '$walletCurrId')" );
    $walletId=mysqli_insert_id($mysql);
    $mysql->query( "INSERT INTO `wallet_access`(`wallet_id`, `user_id`, `access_level_id`) 
                    VALUES ('$walletId', '$userId', '1')" );
                    
    $cart = array(
      "walletId" => $walletId,
      "walletName" => $walletName,
      "walletCurrencyId" => $walletCurrId
    );
    
    echo json_encode( $cart, JSON_UNESCAPED_UNICODE );                
    
    }
    $mysql->close();
    
    //header('Location: /');
?>