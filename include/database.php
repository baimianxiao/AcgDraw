<?php
include("./config.php");
$mysqli_conn = mysqli_connect($mysqli_host, $mysqli_user, $mysqli_password, $mysqli_name);
if (!$mysqli_conn) {
    exit("Connection failed:" . mysqli_connect_error());
}
//异常Mysql链接捕获