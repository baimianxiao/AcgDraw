<?php
//版本信息，用于更新
$_updateVersionControl = "1.0.0";
$_updateVersion = "1";

include("./config.php");
include("./function.php");
$table_data_html = curl_request("https://prts.wiki/index.php?title=%E5%8D%A1%E6%B1%A0%E4%B8%80%E8%A7%88/%E9%99%90%E6%97%B6%E5%AF%BB%E8%AE%BF&action=edit");
preg_match_all("/wpTextbox1\">[\s\S]*textarea>/", $table_data_html, $match);
$textarea = $match[0][0];
preg_match_all("/==非标准寻访==[\s\S]*==标准寻访==/", $textarea, $match);
$table_data_text_1 = str_replace("==标准寻访==", "", str_replace("==非标准寻访==", "", $match[0][0]));
//print_r($match[0][0]);
preg_match_all("/==标准寻访==[\s\S]*/", $textarea, $match);
$table_data_text_2 = str_replace("==标准寻访==", "", str_replace("</textarea>", "", $match[0][0]));
$table_data_array_1 = explode("|-", $table_data_text_1);
$table_data_array_2 = explode("|-", $table_data_text_2);


foreach ($table_data_array_1 as $key => $value) {
  preg_match_all("/link=[\s\S]*?]/", $value, $match);
  $table_data_single["id"] = str_replace("]", "", str_replace("link=", "", $match[0][0]));
  preg_match_all("/\[\[[\s\S]*?\]\]/", $value, $match);
  $table_data_single["name"] = str_replace("]]", "", str_replace("[[", "", $match[0][1]));
  preg_match_all("/[\s\S]*/", $value, $match);
  $characterData = $match[0][0];
  preg_match_all("/{{[\s\S]*?}}/", $characterData, $match);
  $characterList = $match[0];
  $table_data_single["star6_up"] =  $characterList;
  foreach ($characterList as $key => $value) {
    //判断是否为限定
    if (strstr($value, "limited=1") != false) {
      preg_match_all("/\|[\s\S]*\|/", $value, $match);
      $characterName = str_replace("|", "", $match[0][0]);
      $characterList[$key] = array(
        "name" => $characterName,
        "limited" => "1"
      );
    } else {
      preg_match_all("/\|[\s\S]*}}/", $value, $match);
      $characterName = str_replace("}}", "", str_replace("|", "", $match[0][0]));
      $characterList[$key] = array(
        "name" => $characterName,
        "limited" => "0"
      );
    }
  }
  $table_data_single["star6_up"] =  $characterList;
  echo "<pre>";
  print_r($table_data_single);
  echo "<pre>";
}

echo "<pre>";
print_r($table_data_array_1);
print_r($table_data_array_2);
echo "<pre>";
function get_table_data()
{
  //
  $table_data_html = curl_request("https://prts.wiki/index.php?title=%E5%8D%A1%E6%B1%A0%E4%B8%80%E8%A7%88/%E9%99%90%E6%97%B6%E5%AF%BB%E8%AE%BF&action=edit");
  //
  preg_match_all("/wpTextbox1\">[\s\S]*textarea>/", $table_data_html, $match);
  $textarea = $match[0][0];
  preg_match_all("/==非标准寻访==[\s\S]*==标准寻访==/", $textarea, $match);
  $table_data_text_1 = str_replace("==标准寻访==", "", str_replace("==非标准寻访==", "", $match[0][0]));
  //print_r($match[0][0]);
  preg_match_all("/==标准寻访==[\s\S]*/", $textarea, $match);
  $table_data_text_2 = str_replace("==标准寻访==", "", str_replace("</textarea>", "", $match[0][0]));
  $table_data_array_1 = explode("|-", $table_data_text_1);
  $table_data_array_2 = explode("|-", $table_data_text_2);
  foreach ($table_data_array_1 as $key => $value) {
    preg_match_all("/link=[\s\S]*?]/", $value, $match);
    $table_data_single["id"] = str_replace("]", "", str_replace("link=", "", $match[0][0]));
    preg_match_all("/\[\[[\s\S]*?\]\]/", $value, $match);
    $table_data_single["name"] = str_replace("]]", "", str_replace("[[", "", $match[0][1]));
    preg_match_all("/[\s\S]*/", $value, $match);
    $characterData = $match[0][0];
    preg_match_all("/{{[\s\S]*?}}/", $characterData, $match);
    $characterList = $match[0];
    $table_data_single["star6_up"] =  $characterList;
    //对匹配出的人物信息字符串进行遍历处理
    foreach ($characterList as $key => $value) {
      //判断是否为限定
      if (strstr($value, "limited=1") != false) {
        preg_match_all("/\|[\s\S]*\|/", $value, $match);
        $characterName = str_replace("|", "", $match[0][0]);
        $characterList[$key] = array(
          "name" => $characterName,
          "limited" => "1"
        );
      } else {
        preg_match_all("/\|[\s\S]*}}/", $value, $match);
        $characterName = str_replace("}}", "", str_replace("|", "", $match[0][0]));
        $characterList[$key] = array(
          "name" => $characterName,
          "limited" => "0"
        );
      }
    }
    $table_data_single["star6_up"] =  $characterList;
    return $table_data_single;

  }
}
