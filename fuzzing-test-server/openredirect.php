<?php 

if(isset($_GET['url'])){
	header("Location: ".$_GET['url'], 302);
}else{
	echo '<a href="/openredirect.php?url=/">test</a>';
}

?>
