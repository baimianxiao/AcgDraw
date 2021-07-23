<?php
$beijing1 = "image/gacha/";
$shuiji2 = "bg.png";
$shuiji4 = "bg1.png";
$bggen = "image/gacha/";
$chgen = "image/photo/";
$classgen = "image/class/";
$shuiji3 = $beijing1 . "/" . $shuiji2;
$shuiji5 = $beijing1 . "/" . $shuiji4;
$file1 = "image/out/";
$sjname = date('Ymd_H_i_s').rand(1,9999);
$im = imagecreatetruecolor(960, 450);
$srcImage = imagecreatefrompng($shuiji3);
$srcImageInfo = getimagesize($shuiji3);
$imageWidth = $srcImageInfo[0];
$imageHeight = $srcImageInfo[1];
imagecopyresampled($im, $srcImage, 0, 0, 0, 0, $imageWidth, $imageHeight, imagesx($srcImage), imagesy($srcImage));

for ($i = 1; $i <= 10; $i++) {
    $bgx = 70 + ($i - 1) * 82;
    $chx = 70 + ($i - 1) * 82;
    $classx = 80 + ($i - 1) * 82;
    $xx = rand(0, 1000);
    $cc = rand(0, 8);
    switch ($cc) {
        case 1:
            $class = $classgen . "caster.png";
            $load1 = "caster/";
            if ($xx >= 0 && $xx <= 20) {
                $bg = $bggen . "6.png";
                $load2 = "6";
                $sl = 7;
            } elseif ($xx >= 21 && $xx <= 100) {
                $bg = $bggen . "5.png";
                $load2 = "5";
                $sl = 6;
            } elseif ($xx >= 101 && $xx <= 400) {
                $bg = $bggen . "4.png";
                $load2 = "4";
                $sl = 5;
            } else {
                $bg = $bggen . "3.png";
                $load2 = "3";
                $sl = 2;
            }
            break;
        case 2:
            $class = $classgen . "medic.png";
            $load1 = "medic/";
            if ($xx >= 0 && $xx <= 20) {
                $bg = $bggen . "6.png";
                $load2 = "6";
                $sl = 3;
            } elseif ($xx >= 21 && $xx <= 100) {
                $bg = $bggen . "5.png";
                $load2 = "5";
                $sl = 4;
            } elseif ($xx >= 101 && $xx <= 400) {
                $bg = $bggen . "4.png";
                $load2 = "4";
                $sl = 3;
            } else {
                $bg = $bggen . "3.png";
                $load2 = "3";
                $sl = 2;
            }
            break;

        case 3:
            if ($xx >= 0 && $xx <= 20) {
                $bg = $bggen . "6.png";
                $load2 = "6";
                $sl = 3;
            } elseif ($xx >= 21 && $xx <= 100) {
                $bg = $bggen . "5.png";
                $load2 = "5";
                $sl = 5;
            } elseif ($xx >= 101 && $xx <= 400) {
                $bg = $bggen . "4.png";
                $load2 = "4";
                $sl = 3;
            } else {
                $bg = $bggen . "3.png";
                $load2 = "3";
                $sl = 3;
            }
            $class = $classgen . "pioneer.png";
            $load1 = "pioneer/";
            break;
        case 4:
            if ($xx >= 0 && $xx <= 20) {
                $bg = $bggen . "6.png";
                $load2 = "6";
                $sl = 7;
            } elseif ($xx >= 21 && $xx <= 100) {
                $bg = $bggen . "5.png";
                $load2 = "5";
                $sl = 12;
            } elseif ($xx >= 101 && $xx <= 400) {
                $bg = $bggen . "4.png";
                $load2 = "4";
                $sl = 8;
            } else {
                $bg = $bggen . "3.png";
                $load2 = "3";
                $sl = 2;
            }
            $class = $classgen . "sniper.png";
            $load1 = "sniper/";
            break;
        case 5:
            if ($xx >= 0 && $xx <= 20) {
                $bg = $bggen . "6.png";
                $load2 = "6";
                $sl = 3;
            } elseif ($xx >= 21 && $xx <= 100) {
                $bg = $bggen . "5.png";
                $load2 = "5";
                $sl = 9;
            } else {
                $bg = $bggen . "4.png";
                $load2 = "4";
                $sl = 4;
            }
            $class = $classgen . "special.png";
            $load1 = "special/";
            break;
        case 6:
            if ($xx >= 0 && $xx <= 20) {
                $bg = $bggen . "6.png";
                $load2 = "6";
                $sl = 4;
            } elseif ($xx >= 21 && $xx <= 100) {
                $bg = $bggen . "5.png";
                $load2 = "5";
                $sl = 7;
            } elseif ($xx >= 101 && $xx <= 400) {
                $bg = $bggen . "4.png";
                $load2 = "4";
                $sl = 3;
            } else {
                $bg = $bggen . "3.png";
                $load2 = "3";
                $sl = 1;
            }
            $class = $classgen . "support.png";
            $load1 = "support/";
            break;
        case 7:
            if ($xx >= 0 && $xx <= 20) {
                $bg = $bggen . "6.png";
                $load2 = "6";
                $sl = 6;
            } elseif ($xx >= 21 && $xx <= 100) {
                $bg = $bggen . "5.png";
                $load2 = "5";
                $sl = 6;
            } elseif ($xx >= 101 && $xx <= 400) {
                $bg = $bggen . "4.png";
                $load2 = "4";
                $sl = 3;
            } else {
                $bg = $bggen . "3.png";
                $load2 = "3";
                $sl = 3;
            }
            $class = $classgen . "tank.png";
            $load1 = "tank/";
            break;
        default:
            if ($xx >= 0 && $xx <= 20) {
                $bg = $bggen . "6.png";
                $load2 = "6";
                $sl = 8;
            } elseif ($xx >= 21 && $xx <= 100) {
                $bg = $bggen . "5.png";
                $load2 = "5";
                $sl = 9;
            } elseif ($xx >= 101 && $xx <= 400) {
                $bg = $bggen . "4.png";
                $load2 = "4";
                $sl = 9;
            } else {
                $bg = $bggen . "3.png";
                $load2 = "3";
                $sl = 3;
            }
            $class = $classgen . "warrior.png";
            $load1 = "warrior/";
    }
    $load3 = $load1 . $load2;
    $sj = rand(1, $sl);
    $ch = "image/ch/" . "" . $load3 . "/" . $sj . ".png";
    $test = "image/ch/warrior/6/1.png";
    $srcImage1 = imagecreatefrompng($bg);
    $srcImageInfo1 = getimagesize($bg);
    $imageWidth1 = $srcImageInfo1[0];
    $imageHeight1 = $srcImageInfo1[1];
    imagecopyresampled($im, $srcImage1, $bgx, 0, 0, 0, $imageWidth1, $imageHeight1, imagesx($srcImage1), imagesy($srcImage1));

    $srcImage2 = imagecreatefrompng($ch);
    $srcImageInfo2 = getimagesize($ch);
    $imageWidth2 = $srcImageInfo2[0];
    $imageHeight2 = $srcImageInfo2[1];
    imagecopyresampled($im, $srcImage2, $chx, 115, 20, 0, 120, 240, imagesx($srcImage2), imagesy($srcImage2));

    $srcImage3 = imagecreatefrompng($class);
    $srcImageInfo3 = getimagesize($class);
    $imageWidth3 = $srcImageInfo3[0];
    $imageHeight3 = $srcImageInfo3[1];
    imagecopyresampled($im, $srcImage3, $classx, 323, 0, 0, 59, 59, imagesx($srcImage3), imagesy($srcImage3));
}

$srcImage = imagecreatefrompng($shuiji5);
$srcImageInfo = getimagesize($shuiji5);
$imageWidth = $srcImageInfo[0];
$imageHeight = $srcImageInfo[1];
imagecopyresampled($im, $srcImage, 0, 0, 0, 0, $imageWidth, $imageHeight, imagesx($srcImage), imagesy($srcImage));
imagepng($im, $file1 . $sjname . ".png");
$file2 = $file1 . $sjname . ".png";
$url = "http://www.baimianxiao.cn/api/mrfz/" . $file1 . $sjname . ".png";
$url = str_re($url);
header("Location:" . $url);
function str_re($str)
{
    $str = str_replace(' ', "", $str);
    $str = str_replace("\n", "", $str);
    $str = str_replace("\t", "", $str);
    $str = str_replace("\r", "", $str);
    return $str;
}
