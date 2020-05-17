<?php
    $findUser = filter_var(trim($_GET['findUser']), FILTER_SANITIZE_STRING);
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
        SELECT `users`.`user_id`, `users`.`first_name`, `users`.`last_name`, `users`.`login`
        FROM `users`
        WHERE `users`.`login` LIKE '%$findUser%' ");
        
        $availableWallets = array();
        
        while($users = $resultRecords->fetch_assoc())
        {
            $availableWallets[] = $users;
        }
    }
    echo json_encode( $availableWallets, JSON_UNESCAPED_UNICODE );
    $mysql->close();
    
    //header('Location: /');
?>