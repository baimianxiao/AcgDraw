<?php
$dbhost = 'localhost'; // mysql服务器主机地址
$dbuser = 'arknightsdraw';  // mysql用户名
$dbpass = 'wyc18971346783'; // mysql用户名密码
$dbname = 'arknightsdraw';// 规定默认使用的数据库
$conn = mysqli_connect($dbhost, $dbuser, $dbpass,$dbname);
if(! $conn )
{
  exit("Connection failed:".mysqli_connect_error());
}
//异常Mysql链接捕获
$sql = "CREATE TABLE Global( ".
        "global_times INT NOT NULL AUTO_INCREMENT, ".
        "request_ip VARCHAR(100) NOT NULL, ".
        "request_type VARCHAR(40) NOT NULL, ".
        "request_id VARCHAR(40) NOT NULL, ".
        "PRIMARY KEY ( global_times ))ENGINE=InnoDB DEFAULT CHARSET=utf8; ";
$retval = mysqli_query( $conn, $sql);
if(! $retval )
{
  exit('数据表创建失败: ' . mysqli_error($conn));
}
echo("初始化成功")
?>