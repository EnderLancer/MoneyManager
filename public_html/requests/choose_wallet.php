<?php
    $walletId = filter_var(trim($_GET['walletId']), FILTER_SANITIZE_STRING);
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
        $resultWallet = $mysql->query("
        SELECT `wallet`.`wallet_id`, `wallet`.`wallet_name`, `access_lvl`.`access_level_name`, `currency`.`currency_symbol`
        FROM ((`wallet` INNER JOIN `wallet_access` ON `wallet`.`wallet_id`=`wallet_access`.`wallet_id`)
		INNER JOIN `access_lvl` ON `wallet_access`.`access_level_id`=`access_lvl`.`access_level_id`)
        INNER JOIN `currency` ON `wallet`.`wallet_currency_id`=`currency`.`currency_id`
        WHERE `wallet_access`.`user_id` = '$userId'
		AND `wallet`.`wallet_id` = '$walletId' ");
        
        $availableWallets = $resultWallet->fetch_assoc();
        
        $resultRecords = $mysql->query("
        SELECT `records`.`records_id`, `records`.`record_name`, `records`.`datetime`, `records`.`volume`, `action`.`action_id`, `action`.`action_name`
        FROM `records` INNER JOIN `action` ON `records`.`action_id`=`action`.`action_id`
        WHERE `records`.`wallet_id` = '$walletId' ");
        
        $availableWallets["records"] = array();
        
        while($record = $resultRecords->fetch_assoc())
        {
            $availableWallets["records"][] = $record;
        }
    }
    echo json_encode( $availableWallets, JSON_UNESCAPED_UNICODE );
    $mysql->close();
    
    //header('Location: /');
?>