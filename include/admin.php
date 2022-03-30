<?php
//版本信息，用于更新
$_updateVersionControl = "1.0.0";
$_updateVersion = "1";

//引入设置文件,数据库操作,常用函数
include("./config.php");
include("./database.php");
include("./function.php");
include("./update.php");

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
    }elseif($mode=="table"or$mode==1){
        

    }
}

function start_update()
{
}
