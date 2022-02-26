<?php
//引入设置文件,数据库操作,常用函数
include("./include/config.php");
include("./include/database.php");
include("./include/function.php");

//背景图片与遮罩图片路径
$background = "./data/image/gacha/bg.png";
$background1 = "./data/image/gacha/bg1.png";

/*
图片文件路径
bgpath为不同星级背景路径
chpath为相关人物图片路径
classpath为不同职业图标路径
*/
$backgroud_path = "./data/image/gacha/";
$character_path = "./data/image/character/";
$class_path = "./data/image/class/";

//获取人物信息
$character_file = "./data/character_list.json";
$character_list = file_get_contents($character_file);
$character_list = json_decode($character_list, true);

//获取不同星级人物列表
$star_list_file = "star_list.json";
$star_list = file_get_contents($star_list);
$star_list = json_decode($star_list, true);

$sixStarHasGot = 0;
$minimun = 0;
$srcBg = imagecreatefrompng($background);
$im = imagecreatetruecolor(imagesx($srcBg), imagesy($srcBg));
imagecopyresampled($im, $srcBg, 0, 0, 0, 0, imagesx($srcBg), imagesy($srcBg), imagesx($srcBg), imagesy($srcBg));
//绘制背景
for ($i = 1; $i <= 10; $i++) {
    $bgx = 70 + ($i - 1) * 82;
    $chx = 70 + ($i - 1) * 82;
    $classx = 80 + ($i - 1) * 82;
    $starType = rand(0, 1000);
    if ($starType >= 0 && $starType <= 20) {
        $star = 6;
        $sixStarHasGot = 1;
        $minimun = $minimun + 1;
    } elseif ($starType >= 21 && $starType <= 100) {
        $star = 5;
        $minimun = $minimun + 1;
    } elseif ($starType >= 101 && $starType <= 400) {
        $star = 4;
        $minimun = $minimun + 1;
    } else {
        $star = 3;
    }
    //强行保底4星
    if ($i = 10 and $minimun = 0) {
        $star = 4;
    }
    $character_name = array_rand($star_list[$star]);
    $ch = $character_path . $character_name . ".png";
    $bg = $backgroud_path . $star . ".png";
    $class = $class_path . $character_list[$character_name]["class"] . ".png";
    $srcImage1 = imagecreatefrompng($bg);
    imagecopyresampled($im, $srcImage1, $bgx, 0, 0, 0, imagesx($srcImage1), imagesy($srcImage1), imagesx($srcImage1), imagesy($srcImage1));
    $srcImage2 = imagecreatefrompng($ch);
    imagecopyresampled($im, $srcImage2, $chx, 115, 20, 0, 120, 240, imagesx($srcImage2), imagesy($srcImage2));
    $srcImage3 = imagecreatefrompng($class);
    imagecopyresampled($im, $srcImage3, $classx, 323, 0, 0, 59, 59, imagesx($srcImage3), imagesy($srcImage3));
}

$srcBg1 = imagecreatefrompng($background1);
imagecopyresampled($im, $srcBg1, 0, 0, 0, 0, imagesx($srcBg1), imagesy($srcBg1), imagesx($srcBg1), imagesy($srcBg1));
imagepng($im, $outPut2 . $randomname . ".png");
$url = $outPut1 . $randomname . ".png";

if ($type == "json") {
    header('Content-Type:application/json; charset=utf-8');
    $arr = array('six' => $sixStarHasGot, 'url' => $url);
    $out = str_replace("\\", "", json_encode($arr));
    exit($out);
} elseif ($type == "image") {
    header("Content-Type:image/jpeg");
    imagepng($im);
} else {
    header("Content-Type:image/jpeg");
    imagepng($im); //默认返回
}
//根据入参不同的返回
