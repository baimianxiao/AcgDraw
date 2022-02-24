<?php
include("./config.php");
//数据目录路径
include("./function.php");
$data_path = "..//data//";

//人物数据提取
function character_list_create()
{
    global $data_path;
    $character_table = $data_path . "character_table.json";
    if (is_file($character_table)) {
        unlink($character_table);
    }
    $json_string = file_get_contents($character_table);

    // 用参数true把JSON字符串强制转成PHP数组 
    $data = json_decode($json_string, true);
    // 遍历原文件提取需要的参数
    foreach ($data as $key => $value) {
        if ($value["itemObtainApproach"] == "招募寻访") {
            $character_data_single["name"] = $value["name"];
            $character_data_single["star"] = $value["rarity"];
            $character_data_single["class"] = $value["profession"];
            $character_data_single["tag"] = $value["tagList"];
            $character_data[$key] = $character_data_single;
            echo "{$key}==>" . $value["name"] . "<br>";
        }
    }
    $character_data_list = fopen($data_path . "character_list.json", "w");
    $character_data = json_encode($character_data, JSON_UNESCAPED_UNICODE);
    fwrite($character_data_list, $character_data);
    fclose($character_data_list);
}

function imageUrl_get($url, $name)
{
    $matches_str = '/\/[0-9a-z]+\/[0-9a-z]+\/\%E5\%8D\%8A\%E8\%BA\%AB\%E5\%83\%8F_' . addcslashes(urlencode($name), "%") . '\_1\.png' . '/';
    $image_url = preg_match_all($matches_str, $url, $matches);
    $image_url_all = "https://prts.wiki//images" . $matches[0][0];
    return $image_url_all;
}

//爬取图片url加入character_list.json




//down_file("https://githubraw.baimianxiao.cn/Kengxxiao/ArknightsGameData/master/zh_CN/gamedata/excel/character_table.json", "../data/");
if(true){
    character_list_create();
}

