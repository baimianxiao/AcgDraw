<?php
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

echo(urlencode("明日方舟"));