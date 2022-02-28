<?php
//设置文件
include("./config.php");

include("./function.php");
//数据目录路径
$data_path = "../data/";

//获取更新文件版本
function get_update_version($mode=0){
    global $update_address;
    echo($version_data=curl_request( $update_address. "/Kengxxiao/ArknightsGameData/master/zh_CN/gamedata/excel/data_version.txt"));
    preg_match_all("/VersionControl\:([0-9\.]+)/",$version_data,$match);
    $version_control=$match[1][0];
    preg_match_all("/Change:([0-9]+)/",$version_data,$match);
    $version=$match[0][0];
    preg_match_all("/[0-9\.]+\/[0-9\.]+\/[0-9\.]+/",$version_data,$match);
    $update_date=$match[1][0];

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
            if (!array_key_exists("imageUrl", $character_list[$key])) {
                $character_data_single["imageUrl"] = imageUrl_get($value["name"]);
                echo ("爬取{$key}</br>");
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
    $image_url_all = "https://prts.wiki//images" . $matches[0][0];
    return $image_url_all;
}



//down_file("https://githubraw.baimianxiao.cn/Kengxxiao/ArknightsGameData/master/zh_CN/gamedata/excel/character_table.json","character_table.json", "../data/");
if (true) {
    character_list_create();
}
