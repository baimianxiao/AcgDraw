<?php
//引入设置文件,数据库操作,常用函数
include("./include/config.php");
include("./include/function.php");

//判断请求类型
if ($_SERVER['REQUEST_METHOD'] == 'GET') {
    $drawMode = $_GET["drawMode"];
    $backMode = $_GET["backMode"];
    $tableName = $_GET["tableName"];
    if ($_GET["probabilityUp"] == null) {
        $probabilityUp = 0;
    } else {
        $probabilityUp = $_GET["probabilityUp"];
    }
} elseif ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $drawMode = $_POST["drawMode"];
    $backMode = $_POST["backMode"];
    $tableName = $_POST["tableName"];
    if ($_POST["probabilityUp"] == null) {
        $probabilityUp = 0;
    } else {
        $probabilityUp = $_POST["probabilityUp"];
    }
}

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
$star_list_file = "./data/star_list.json";
$star_list = file_get_contents($star_list_file);
$star_list = json_decode($star_list, true);

//读取卡池文件
$characterTableList = get_json_file("./data/table_data.json");

$characterName = get_json_file("./data/character_name_list.json");

$sixStarHasGot = 0;
$minimun = 0;
$expect = 0;

//判断传入的卡池名是否存在，否则随机卡池
if (isset($characterTableList[$tableName]) == false) {
    $tableName = array_rand($characterTableList);
}

$tableData = $characterTableList[$tableName];
$tableNameAll = $tableData["name"];
$star6UP = $tableData["star6_up"];
$star5UP = $tableData["star5_up"];

$srcBg = imagecreatefrompng($background);
$im = imagecreatetruecolor(imagesx($srcBg), imagesy($srcBg));
imagecopyresampled($im, $srcBg, 0, 0, 0, 0, imagesx($srcBg), imagesy($srcBg), imagesx($srcBg), imagesy($srcBg));

for ($i = 1; $i <= 10; $i++) {
    $bgx = 70 + ($i - 1) * 82;
    $chx = 70 + ($i - 1) * 82;
    $classx = 80 + ($i - 1) * 82;
    $starType = rand(0, 1000);
    $up = rand(0, 100);
    if ($starType >= 0 && $starType <= 20 + $probabilityUp) {
        if ($up <= 50) {
            $character = $star6UP[array_rand($star6UP)];
            $characterKey = $characterName[$character];
        } else {
            $characterKey = $star_list[6][array_rand($star_list[6])];
            $ex = 1;
        }
        $star = 6;
        $sixStarHasGot = 1;
        $minimun = $minimun + 1;
    } elseif ($starType >= 21 + $probabilityUp && $starType <= 100 + $probabilityUp) {
        if ($up <= 50) {
            $character = $star5UP[array_rand($star5UP)];
            $characterKey = $characterName[$character];
        } else {
            $characterKey = $star_list[5][array_rand($star_list[5])];
        }
        $star = 5;
        $minimun = $minimun + 1;
    } elseif ($starType >= 101 && $starType <= 400) {
        $characterKey = $star_list[4][array_rand($star_list[4])];
        $minimun = $minimun + 1;
        $star = 4;
    } else {
        $characterKey = $star_list[3][array_rand($star_list[3])];
        $star = 3;
    }
    //强行保底4星
    if ($i == 10 and $minimun = 0) {
        $characterKey = $star_list[4][array_rand($star_list[4])];
        $star = 4;
    }

    $ch = $character_path . $characterKey . ".png";
    $bg = $backgroud_path . $star . ".png";
    $class = $class_path . $character_list[$characterKey]["class"] . ".png";
    $srcImage1 = imagecreatefrompng($bg);
    imagecopyresampled($im, $srcImage1, $bgx, 0, 0, 0, imagesx($srcImage1), imagesy($srcImage1), imagesx($srcImage1), imagesy($srcImage1));
    $srcImage2 = imagecreatefrompng($ch);
    imagecopyresampled($im, $srcImage2, $chx, 115, 20, 0, 120, 240, imagesx($srcImage2), imagesy($srcImage2));
    $srcImage3 = imagecreatefrompng($class);
    imagecopyresampled($im, $srcImage3, $classx, 323, 0, 0, 59, 59, imagesx($srcImage3), imagesy($srcImage3));
}

$srcBg1 = imagecreatefrompng($background1);
imagecopyresampled($im, $srcBg1, 0, 0, 0, 0, imagesx($srcBg1), imagesy($srcBg1), imagesx($srcBg1), imagesy($srcBg1));

function getrandstr($length)
{
    $str = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890';
    $randStr = str_shuffle($str); //打乱字符串
    $rands = substr($randStr, 0, $length); //substr(string,start,length);返回字符串的一部分
    return $rands;
}
//返回信息
if ($backMode == "image") {
    header("Content-Type:image/png");
    imagepng($im);
} elseif ($backMode == "json") {
    header("Content-Type:application/json");
    $imageName = getrandstr(7) . ".png";
    imagepng($im, "./data/image/out/" . $imageName);
    $imageUrl = $rootUrl . "data/image/out/" . $imageName;
    $return_data = array(
        "sixStarHasGot" => $sixStarHasGot,
        "expect" => $expect,
        "tableName" => $tableNameAll,
        "imageUrl" => $imageUrl,
        "test" => $tableData
    );
    echo (json_encode($return_data, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES));
} else {
    header("Content-Type:image/png");
    imagepng($im);
}
