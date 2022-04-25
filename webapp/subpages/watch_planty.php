<?php
$servername = "localhost";
$username="root";
$password="password";
$database="Planty2";

//Tables
$planty_data="Planty_data";
$planty_settings="Planty_settings";
$camera_data="Camera_data";
$camera_settings="Camera_settings";
  
$conn = new mysqli($servername, $username, $password, $database);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

$plant_insert_statement="SELECT * FROM $planty_data order by datetime desc limit 48";
$plant_result = $conn->query($plant_insert_statement);
$plant_rows = $plant_result->num_rows;

$camera_insert_statement="SELECT * FROM $camera_data order by datetime desc limit 10";
$camera_result = $conn->query($camera_insert_statement);
$camera_rows = $camera_result->num_rows;

$moisture_insert_statement="SELECT * FROM $planty_data order by datetime desc limit 24";
$moisture_result = $conn->query($moisture_insert_statement);
$moisture_rows = $moisture_result->num_rows;

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
	
 	<?php 
		echo "<table style=\"width:75%\">
				<tr> 
					<th>Date and time</th>
					<th>Plant</th>
					<th>Motor duration</th>
					<th>Motor power</th>
					<th>Temperature</th>
					<th>Humidity</th>
					<th>Light</th>
					<th>Natural light</th>
					<th>Moisture</th>
				</tr>";
		for ($x = 0; $x < $plantrow_cnt; $x++) {
			
			$row = $plant_result->fetch_array(MYSQLI_BOTH);
			$temp_date = $row["datetime"];
			$temp_plant = $row["plant"];
			$temp_motor_duration = $row["motor_duration"];
			$temp_motor_power = $row["motor_power"];
			$temp_temperature = $row["temperature"];
			$temp_humidity = $row["humidity"];
			$temp_light = $row["light"];
			$temp_light_wo_regulator = $row["light_wo_regulator"];
			$temp_moisture = $row["moisture"];
			echo 
			"<tr>
				<td>$temp_date</td>
				<td>$temp_plant</td>
				<td>$temp_motor_duration</td>
				<td>$temp_motor_power</td>
				<td>$temp_temperature</td>
				<td>$temp_humidity</td>
				<td>$temp_light</td>
				<td>$temp_light_wo_regulator</td>
				<td>$temp_moisture</td>
			</tr>";
		}		
		echo "</table>";
		$plant_result->free();
 	?>
 	
 	<h2>Planty Camera</h2>
 	
 	<?php 
		echo "<table style=\"width:75%\">
				<tr> 
					<th>Date and time</th>
					<th>Original pixels</th>
					<th>Green pixels</th>
					<th>Green percentage</th>
				</tr>";
		for ($x = 0; $x < $camerarow_cnt; $x++) {
			
			$row = $camera_result->fetch_array(MYSQLI_BOTH);
			$temp_date = $row["datetime"];
			$temp_original_pixels = $row["original_pixel"];
			$temp_green_pixels = $row["green_pixel"];
			$temp_green_percent = $row["green_percent"];
			echo 
			"<tr>
				<td>$temp_date</td>
				<td>$temp_original_pixels</td>
				<td>$temp_green_pixels</td>
				<td>$temp_green_percent</td>
			</tr>";
		}		
		echo "</table>";
		$camera_result->free();
 	?>
</body>
