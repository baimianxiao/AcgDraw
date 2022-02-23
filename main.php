<?php
//引入设置文件和数据库操作
include("./include/config.php");
include("./include/database.php");

$background = "image/gacha/bg.png";
$background1 = "image/gacha/bg1.png";
//背景图片与遮罩图片路径
$bgpath = "image/gacha/";
$chpath = "image/ch/";
$classpath = "image/class/";
/*
图片文件路径
bgpath为不同星级背景路径
chpath为相关人物图片路径
classpath为不同职业图标路径
*/
$outPut2 = "image/out/";
//输出图片目录的路径
$type = $_GET['type'];
$id = $_GET['id'];
/*
获取入参
$type指出返回的类型,支持png,image,json
$someThingid指定群号或者QQ号,
*/
if (!$id) {
    $id = "12345";
}
if (!$type) {
    $type = "默认";
} else {
}
//没有入参id就直接爬
if (getenv('HTTP_CLIENT_IP') && strcasecmp(getenv('HTTP_CLIENT_IP'), 'unknown')) {
    $ip = getenv('HTTP_CLIENT_IP');
} else if (getenv('HTTP_X_FORWARDED_FOR') && strcasecmp(getenv('HTTP_X_FORWARDED_FOR'), 'unknown')) {
    $ip = getenv('HTTP_X_FORWARDED_FOR');
} else if (getenv('REMOTE_ADDR') && strcasecmp(getenv('REMOTE_ADDR'), 'unknown')) {
    $ip = getenv('REMOTE_ADDR');
} else if (isset($_SERVER['REMOTE_ADDR']) && $_SERVER['REMOTE_ADDR'] && strcasecmp($_SERVER['REMOTE_ADDR'], 'unknown')) {
    $ip = $_SERVER['REMOTE_ADDR'];
}
$userIp =  preg_match('/[\d\.]{7,15}/', $ip, $matches) ? $matches[0] : '';
//以上是获取用户的IP地址
$randomname = date('Ymd_H_i_s') . rand(1, 9999); //随机生成存储的文件名称
$sixStarHasGot = 0;

$dbhost = 'localhost'; // mysql服务器主机地址
$dbuser = 'arknightsdraw';  // mysql用户名
$dbpass = 'wyc18971346783'; // mysql用户名密码
$dbname = 'arknightsdraw'; // 规定默认使用的数据库

$readMain = "SELECT global_times FROM Global";
$sqlMain = mysqli_query($conn, $readMain);
if (!$sqlMain) {
    $sql = "CREATE TABLE Global( " .
        "global_times INT NOT NULL AUTO_INCREMENT, " .
        "request_ip VARCHAR(100) NOT NULL, " .
        "request_type VARCHAR(40) NOT NULL, " .
        "request_id VARCHAR(40) NOT NULL, " .
        "PRIMARY KEY ( global_times )); ";
    mysqli_query($conn, $sql);
}
//以上是判断是否需要初始化数据库
$sql_insert = "INSERT INTO Global " .
    "(request_ip,request_type,request_id) " .
    "VALUES " .
    "('$userIp','$type','$id')";
mysqli_select_db($conn, 'arknightsdraw');
$retval = mysqli_query($conn, $sql_insert);
$sql_id = "userid_" . "$id";   //由于mysql不支持纯数字表名，这里为id加一个前缀
$getTimes = "SELECT MAX(times) FROM $sql_id";
$times = mysqli_query($conn, $getTimes);
if ($times != 0 && $times < 10) {
} elseif ($times >= 10) {
    $delUser = "DROP TABLE $sql_id";
    mysqli_query($conn, $delUser);
} else {
    $createUser = "CREATE TABLE $sql_id( " .
        "times INT NOT NULL AUTO_INCREMENT," .
        "six_Star_Has_Got Integer(100), " .
        "run_Result_1 Text(100), " .
        "run_Result_2 Text(100), " .
        "run_Result_3 Text(100), " .
        "run_Result_4 Text(100), " .
        "run_Result_5 Text(100), " .
        "run_Result_6 Text(100), " .
        "run_Result_7 Text(100), " .
        "run_Result_8 Text(100), " .
        "run_Result_9 Text(100), " .
        "run_Result_10 Text(100), " .
        "PRIMARY KEY (times)); ";
    $varsqlUser = mysqli_query($conn, $createUser);
    //这里懒得写异常捕获了x
}
$srcBg = imagecreatefrompng($background);
$im = imagecreatetruecolor(imagesx($srcBg), imagesy($srcBg));
imagecopyresampled($im, $srcBg, 0, 0, 0, 0, imagesx($srcBg), imagesy($srcBg), imagesx($srcBg), imagesy($srcBg));
//绘制背景
for ($i = 1; $i <= 10; $i++) {
    $bgx = 70 + ($i - 1) * 82;
    $chx = 70 + ($i - 1) * 82;
    $classx = 80 + ($i - 1) * 82;
    $starType = rand(0, 1000);
    $classType = rand(0, 7);
    $classArr = ["caster", "medic", "pioneer", "sniper", "special", "support", "tank", "warrior"];
    $classLoad = $classArr[$classType];
    if ($starType >= 0 && $starType <= 20) {
        $starLoad = "6";
        $sixStarHasGot = 1;
    } elseif ($starType >= 21 && $starType <= 100) {
        $starLoad = "5";
    } elseif ($starType >= 101 && $starType <= 400) {
        $starLoad = "4";
    } elseif ($starType >= 401 && $classLoad == "special") {
        $starLoad = "4";
    } else {
        $starLoad = "3";
    }
    $filepath = $chpath . $classLoad . "/" . $starLoad;
    $file_arr = [];
    $handler = opendir($filepath);
    while (($filename = readdir($handler)) !== false) {
        if ($filename != "." && $filename != "..") {
            array_push($file_arr, $filename);
        }
    }
    $key = array_rand($file_arr, 1);
    $ch = $filepath . "/" . $file_arr[$key];
    $bg = $bgpath . $starLoad . ".png";
    $class = $classpath . $classLoad . ".png";
    $srcImage1 = imagecreatefrompng($bg);
    imagecopyresampled($im, $srcImage1, $bgx, 0, 0, 0, imagesx($srcImage1), imagesy($srcImage1), imagesx($srcImage1), imagesy($srcImage1));
    $srcImage2 = imagecreatefrompng($ch);
    imagecopyresampled($im, $srcImage2, $chx, 115, 20, 0, 120, 240, imagesx($srcImage2), imagesy($srcImage2));
    $srcImage3 = imagecreatefrompng($class);
    imagecopyresampled($im, $srcImage3, $classx, 323, 0, 0, 59, 59, imagesx($srcImage3), imagesy($srcImage3));
    $savemsg = $bg . "|" . $ch . "|" . $class;
    $savearr[$i] = $savemsg;
}
$user_insert = "INSERT INTO $sql_id " .
    "(six_Star_Has_Got,run_Result_1,run_Result_2,run_Result_3,run_Result_4,run_Result_5,run_Result_6,run_Result_7,run_Result_8,run_Result_9,run_Result_10) " .
    "VALUES " .
    "($sixStarHasGot,'$savearr[1]','$savearr[2]','$savearr[3]','$savearr[4]','$savearr[5]','$savearr[6]','$savearr[7]','$savearr[8]','$savearr[9]','$savearr[10]');";
mysqli_select_db($conn, 'arknightsdraw');
$user_retval = mysqli_query($conn, $user_insert);
$srcBg1 = imagecreatefrompng($background1);
imagecopyresampled($im, $srcBg1, 0, 0, 0, 0, imagesx($srcBg1), imagesy($srcBg1), imagesx($srcBg1), imagesy($srcBg1));
imagepng($im, $outPut2 . $randomname . ".png");
$url = $outPut1 . $randomname . ".png";

if ($type == "png") {
    header("Location:" . $url);;
} elseif ($type == "json") {
    header('Content-Type:application/json; charset=utf-8');
    $arr = array('six' => $sixStarHasGot, 'url' => $url);
    $out = str_replace("\\", "", json_encode($arr));
    exit($out);
} elseif ($type == "image") {
    header("Content-Type:image/jpeg");
    imagepng($im,);
} else {
    header("Content-Type:image/jpeg");
    imagepng($im,); //默认返回
}
//根据入参不同的返回
