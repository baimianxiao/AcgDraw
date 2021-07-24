<?php
$background = "image/gacha/bg.png";
$background1 = "image/gacha/bg1.png";//背景图片与遮罩图片路径

$bgpath = "image/gacha/";
$chpath = "image/ch/";
$classpath = "image/class/";
/*
图片文件路径
bgpath为不同星级背景路径
chpath为相关人物图片路径
classpath为不同职业图标路径
*/
$utl1="http://www.baimianxiao.cn/api/mrfz/";//api.php文件的位置

$file1 = "image/out/";//输出图片的文件夹

$sjname = date('Ymd_H_i_s').rand(1,9999);//使用时间和随机数组成文件名

$srcBg = imagecreatefrompng($background);
$im = imagecreatetruecolor(imagesx($srcBg),imagesy($srcBg));//以背景图片的大小创建画布
imagecopyresampled($im, $srcBg, 0, 0, 0, 0, imagesx($srcBg), imagesy($srcBg), imagesx($srcBg), imagesy($srcBg));


for ($i = 1; $i <= 10; $i++) {
    $bgx = 70 + ($i - 1) * 82;
    $chx = 70 + ($i - 1) * 82;
    $classx = 80 + ($i - 1) * 82;
   
    $starType = rand(0, 1000);
    $classType = rand(1, 8);
    switch ($classType)
    {
        case 1:
            $classLoad="caster";
            break;
        case 2:
            $classLoad="medic";
            break;
        case 3:
            $classLoad="pioneer";
            break;
        case 4:
            $classLoad="sniper";
            break;
        case 5:
            $classLoad="special";
            break;
        case 6:
            $classLoad="support";
            break;
        case 7:
            $classLoad="tank";
            break;
        default:$classLoad="warrior";
        
    }
    if ($starType >= 0 && $starType <= 20) {
        $starLoad="6";
    } elseif ($starType >= 21 && $starType <= 100) {
        $starLoad="5";                
    } elseif ($starType >= 101 && $starType <= 400) {
        $starLoad="4";                
    } elseif ($starType >= 401 && $classLoad=="special"){
        $starLoad="4";//由于特种没有
    } else {
        $starLoad="3";                
    }
    //随机职业路径，随机星级路径
    $filepath=$chpath.$classLoad."/".$starLoad;//合成目标目录路径
    $file_arr = [];//存放目标文件名
    $handler = opendir($filepath);//当前目录中的文件夹下的文件夹
    while (($filename = readdir($handler)) !== false) {
        if ($filename != "." && $filename != "..") {
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
}
$srcBg1 = imagecreatefrompng($background1);
imagecopyresampled($im, $srcBg1, 0, 0, 0, 0, imagesx($srcBg1), imagesy($srcBg1), imagesx($srcBg1), imagesy($srcBg1));
imagepng($im, $file1 . $sjname . ".png");//导出图片
$url = $url1. $file1 . $sjname . ".png";
header("Location:" . $url);//重定向到图片
?>