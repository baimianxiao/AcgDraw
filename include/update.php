<?php
//版本信息，用于更新
$_updateVersionControl = "1.0.10";
$_updateVersion = "10";

//设置文件
include("./config.php");
include("./function.php");
//数据目录路径
$data_path = "../data/";

//获取更新文件版本
function get_update_version($mode = 0)
{
  global $updateAddress, $data_path;
  $version_data = curl_request($updateAddress . "/Kengxxiao/ArknightsGameData/master/zh_CN/gamedata/excel/data_version.txt");
  preg_match_all("/VersionControl\:([0-9\.]+)/", $version_data, $match);
  $characterTableVersion['control'] = $match[1][0];
  preg_match_all("/Change:([0-9]+)/", $version_data, $match);
  $characterTableVersion['id'] = $match[1][0];
  preg_match_all("/[0-9]+\/[0-9]+\/[0-9]+/", $version_data, $match);
  $characterTableVersion['date'] = $match[0][0];
  if ($mode == 0) {
    return $characterTableVersion;
  } elseif ($mode == 1) {

    $updateVersion = fopen($data_path . "update_version.json", "w");
    $characterTableVersion = json_encode($characterTableVersion, JSON_UNESCAPED_UNICODE);
    fwrite($updateVersion, $characterTableVersion);
    fclose($updateVersion);
    return true;
  } else {
    return false;
  }
}

//人物数据提取
function character_list_create($mode = 0)
{
  global $data_path;
  $character_file = $data_path . "character_table.json";
  $character_table = file_get_contents($character_file);
  $character_table = json_decode($character_table, true);

  $list_file = $data_path . "character_list.json";
  //
  if (file_exists($list_file)) {
    $character_list = file_get_contents($list_file);
    $character_list = json_decode($character_list, true);
  } else {
    $character_list = array();
  }
  //初始化全局人物数组
  $character_star_list = array(
    3 => array(),
    4 => array(),
    5 => array(),
    6 => array()
  );
  // 遍历原文件提取需要的参数
  foreach ($character_table as $key => $value) {
    if ($value["itemObtainApproach"] == "招募寻访") {
      $character_data_single["name"] = $value["name"];
      $character_data_single["star"] = $value["rarity"] + 1;
      $character_data_single["class"] = $value["profession"];
      if ($character_list[$key]["imageUrl"] == "" or $character_list[$key]["imageUrl"] == null) {
        //wiki未更新图片时跳过该角色
        if (imageUrl_get($value["name"]) == false) {
          continue;
        } else {
          $character_data_single["imageUrl"] = imageUrl_get($value["name"]);
          echo ("爬取{$key}</br>");
        }
      } else {
        //防止imagUrl存在时被空参数覆盖
        $character_data_single["imageUrl"] = $character_list[$key]["imageUrl"];
      }
      $character_data[$key] = $character_data_single;
      if (!file_exists($data_path . 'image/character/' . $key . '.png')) {
        down_file($character_data_single["imageUrl"], $key . '.png', $data_path . 'image/character/');
        echo ("下载{$key}.png</br>");
      }
      //根据星级分类
      if ($character_data_single["star"] == 6) {
        $character_star_list[6][count((array)$character_star_list[6])] = $key;
      } elseif ($character_data_single["star"] == 5) {
        $character_star_list[5][count((array)$character_star_list[5])] = $key;
      } elseif ($character_data_single["star"] == 4) {
        $character_star_list[4][count((array)$character_star_list[4])] = $key;
      } elseif ($character_data_single["star"] == 3) {
        $character_star_list[3][count((array)$character_star_list[3])] = $key;
      } else {
        $character_star_list[0][count((array)$character_star_list[0])] = $key;
      }
    }
  }
  //保存全局人物信息
  $character_star = fopen($data_path . "star_list.json", "w");
  $character_star_list = json_encode($character_star_list, JSON_UNESCAPED_UNICODE);
  fwrite($character_star, $character_star_list);
  fclose($character_star);
  //保存单个人物信息
  $character_data_list = fopen($data_path . "character_list.json", "w");
  $character_data = json_encode($character_data, JSON_UNESCAPED_UNICODE);
  fwrite($character_data_list, $character_data);
  fclose($character_data_list);
}

//爬取图片url加入character_list.json
function imageUrl_get($name)
{
  $url = curl_request("https://prts.wiki/w/PRTS:%E6%96%87%E4%BB%B6%E4%B8%80%E8%A7%88/%E5%B9%B2%E5%91%98%E7%B2%BE%E8%8B%B10%E5%8D%8A%E8%BA%AB%E5%83%8F");
  $matches_str = '/\/[0-9a-z]+\/[0-9a-z]+\/\%E5\%8D\%8A\%E8\%BA\%AB\%E5\%83\%8F_' . addcslashes(urlencode($name), "%") . '\_1\.png' . '/';
  preg_match_all($matches_str, $url, $matches);
  if ($matches == null or $matches == "") {
    return false;
  } else {
    $image_url_all = "https://prts.wiki//images" . $matches[0][0];
    return $image_url_all;
  }
}

//获取本地版本信息
function get_local_version()
{
  global $data_path;
  $localFileVersion = $data_path . "update_version.json";
  $localFileVersion = file_get_contents($localFileVersion);
  $localFileVersion = json_decode($localFileVersion, true);
  return $localFileVersion;
}

function character_change()
{
  global $data_path;
  $character_file = $data_path . "character_list.json";
  $character_table = file_get_contents($character_file);
  $characterList = json_decode($character_table, true);
  $characterNameList = table_change($characterList, "name", 1);
  $character_data_list = fopen($data_path . "character_name_list.json", "w");
  $character_data = json_encode($characterNameList, JSON_UNESCAPED_UNICODE);
  fwrite($character_data_list, $character_data);
  fclose($character_data_list);
  return true;
}
//down_file("https://githubraw.baimianxiao.cn/Kengxxiao/ArknightsGameData/master/zh_CN/gamedata/excel/character_table.json","character_table.json", "../data/");

//character_list_create();
function update_table()
{
  global $data_path;
  $table_data_1 = get_table_data("https://prts.wiki/index.php?title=%E5%8D%A1%E6%B1%A0%E4%B8%80%E8%A7%88/%E9%99%90%E6%97%B6%E5%AF%BB%E8%AE%BF&action=edit", 0);
  $table_data_2 = get_table_data("https://prts.wiki/index.php?title=%E5%8D%A1%E6%B1%A0%E4%B8%80%E8%A7%88/%E9%99%90%E6%97%B6%E5%AF%BB%E8%AE%BF&action=edit", 1);
  $table_data_1 = manage_table_data($table_data_1);
  $table_data_2 = manage_table_data($table_data_2, 1);
  $table_data = array_merge($table_data_1, $table_data_2);
  print_r($table_data);
  json_write($table_data, $data_path . "table_data.json");
}

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

function manage_table_data($tableData, $table = 0, $mode = 0)
{
  global $data_path;
  $characterDataList = get_json_file($data_path . "character_name_list.json");
  $characterTableList = get_json_file($data_path . "character_list.json");
  $characterStarList = get_json_file($data_path . 'star_list.json');
  $characterStar6List = $characterStarList["6"];
  $characterStar5List = $characterStarList["5"];
  $characterLimited6 = array();
  $characterLimited5 = array();
  foreach ($tableData as $key => $value) {
    if ($table == 0) {
      preg_match_all("/link=([\s\S]*?)]]/", $value, $match);
    } else {
      preg_match_all("/link=[\s\S]*?\/([\s\S]*?)]/", $value, $match);
    }
    if ($match[1][0] == "" or $match[1][0] == null) {
      //如果ID为空跳出循环
      continue;
    }
    $tableID = $match[1][0];
    preg_match_all("/\[\[[\s\S]*?\|([\s\S]*?)\]\]/", $value, $match);
    $tableDataSingle["name"] = $match[1][1];
    preg_match_all("/[\s\S]*/", $value, $match);
    $characterData = $match[0][0];
    preg_match_all("/\d*-\d*-[\s\S]*?:\d*/", $value, $match);
    $tableDataSingle["time"] = $match[0];
    preg_match_all("/{{[\s\S]*?}}/", $characterData, $match);
    $characterList = $match[0];
    $upDataStar6 = array();
    $upDataStar5 = array();
    $upDataStar4 = array();
    //对匹配出的人物信息字符串进行遍历处理
    foreach ($characterList as $key => $value) {
      //判断是否为限定
      if (strstr($value, "limited=1") == true) {
        $tableDataSingle['limited'] = 1;
        preg_match_all("/\|([\s\S]*)\|/", $value, $match);
      } else {
        $tableDataSingle['limited'] = 0;
        preg_match_all("/\|([\s\S]*)\}\}/", $value, $match);
      }

      $characterName = $match[1][0];

      $characterStar = $characterTableList[$characterDataList[$characterName]]["star"];
      if ($characterStar == 6) {
        array_push($upDataStar6, $characterName);
        if ($tableDataSingle['limited'] == 1) {
          $characterKey = $characterTableList[$characterDataList[$characterName]];
          array_push($characterLimited6, $characterKey);
        }
      } elseif ($characterStar == 5) {
        array_push($upDataStar5, $characterName);
        if ($tableDataSingle['limited'] == 1) {
          $characterKey = $characterTableList[$characterDataList[$characterName]];
          array_push($characterLimited5, $characterKey);
        }
      } else {
        array_push($upDataStar4, $characterName);
      }
    }
    $tableDataSingle["star6_up"] = $upDataStar6;
    $tableDataSingle['star5_up'] = $upDataStar5;
    $tableDataSingle['star4_up'] = $upDataStar4;
    $tableDataList[$tableID] = $tableDataSingle;
  }
  $characterStar6List = array_diff($characterStar6List, $characterLimited6);
  $characterStar5List = array_diff($characterStar5List, $characterLimited5);
  $characterStarList["6"] = $characterStar6List;
  $characterStarList["5"] = $characterStar5List;
  json_write($characterStarList, $data_path . "star_list.json");
  return $tableDataList;
}
