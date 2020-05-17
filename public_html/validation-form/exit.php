<?php
    setcookie('fName', $_COOKIE['fName'], time() - 3600 * 24, "/");
    setcookie('lName', $_COOKIE['lName'], time() - 3600 * 24, "/");
    header('Location: /');
?>