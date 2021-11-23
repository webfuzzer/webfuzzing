<?php 

setcookie('fuzzing', 'fuzzing', time()+3600);

?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    <a href="/search.php?search=1">search(xss)</a>
    <a href="/test.php?test=1">test(xss)</a>
    <a href="/cookie.php">cookie(xss)</a>
    <a href="headers.php">headers(xss)</a>
    <a href="/post.php">post(xss)</a>
    <a href="loop.php?a=1&b=1&c=1">loop(xss)</a>
    <a href="login.php">login(sqli)</a>
    <a href="/board.php?title=test">board(sqli)</a>
    <a href="/script.php">script(xss)</a>
    <a href="/openredirect.php">openredirect(open redirect)</a>
    <a href="/ssti.php">ssti(ssti)</a>
</body>
</html>
