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
$file1 = "http://www.baimianxiao.cn/api/mrfz/image/out/";//输出图片文件的位置
$file2="image/out/";
$type=$_GET['type'];
$probUp=$_GET['probup'];
//获取入参
$six=0;
$sjname = date('Ymd_H_i_s').rand(1,9999);
$srcBg = imagecreatefrompng($background);
$im = imagecreatetruecolor(imagesx($srcBg),imagesy($srcBg));
imagecopyresampled($im, $srcBg, 0, 0, 0, 0, imagesx($srcBg), imagesy($srcBg), imagesx($srcBg), imagesy($srcBg));
for ($i = 1; $i <= 10; $i++) {
    $bgx = 70 + ($i - 1) * 82;
    $chx = 70 + ($i - 1) * 82;
    $classx = 80 + ($i - 1) * 82;
    $starType = rand(0, 1000);
    $classType = rand(0, 7);
    $classArr=["caster","medic","pioneer","sniper","special","support","tank","warrior"];
    $classLoad=$classArr[$classType];
    if ($starType >= 0 && $starType <= 20+$probUp*20) {
        $starLoad="6";
        $six=1;
    } elseif ($starType >= 21+$probUp*20 && $starType <= 100+$probUp*20) {
        $starLoad="5";                
    } elseif ($starType >= 101+$probUp*20 && $starType <= 400) {
        $starLoad="4";                
    } elseif ($starType >= 401 && $classLoad=="special"){
        $starLoad="4";//特种没有三星
    } else {
        $starLoad="3";                
    }
    //随机职业路径，随机星级路径
    $filepath=$chpath.$classLoad."/".$starLoad;
    $file_arr = [];
    $handler = opendir($filepath);
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
    $probUp=0;
}
$srcBg1 = imagecreatefrompng($background1);
imagecopyresampled($im, $srcBg1, 0, 0, 0, 0, imagesx($srcBg1), imagesy($srcBg1), imagesx($srcBg1), imagesy($srcBg1));
imagepng($im, $file2 . $sjname . ".png");
$url = $file1 . $sjname . ".png";

if($type=="png"){
    header("Location:" . $url);;
}elseif($type=="json"){
    header('Content-Type:application/json; charset=utf-8');
    $arr = array('six'=>$six,'url'=>$url);
    $out=str_replace("\\","",json_encode($arr));
    exit($out); 
}elseif($type=="image"){
    header("Content-Type:image/jpeg");
    imagepng($im,);
}else {
    header("Content-Type:image/jpeg");
    imagepng($im,);
}//根据入参不同的返回
?>
