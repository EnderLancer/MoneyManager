<?php

    require "../blocks/connect.php";
    
    $resultAccessLvl = $mysql->query(" SELECT * FROM `access_lvl` ");
    $resultAction = $mysql->query(" SELECT * FROM `action` ");
    $resultCurrency = $mysql->query(" SELECT * FROM `currency` ");
    $resultStatus = $mysql->query(" SELECT * FROM `status` ");
    
    $availableWallets = array();
    
    while($wallet = $resultAccessLvl->fetch_assoc())
    {
        $availableWallets["accessLvl"][] = $wallet;
    }
    while($wallet = $resultAction->fetch_assoc())
    {
        $availableWallets["action"][] = $wallet;
    }
    while($wallet = $resultCurrency->fetch_assoc())
    {
        $availableWallets["currency"][] = $wallet;
    }
    while($wallet = $resultStatus->fetch_assoc())
    {
        $availableWallets["status"][] = $wallet;
    }
    
    echo json_encode( $availableWallets, JSON_UNESCAPED_UNICODE );
    $mysql->close();
    
    //header('Location: /');
?>