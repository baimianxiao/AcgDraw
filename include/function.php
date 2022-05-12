<?php
//版本信息，用于更新
$_updateVersionControl = "1.0.3";
$_updateVersion = "3";

//curl爬虫
function curl_request($url, $post = [], $cookie = '',  $returnCookie = false)
{
  $curl  =  curl_init();
  curl_setopt($curl, CURLOPT_URL,  $url);
  curl_setopt($curl, CURLOPT_USERAGENT,  'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)');
  curl_setopt($curl, CURLOPT_FOLLOWLOCATION,  1);
  curl_setopt($curl, CURLOPT_AUTOREFERER,  1);
  curl_setopt($curl, CURLOPT_REFERER,  "http://XXX");
  if ($post) {
    curl_setopt($curl, CURLOPT_POST,  1);
    curl_setopt($curl, CURLOPT_POSTFIELDS,  http_build_query($post));
  }
  if ($cookie) {
    curl_setopt($curl, CURLOPT_COOKIE,  $cookie);
  }
  curl_setopt($curl, CURLOPT_HEADER,  $returnCookie);
  curl_setopt($curl, CURLOPT_TIMEOUT,  10);
  curl_setopt($curl, CURLOPT_RETURNTRANSFER,  1);
  $data  =  curl_exec($curl);
  if (curl_errno($curl)) {
    return  curl_error($curl);
  }
  curl_close($curl);
  //检查cookie
  if ($returnCookie) {
    list($header,  $body)  =  explode("\r\n\r\n",  $data,  2);
    preg_match_all("/Set\-Cookie:([^;]*);/",  $header,  $matches);
    $info['cookie']   =  substr($matches[1][0],  1);
    $info['content']  =  $body;
    return  $info;
  } else {
    return  $data;
  }
}

//下载函数
function down_file($url, $file_name, $folder = "./")
{
  set_time_limit(24 * 60 * 60); // 设置超时时间
  $destination_folder = $folder . '/'; // 文件下载保存目录，默认为当前文件目录
  if (!is_dir($destination_folder)) { // 判断目录是否存在
    mkdirs($destination_folder); // 如果没有就建立目录
  }
  $file = fopen($url, "rb"); // 远程下载文件，二进制模式
  if ($file) { // 如果下载成功
    $newf = fopen($destination_folder . $file_name, "wb"); // 远在文件文件
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

//获取ip地址
function get_ip()
{
  if (getenv('HTTP_CLIENT_IP') && strcasecmp(getenv('HTTP_CLIENT_IP'), 'unknown')) {
    $ip = getenv('HTTP_CLIENT_IP');
  } else if (getenv('HTTP_X_FORWARDED_FOR') && strcasecmp(getenv('HTTP_X_FORWARDED_FOR'), 'unknown')) {
    $ip = getenv('HTTP_X_FORWARDED_FOR');
  } else if (getenv('REMOTE_ADDR') && strcasecmp(getenv('REMOTE_ADDR'), 'unknown')) {
    $ip = getenv('REMOTE_ADDR');
  } else if (isset($_SERVER['REMOTE_ADDR']) && $_SERVER['REMOTE_ADDR'] && strcasecmp($_SERVER['REMOTE_ADDR'], 'unknown')) {
    $ip = $_SERVER['REMOTE_ADDR'];
  }
  return  preg_match('/[\d\.]{7,15}/', $ip, $matches) ? $matches[0] : '';
}

//
function table_change($array, $vableToChange = "", $mode = 0)
{
  if ($mode == 0) {
    foreach ($array as $key => $vable) {
      $newKey = $array[$key];
      $newArray[$newKey] = $key;
    }
  } elseif ($mode == 1) {
    if ($vableToChange == "") {
      return false;
    }
    foreach ($array as $key => $vable) {
      $newKey = $vable[$vableToChange];
      $newArray[$newKey] = $key;
    }
  }
  return $newArray;
}

function get_json_file($file){
    $fileConnect = file_get_contents($file);
    if($fileConnect==null)
    {
        throw new Exception("get_json_file() not find file");
    }
    $jsonData = json_decode($fileConnect, true);
    return $jsonData;
}

function json_write($jsonData,$jsonPath){
  $jsonPath = fopen($jsonPath, "w");
  $jsonData = json_encode($jsonData, JSON_UNESCAPED_UNICODE);
  fwrite($jsonPath, $jsonData);
  fclose($jsonPath);
}
