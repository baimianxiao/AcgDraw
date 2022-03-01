<?php
include("./config.php");
include("./function.php");
$table_data_html = curl_request("https://prts.wiki/index.php?title=%E5%8D%A1%E6%B1%A0%E4%B8%80%E8%A7%88/%E9%99%90%E6%97%B6%E5%AF%BB%E8%AE%BF&action=edit");
preg_match_all("/wpTextbox1\">[\s\S]*textarea>/", $table_data_html, $match);
$textarea = $match[0][0];
preg_match_all("/==非标准寻访==[\s\S]*==标准寻访==/", $textarea, $match);
$table_data_text_1 = str_replace("==标准寻访==", "", str_replace("==非标准寻访==", "", $match[0][0]));
//print_r($match[0][0]);
preg_match_all("/==标准寻访==[\s\S]*/", $textarea, $match);
$table_data_text_2=str_replace("==标准寻访==", "", str_replace("</textarea>", "", $match[0][0]));
echo "<pre>";
print_r(explode("|-", $table_data_text_1));
print_r(explode("|-", $table_data_text_2));
echo "<pre>";
