<?php
    $servername = "localhost";
    $username="root";
    $password="password";
    $database="nano";
    $nano_data="nano_data";

    //mysql_connect(localhost,$username,$password);
    $conn = new mysqli($servername, $username, $password, $database);

    // Check connection
    if ($conn->connect_error) {
        die("Connection failed: " . $conn->connect_error);
    }

    $lastNanoUpdate_insert_statement="SELECT * FROM $nano_data order by datetime desc limit 1";
    $lastUpdateQuery = $conn->query($lastNanoUpdate_insert_statement);
    $lastUpdateResults = $lastUpdateQuery->fetch_array(MYSQLI_BOTH);
    $lastUpdateDatetime = $lastUpdateResults["datetime"];
    $plant1 = $lastUpdateResults["plant_1"];
    $plant2 = $lastUpdateResults["plant_2"];

    $moisture_plant1_plot_day = "/Images/nano/moisture_plant1_plot_day.png";
    $moisture_plant2_plot_day = "/Images/nano/moisture_plant2_plot_day.png";
?>

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
	"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">

<head>
	<style>
		table, th, td {
			border: 1px solid black;
			border-collapse: collapse;
		}
	
	</style>
	<title>Nano</title>
	<meta http-equiv="content-type" content="text/html;charset=utf-8" />
	<meta name="generator" content="Geany 1.29" />
</head>

<body>
    <h1>Nano</h1>
	Last update: <?php echo $lastUpdateDatetime?>
    <h2><?php echo $plant1?></h2>
	<img src="<?php echo $moisture_plant1_plot_day ?>" width="666" height="500" alt="Moisture plot 1" align="top"/>
    <h2><?php echo $plant2?></h2>
	<img src="<?php echo $moisture_plant2_plot_day ?>" width="666" height="500" alt="Moisture plot 2" align="top"/>
</body>
</html>