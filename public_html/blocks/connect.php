<?php
    $host='localhost'; // имя хоста (уточняется у провайдера)
    $database='id12652518_wallet_manager'; // имя базы данных, которую вы должны создать
    $user='id12652518_artemon'; // заданное вами имя пользователя, либо определенное провайдером
    $pswd='Passwordart1_'; // заданный вами пароль
     
    $mysql = new mysqli($host, $user, $pswd, $database);
?>