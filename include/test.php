<?php
include("./config.php");
include("./function.php");
$version_data=curl_request( "https://prts.wiki/index.php?title=%E5%8D%A1%E6%B1%A0%E4%B8%80%E8%A7%88/%E9%99%90%E6%97%B6%E5%AF%BB%E8%AE%BF&action=edit");
//preg_match_all("/VersionControl\:([0-9\.]+)/",$version_data,$match);
preg_match_all("/wpTextbox1.*<\/textarea>/",$version_data,$match);
//preg_match_all("/[0-9\.]+\/[0-9\.]+\/[0-9\.]+/",$version_data,$match);
print_r($match);
