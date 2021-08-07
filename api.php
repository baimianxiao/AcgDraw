<?php
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
$outPut1 = "http://www.baimianxiao.cn/api/mrfz/image/out/";
$outPut2 ="image/out/";
//输出图片目录的路径
$type=$_GET['type'];
$someThingid=$_GET['id'];
/*
获取入参
$type指出返回的类型,支持png,image,json
$someThingid指定群号或者QQ号,
*/
if (!$someThingid)
{
    exit("内部错误:您没有输入id。");
}
else
{
    $id=$someThingid;
}
if (!$type)
{
    $type="默认";
}
else
{
}
//没有入参id就直接爬
if (getenv('HTTP_CLIENT_IP') && strcasecmp(getenv('HTTP_CLIENT_IP'), 'unknown')) 
{
    $ip = getenv('HTTP_CLIENT_IP');
} 
else if (getenv('HTTP_X_FORWARDED_FOR') && strcasecmp(getenv('HTTP_X_FORWARDED_FOR'), 'unknown')) 
{
    $ip = getenv('HTTP_X_FORWARDED_FOR');
} 
else if (getenv('REMOTE_ADDR') && strcasecmp(getenv('REMOTE_ADDR'), 'unknown'))
{
    $ip = getenv('REMOTE_ADDR');
} else if (isset($_SERVER['REMOTE_ADDR']) && $_SERVER['REMOTE_ADDR'] && strcasecmp($_SERVER['REMOTE_ADDR'], 'unknown'))
{
    $ip = $_SERVER['REMOTE_ADDR'];
}
$userIp =  preg_match ( '/[\d\.]{7,15}/', $ip, $matches ) ? $matches [0] : '';

$sixStarhasGot=0;
$randomname = date('Ymd_H_i_s').rand(1,9999);

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
$sql_insert = "INSERT INTO Global ".
              "(request_ip,request_type,request_id) ".
              "VALUES ".
              "('$userIp','$type','$someThingid')";
mysqli_select_db( $conn, 'arknightsdraw' );
$retval = mysqli_query( $conn, $sql_insert);

$srcBg = imagecreatefrompng($background);
$im = imagecreatetruecolor(imagesx($srcBg),imagesy($srcBg));
imagecopyresampled($im, $srcBg, 0, 0, 0, 0, imagesx($srcBg), imagesy($srcBg), imagesx($srcBg), imagesy($srcBg));
for ($i = 1; $i <= 10; $i++)
{
    $bgx = 70 + ($i - 1) * 82;
    $chx = 70 + ($i - 1) * 82;
    $classx = 80 + ($i - 1) * 82;
    $starType = rand(0, 1000);
    $classType = rand(0, 7);
    $classArr=["caster","medic","pioneer","sniper","special","support","tank","warrior"];
    $classLoad=$classArr[$classType];
    if ($starType >= 0 && $starType <= 20+$probUp*20) 
    {
        $starLoad="6";
        $sixStarhasGot=1;
    } 
    elseif ($starType >= 21+$probUp*20 && $starType <= 100+$probUp*20) 
    {
        $starLoad="5";                
    } 
    elseif ($starType >= 101+$probUp*20 && $starType <= 400)
    {
        $starLoad="4";                
    } 
    elseif ($starType >= 401 && $classLoad=="special")
    {
        $starLoad="4";
    }
    else
    {
        $starLoad="3";                
    }
    $filepath=$chpath.$classLoad."/".$starLoad;
    $file_arr = [];
    $handler = opendir($filepath);
    while (($filename = readdir($handler)) !== false) 
    {
        if ($filename != "." && $filename != "..") 
        {
            array_push($file_arr, $filename);
        }
    }
    $key = array_rand($file_arr,1);
    $ch =$filepath."/".$file_arr[$key];
    $bg=$bgpath.$starLoad.".png";
    $class=$classpath.$classLoad.".png";
    $srcImage1 = imagecreatefrompng($bg);
    imagecopyresampled($im, $srcImage1, $bgx, 0, 0, 0, imagesx($srcImage1), imagesy($srcImage1), imagesx($srcImage1), imagesy($srcImage1));
    $srcImage2 = imagecreatefrompng($ch);
    imagecopyresampled($im, $srcImage2, $chx, 115, 20, 0, 120, 240, imagesx($srcImage2), imagesy($srcImage2));
    $srcImage3 = imagecreatefrompng($class);
    imagecopyresampled($im, $srcImage3, $classx, 323, 0, 0, 59, 59, imagesx($srcImage3), imagesy($srcImage3));
    $probUp=0;
}
$srcBg1 = imagecreatefrompng($background1);
imagecopyresampled($im, $srcBg1, 0, 0, 0, 0, imagesx($srcBg1), imagesy($srcBg1), imagesx($srcBg1), imagesy($srcBg1));
imagepng($im, $outPut2 . $randomname . ".png");
$url = $outPut1 . $randomname . ".png";

if($type=="png")
{
    header("Location:" . $url);;
}
elseif($type=="json")
{
    header('Content-Type:application/json; charset=utf-8');
    $arr = array('six'=>$sixStarhasGot,'url'=>$url);
    $out=str_replace("\\","",json_encode($arr));
    exit($out); 
}
elseif($type=="image")
{
    header("Content-Type:image/jpeg");
    imagepng($im,);
}
else 
{
    header("Content-Type:image/jpeg");
    imagepng($im,);//默认返回
}
//根据入参不同的返回
?>
