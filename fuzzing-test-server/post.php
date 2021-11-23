<?php 

if(isset($_POST['string'])){
	echo $_POST['string'];
}else{
	?>
		<form method="POST">
			<input type="text" name="string">
			<input type="submit" name="submit">
		</form>
	<?php
}

?>
