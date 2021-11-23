<?php 

function ssti($pay){
    $cu = curl_init();
    curl_setopt($cu, CURLOPT_URL, "http://localhost:5000?payload=".urlencode($pay));

    $result = curl_exec($cu);

    curl_close($cu);

    return $result;
}

if($_GET['pay']){
	ssti($_GET['pay']);
}else{
	header("Location: /ssti.php?pay=test");
}

?>
