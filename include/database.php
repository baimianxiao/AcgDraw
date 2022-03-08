<?php
//版本信息，用于更新
$_updateVersionControl = "1.0.0";
$_updateVersion = "1";

include("./config.php");
$mysqliConn = mysqli_connect($mysqliHost, $mysqliUser, $mysqliPassword, $mysqliName);
if (!$mysqliConn) {
    exit("Connection failed:" . mysqli_connect_error());
}
//异常Mysql链接捕获