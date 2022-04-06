<?php
//版本信息，用于更新
$_updateVersionControl = "1.0.0";
$_updateVersion = "1";

//引入设置文件,数据库操作,常用函数
//include("./database.php");
include("./update.php");

$mode = $_POST['mode'];
$data = $_POST['data'];

function need_update($mode = 0)
{
    if ($mode == "character" or $mode == 0) {
        $cloudVersionId = get_update_version(0);
        $cloudVersionId = $cloudVersionId['id'];
        $localVersionId = get_local_version();
        $localVersionId = $localVersionId['id'];
        if ($localVersionId >= $cloudVersionId) {
            $versionId['need'] = false;
        } else {
            $versionId['need'] = true;
        }
        $versionId['cloud'] = $cloudVersionId;
        $versionId['local'] = $localVersionId;
        return $versionId;
    }
    //elseif ($mode == "table" or $mode == 1) {
    //}
}

function start_update()
{
    down_file("https://githubraw.baimianxiao.cn/Kengxxiao/ArknightsGameData/master/zh_CN/gamedata/excel/character_table.json", "character_table.json", "../data/");
    character_list_create();
    character_change();
    $table_data = get_table_data("https://prts.wiki/index.php?title=%E5%8D%A1%E6%B1%A0%E4%B8%80%E8%A7%88/%E9%99%90%E6%97%B6%E5%AF%BB%E8%AE%BF&action=edit", 0);
    print_r(manage_table_data($table_data));
  get_update_version(1);
 return true;
    
}

function api_success($data, $msg = "操作成功", $code = 200, $redirect_url = '')
{
    header('Content-Type:application/json'); //加上这行,前端那边就不需要var result = $.parseJSON(data);
    $ret = ["code" => $code, "msg" => $msg, "data" => $data, 'redirect_url' => $redirect_url];
    return json_encode($ret, JSON_UNESCAPED_UNICODE);
}

if($mode=="get_version"){
    echo (api_success(need_update(0)));
}elseif($mode=="update"){
    echo(api_success(start_update()));
}

