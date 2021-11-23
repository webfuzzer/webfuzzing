<?php 

if(isset($_GET['script'])){
	$script = $_GET['script'];
	echo "
	<script>
		var script = '$script';
		console.log(script);
	</script>
	";
}else{
	echo "
	<form method='GET'>
		<input type='text' name='script'>
		<input type='submit' name='submit'>
	</form>
	";
}

?>

