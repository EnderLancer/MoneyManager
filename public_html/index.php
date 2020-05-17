<!DOCTYPE html>
<html lang="ru">
<head>
	<meta charset="UTF-8">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<meta http-equiv="X-UA-Compatible" content="ie=edge">
	<title>Document</title>
	<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css">
	<link rel="stylesheet" href="css/style.css">
</head>
<body>
    <div class="conteiner mt-4">
        <?php
            if(empty($_COOKIE['fName']) || $_COOKIE['fName'] == ''):
        ?>
    	<div class="row">
    		<div class="col">
    			<h1>Форма регистрации</h1>
				<form action="validation-form/check.php" method="post">
					<input type="text" class="form-control" name="first_name" id="first_name" placeholder="Имя"><br>
					<input type="text" class="form-control" name="last_name" id="last_name" placeholder="Фамилия"><br>
					<input type="text" class="form-control" name="login" id="login" placeholder="Логин"><br>
					<input type="text" class="form-control" name="email" id="email" placeholder="Электронная почта"><br>
					<input type="password" class="form-control" name="pass" id="pass" placeholder="Пароль"><br>
					<button class="btn btn-success" type="submit">Зарегистрировать</button> 
				</form>
    		</div>
    		<div class="col">
    			<h1>Форма авторизации</h1>
				<form action="validation-form/auth.php" method="post">
					<input type="text" class="form-control" name="login" id="login" placeholder="Электронная почта"><br>
					<input type="password" class="form-control" name="pass" id="pass" placeholder="Пароль"><br>
					<button class="btn btn-success" type="submit">Войти</button> 
				</form>  
    		</div>
    	</div>
    	<?php else:?>
    	    <p>Привет <?=$_COOKIE['lName']." ".$_COOKIE['fName']?>. Чтобы выйти нажми 
    	        <a href="validation-form/exit.php">здесь</a>.
    	    </p>
    	<?php endif; ?>
    	
	</div>
	
</body>
</html>