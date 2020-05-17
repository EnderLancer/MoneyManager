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
        $resultRecords = $mysql->query("
        SELECT `records`.`records_id`, `records`.`record_name`, `records`.`datetime`, `records`.`volume`, `action`.`action_id`, `action`.`action_name`
        FROM `records` INNER JOIN `action` ON `records`.`action_id`=`action`.`action_id`
        WHERE `records`.`wallet_id` = '$walletId' ");
        
        $availableWallets = array();
        
        while($record = $resultRecords->fetch_assoc())
        {
            $availableWallets[] = $record;
        }
    }
    echo json_encode( $availableWallets, JSON_UNESCAPED_UNICODE );
    $mysql->close();
    
    //header('Location: /');
?>