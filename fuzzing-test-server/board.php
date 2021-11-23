<?php 

error_reporting(E_ALL);
ini_set("display_errors", 1);

function query_all_fetch(){
	$mysql = new mysqli("localhost", "root", "fuzzing", "fuzzing");
        $execute = $mysql->query("SELECT title, contents FROM board");
        while($fetch = $execute->fetch_assoc()){
                echo $fetch['title']. "&nbsp&nbsp|&nbsp&nbsp";
                echo $fetch['contents']."<br>";
        }

}

if(isset($_GET['title'])){
	$mysql = new mysqli("localhost", "root", "fuzzing", "fuzzing");
	$result = $mysql->query("SELECT title, contents FROM board WHERE title='".$_GET['title']."'");
	$board = $result->fetch_row();
	if(isset($board[0]) && isset($board[1])){
		echo "title : ".$board[0]."<br>";
		echo "contents : ".$board[1]."<br>";

	}else{
		query_all_fetch();
	}
}else{
	query_all_fetch();
}

?>

<form method="GET">
<input type="text" name="title">
<input type="submit" name="submit">
</form>
