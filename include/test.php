<?php
include("./config.php");
include("./function.php");
echo($version_data=curl_request( $update_address. "/Kengxxiao/ArknightsGameData/master/zh_CN/gamedata/excel/data_version.txt"));
//preg_match_all("/VersionControl\:([0-9\.]+)/",$version_data,$match);
preg_match_all("/Change:([0-9]+)/",$version_data,$match);
//preg_match_all("/[0-9\.]+\/[0-9\.]+\/[0-9\.]+/",$version_data,$match);
print_r($match);