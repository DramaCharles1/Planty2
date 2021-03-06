<?php
//phpinfo();

$servername = "localhost";
$username="root";
$password="password";
$database="Planty2";

//Tables
$planty_data="Planty_data";
$planty_settings="Planty_settings";
$camera_data="Camera_data";
$camera_settings="Camera_settings";
  
//mysql_connect(localhost,$username,$password);
$conn = new mysqli($servername, $username, $password, $database);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

$lastCameraUpdate_insert_statement="SELECT * FROM $camera_data order by datetime desc limit 1";
$lastCameraUpdateQuery = $conn->query($lastCameraUpdate_insert_statement);
$lastCameraUpdateResults= $lastCameraUpdateQuery->fetch_array(MYSQLI_BOTH);
$lastCameraUpdateDatetime = $lastCameraUpdateResults["datetime"];
//$lastCameraUpdateResults->free();

$lastPlantyUpdate_insert_statement="SELECT * FROM $planty_data order by datetime desc limit 1";
$lastUpdateQuery = $conn->query($lastPlantyUpdate_insert_statement);
$lastUpdateResults = $lastUpdateQuery->fetch_array(MYSQLI_BOTH);
$lastUpdateDatetime = $lastUpdateResults["datetime"];
//$lastUpdateResults->free();

$dir="/var/www/html/Images";
$images = glob($dir . "/*.jpg");

$image1 = str_replace("/var/www/html/","",$images[count($images)-1]); 
$image2 = str_replace("/var/www/html/","",$images[count($images)-2]); 
$image3 = str_replace("/var/www/html/","",$images[count($images)-3]); 
$image4 = str_replace("/var/www/html/","",$images[count($images)-4]); 

$moisture_plot_day = "Images/moisture_plot_day.png";
$moisture_plot_three_day = "Images/moisture_plot_three_day.png";
$moisPlotWeek = "MoisturePlotWeek.png";
$green_plot_Week = "Images/green_plot_week.png";
$green_plot_month = "Images/green_plot_month.png";
$light_plot = "Images/light_plot.png";
$light_plot_three_day = "Images/light_plot_three_day.png";
$lightPlotWeek = "LightPlotWeek.png";

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
	<title>Planty</title>
	<meta http-equiv="content-type" content="text/html;charset=utf-8" />
	<meta name="generator" content="Geany 1.29" />
</head>

<body>
	<h1>Planty</h1>
	Last update: <?php echo $lastUpdateDatetime?>
	
	<h2>Today's picture</h2>
	From: <?php echo $lastCameraUpdateDatetime?>
	<img src="<?php echo $image1 ?>" width="666" height="500" alt="image 1" align="top"/>
	<h2>Sunlight</h2>
	<img src="<?php echo $light_plot ?>" width="666" height="500" alt="Sunlight" align="top"/>
	<h2>Sunlight last 3 days</h2>
	<img src="<?php echo $light_plot_three_day ?>" width="666" height="500" alt="Sunlight last 3 days" align="top"/>
	<h2>Moisture</h2>
	<img src="<?php echo $moisture_plot_day ?>" width="666" height="500" alt="Moisture plot" align="top"/>
	<h2>Moisture last 3 days</h2>
	<img src="<?php echo $moisture_plot_three_day ?>" width="666" height="500" alt="Moisture plot last 3 days" align="top"/>
	<h2>Growth week</h2>
	<img src="<?php echo $green_plot_Week ?>" width="666" height="500" alt="Growth" align="top"/>
	<h2>Growth month</h2>
	<img src="<?php echo $green_plot_month ?>" width="666" height="500" alt="Growth" align="top"/>

	<!--
	<img src="<?php echo $image2 ?>" width="512" height="384" alt="image 2" align="top"/>
	<img src="<?php echo $image3 ?>" width="512" height="384" alt="image 3" align="top"/>
	<img src="<?php echo $image4 ?>" width="512" height="384" alt="image 3" align="top"/>
-->
 	 	
 	<form action="subpages/watch_planty.php">
    <input type="submit" value="Two day data" />
	</form>
	
	<form action="subpages/graph.php">
    <input type="submit" value="Another graph" />
	</form>
	
	<form action="subpages/planty_pics.php">
    <input type="submit" value="Show daily pictures" />
	</form>

	<form action="subpages/nano.php">
    <input type="submit" value="Nano" />
	</form>
	
<!--
	<form action="subpages/planty_pics.php" method="get">
	How many days to show: <input type="text" name="amount">
	</form>
-->
	
 	<img src="https://s3.amazonaws.com/codecademy-content/courses/web-101/web101-image_brownbear.jpg" />
	
</body>

</html>
