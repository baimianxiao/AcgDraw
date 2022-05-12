<?php
//版本信息，用于更新
$_updateVersionControl = "1.0.2";
$_updateVersion = "2";

//API根目录url
$rootUrl="http://test.baimianxiao.cn/arknights/arknightsdraw/";
 
//数据库设置
$mysqliSwitch=1; //是否使用数据库
$mysqliHost="localhost";
$mysqliUser="user_name";
$mysqliPassword="password";
$mysqliName="mysql_name";

/*
文件更新使用的网站
1.https://githubraw.baimianxiao.cn/（镜像站，国内可用）
2.https://raw.githubusercontent.com/（原站，国内需要vpn）
默认使用
*/
$updateAddress="https://githubraw.baimianxiao.cn/";

//定时清理缓存间隔,单位：秒
$cleartime=6000;