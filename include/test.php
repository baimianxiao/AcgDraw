<?php
//版本信息，用于更新
$_updateVersionControl = "1.0.0";
$_updateVersion = "1";

include("./config.php");
include("./function.php");

echo "<pre>";
$table_data = get_table_data("https://prts.wiki/index.php?title=%E5%8D%A1%E6%B1%A0%E4%B8%80%E8%A7%88/%E9%99%90%E6%97%B6%E5%AF%BB%E8%AE%BF&action=edit", 1);
print_r(manage_table_data($table_data));
echo "<pre>";
//获取
function get_table_data($url, $mode = 0)
{
  $table_data_html = curl_request($url);
  //爬取卡池数据
  preg_match_all("/wpTextbox1\">[\s\S]*textarea>/", $table_data_html, $match);
  $textarea = $match[0][0];
  //处理卡池数据
  if ($mode == 0) {
    preg_match_all("/==非标准寻访==[\s\S]*==标准寻访==/", $textarea, $match);
    $tableDataText = str_replace("==标准寻访==", "", str_replace("==非标准寻访==", "", $match[0][0]));
    $tableData = explode("|-", $tableDataText);
  } elseif ($mode == 1) {
    preg_match_all("/==标准寻访==[\s\S]*/", $textarea, $match);
    $tableDataText = str_replace("==标准寻访==", "", str_replace("</textarea>", "", $match[0][0]));
    $tableData = explode("|-", $tableDataText);
  } else {
    return false;
  }
  return $tableData;
}

function manage_table_data($tableData)
{
  foreach ($tableData as $key => $value) {
    preg_match_all("/link=[\s\S]*?\/([\s\S]*?)]/", $value, $match);
    if ($match[1][0] == "" or $match[1][0] == null) {
      //如果ID为空跳出循环
      continue;
    }
    $tableID= $match[1][0];
    preg_match_all("/\[\[[\s\S]*?\|([\s\S]*?)\]\]/", $value, $match);
    $table_data_single["name"] = $match[1][1];
    preg_match_all("/[\s\S]*/", $value, $match);
    $characterData = $match[0][0];
    preg_match_all("/\d*-\d*-[\s\S]*?:\d*/", $value, $match);
    $table_data_single["time"]=$match[0];
    preg_match_all("/{{[\s\S]*?}}/", $characterData, $match);
    $characterList = $match[0];
    //对匹配出的人物信息字符串进行遍历处理
    foreach ($characterList as $key => $value) {
      //判断是否为限定
      if (strstr($value, "limited=1") != false) {
        preg_match_all("/\|([\s\S]*)\|/", $value, $match);
        $characterName = $match[1][0];
        $characterList[$key] = array(
          "name" => $characterName,
          "limited" => "1"
        );
      } else {
        preg_match_all("/\|([\s\S]*)}}/", $value, $match);
        $characterName = $match[1][0];
        $characterList[$key] = array(
          "name" => $characterName,
          "limited" => "0"
        );
      }
      $table_data_single["star6_up"] =  $characterList;
    }
    $tableddata[$tableID] = $table_data_single;
  }
  return $tableddata;
}
