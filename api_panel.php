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
mysqli_query($conn , "set names utf8");
$sql_insert = 'SELECT global_times, request_ip, 
        request_type, request_id
        FROM Global';
$retval = mysqli_query( $conn, $sql_insert );
echo "<h2>Arknights-Draw</h2>";
echo '<table border="1"><tr><td>序号</td><td>申请 IP</td><td>申请类型</td><td>申请 ID</td></tr>';
while($row = mysqli_fetch_array($retval, MYSQLI_ASSOC))
{
    echo "<tr><td> {$row['global_times']}</td> ".
         "<td>{$row['request_ip']} </td> ".
         "<td>{$row['request_type']} </td> ".
         "<td>{$row['request_id']} </td> ".
         "</tr>";
}
mysqli_select_db( $conn, 'arknightsdraw' );
?>