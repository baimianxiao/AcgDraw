<?php
//设置文件
include("./config.php");
//数据目录路径
include("./function.php");
$data_path = "../data/";

//人物数据提取
function character_list_create($mode = 0)
{
    global $data_path;
    $character_table = $data_path . "character_table.json";
    $json_string = file_get_contents($character_table);
    // 用参数true把JSON字符串强制转成PHP数组 
    $data = json_decode($json_string, true);
    // 遍历原文件提取需要的参数
    foreach ($data as $key => $value) {
        if ($value["itemObtainApproach"] == "招募寻访") {
            $character_data_single["name"] = $value["name"];
            $character_data_single["star"] = $value["rarity"] + 1;
            $character_data_single["class"] = $value["profession"];
            $character_data_single["imageUrl"] = imageUrl_get($value["name"]);
            $character_data[$key] = $character_data_single;
            if (!file_exists($data_path . 'image/character/' . $key . '.png')) {
                down_file($character_data_single["imageUrl"], $key . '.png', $data_path . 'image/character/');
                echo ('下载');
            }
            $character_star_list = array(
                3 => array(),
                4 => array(),
                5 => array(),
                6 => array()
            );
            if ($character_data_single["star"] == 6) {
                $character_star_list[6][0] = $key;
            } elseif ($character_data_single["star"] == 5) {
            } elseif ($character_data_single["star"] == 4) {
            } elseif ($character_data_single["star"] == 3) {
            } else {
            }
        }
    }
    print_r($character_star_list);
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
    $image_url = preg_match_all($matches_str, $url, $matches);
    $image_url_all = "https://prts.wiki//images" . $matches[0][0];
    return $image_url_all;
}



//down_file("https://githubraw.baimianxiao.cn/Kengxxiao/ArknightsGameData/master/zh_CN/gamedata/excel/character_table.json","character_table.json", "../data/");
if (true) {
    character_list_create();
}
