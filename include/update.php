<?php
include("./config.php");
//数据目录路径
$data_path = "../data/";

//下载函数
function down_file($url, $folder = "./")
{
    set_time_limit(24 * 60 * 60); // 设置超时时间
    $destination_folder = $folder . '/'; // 文件下载保存目录，默认为当前文件目录
    if (!is_dir($destination_folder)) { // 判断目录是否存在
        mkdirs($destination_folder); // 如果没有就建立目录
    }
    $newfname = $destination_folder . basename($url); // 取得文件的名称
    $file = fopen($url, "rb"); // 远程下载文件，二进制模式
    if ($file) { // 如果下载成功
        $newf = fopen($newfname, "wb"); // 远在文件文件
        if ($newf) // 如果文件保存成功
            while (!feof($file)) { // 判断附件写入是否完整
                fwrite($newf, fread($file, 1024 * 8), 1024 * 8); // 没有写完就继续
            }
    }
    if ($file) {
        fclose($file); // 关闭远程文件
    }
    if ($newf) {
        fclose($newf); // 关闭本地文件
    }
    return true;
}

//建立多级目录
function mkdirs($path, $mode = "0755")
{
    if (!is_dir($path)) { // 判断目录是否存在
        mkdirs(dirname($path), $mode); // 循环建立目录
        mkdir($path, $mode); // 建立目录
    }
    return true;
}

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

function imageUrl_get($url,$name){
    $matches_str='/\/[0-9a-z]+\/[0-9a-z]+\/\%E5\%8D\%8A\%E8\%BA\%AB\%E5\%83\%8F_'.addcslashes(urlencode($name),"%").'\_1\.png'.'/';
    $image_url= preg_match_all($matches_str,$url,$matches);
    $image_url_all="https://prts.wiki//images".$matches[0][0];
    return $image_url_all;
  }
  
//爬取图片url加入character_list.json
function add_imageUrl()
{

}
$json_string = file_get_contents('../data/character_table.json');



down_file("https://githubraw.baimianxiao.cn/Kengxxiao/ArknightsGameData/master/zh_CN/gamedata/excel/character_table.json", "../data/");
