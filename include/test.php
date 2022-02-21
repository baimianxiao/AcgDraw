<?php
$data_path="../data/";
$json_string = file_get_contents($data_path."character_table.json");

// 用参数true把JSON字符串强制转成PHP数组 
$data = json_decode($json_string, true);
foreach ($data as $key => $value) {
  if ($value["itemObtainApproach"]=="招募寻访") {
    $character_data_single["name"] = $value["name"];
    $character_data_single["star"] = $value["rarity"];
    $character_data_single["class"] = $value["profession"];
    $character_data[$key] = $character_data_single;
    echo "{$key}==>" . $value["name"] . "<br>";
  }
}
$character_data_list = fopen($data_path."character_list.json", "w");
$character_data=json_encode($character_data,JSON_UNESCAPED_UNICODE);
fwrite($character_data_list,$character_data);
fclose($character_data_list);
echo $character_data;
