#!/bin/bash
index="index.php"
planty_pics="planty_pics.php"
watch_planty="watch_planty.php"
#webserver_dir="/var/www/html"
webserver_dir="/home/pi/temp"

cp $index $webserver_dir
cp subpages/$planty_pics $webserver_dir/subpages
cp subpages/$watch_planty $webserver_dir/subpages
