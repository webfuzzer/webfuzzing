<?php 

error_reporting(E_ALL);
ini_set("display_errors", 1);

if(isset($_POST['uid']) && isset($_POST['upw'])){
	$mysql = new mysqli("localhost", "root", "fuzzing", "fuzzing");
	$sql = "SELECT uid FROM user WHERE uid='".$_POST['uid']."' and upw='".$_POST['upw']."'";
	$execute = $mysql->query($sql);
	$result = $execute->fetch_row();
	if(isset($result[0])){
		echo "Login Success";
	}
}else{
	echo "<script>history.back(-1);</script>";
}


?>
