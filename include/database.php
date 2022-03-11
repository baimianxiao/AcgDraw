<?php
//版本信息，用于更新
$_updateVersionControl = "1.0.0";
$_updateVersion = "1";

include("./config.php");

//异常Mysql链接捕获
$mysqliConn = mysqli_connect($mysqliHost, $mysqliUser, $mysqliPassword, $mysqliName);
if (!$mysqliConn) {
    exit("Connection failed:" . mysqli_connect_error());
}

//
function global_change(){
    
}

//
function character_select(){

}

//
function character_insert(){

}

//
function character_delete(){

}

function table_select(){

}

//
function table_insert(){

}

//
function table_delete(){
    
}