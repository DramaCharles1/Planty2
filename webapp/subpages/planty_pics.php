<?php

$dir="/var/www/html/Images";
$images = glob($dir . "/*.jpg");

$amount = 7;
$plantyImages = array();
	
for ($x = 1; $x <= $amount; $x++) {
	$plantyImages[$x] = str_replace("/var/www/html/","",$images[count($images)-$x]);
}
?>

<head>
	<style>
		table, th, td {
			border: 1px solid black;
			border-collapse: collapse;
		}
	
	</style>
	<title>Planty</title>
	<meta http-equiv="content-type" content="text/html;charset=utf-8" />
	<meta name="generator" content="Geany 1.29" />
</head>

<body>	

<h1>Showing <?php echo $amount?> daily pictures</h1>

	<?php
	for ($x = 1; $x <= $amount; $x++) {
		echo "<img src=../$plantyImages[$x] width=\"512\" height=\"384\" alt=\"image $x\" align=\"top\" />";
		
	}?>
	

</body>
