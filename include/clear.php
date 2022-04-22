 <?php 
include("./config.php");

$flag = 1; //将执行标志设置为1，默认为执行 
ignore_user_abort(); //客户端断开时，可以让脚本继续在后台执行 
set_time_limit(0); //忽略php.ini设置的脚本运行时间限制 
do{ 
$flagfile = "../data/clearlock.txt"; //标志放置在文件“clearlock.txt”中。“0”表示停止执行，“1”表示继续执行 
if(file_exists($flagfile) && is_readable($flagfile)) { //读取文件内容 
$fh = fopen($flagfile,"r"); 
while (!feof($fh)) { 
$flag = fgets($fh); //存储标志 
} 
fclose($fh); 
} 
$dir = "../data/image/out/"; //你的临时目录位置 
$handle=opendir("{$dir}/"); 
while (false !== ($file=readdir($handle))) { 
if ($file!="." && $file!=".." && !is_dir("{$dir}/{$file}")) { 
@unlink ("{$dir}/{$file}"); 
} 
} 
closedir($handle); //关闭由 opendir() 函数打开的目录 
sleep($cleartime); //执行一个周期后，休眠$interval时间，休眠结束后脚本继续执行 
}while($flag); 
