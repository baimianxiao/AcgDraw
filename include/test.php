<?php
$data_path = "../data/";
$json_string = file_get_contents($data_path . "character_table.json");

// 用参数true把JSON字符串强制转成PHP数组 
/*$data = json_decode($json_string, true);
foreach ($data as $key => $value) {
  if ($value["itemObtainApproach"] == "招募寻访") {
    $character_data_single["name"] = $value["name"];
    $character_data_single["star"] = $value["rarity"];
    $character_data_single["class"] = $value["profession"];
    $character_data[$key] = $character_data_single;
    echo "{$key}==>" . $value["name"] . "<br>";
  }
}
$character_data_list = fopen($data_path . "character_list.json", "w");
$character_data = json_encode($character_data, JSON_UNESCAPED_UNICODE);
fwrite($character_data_list, $character_data);
fclose($character_data_list);
echo $character_data;*/

/*
 def get_url(name):
    url = "https://prts.wiki/w/PRTS:%E6%96%87%E4%BB%B6%E4%B8%80%E8%A7%88/%E5%B9%B2%E5%91%98%E7%B2%BE%E8%8B%B10%E5%8D%8A%E8%BA%AB%E5%83%8F "
    request = urllib.request.Request(url)
    # 模拟Mozilla浏览器进行爬虫
    request.add_header("user-agent", "Mozilla/5.0")
    response2 = urllib.request.urlopen(request)
    html_str = str(response2.read(), encoding="utf-8")
    pic_url = re.findall(
        r'/images/thumb/[0-9a-z]+/[0-9a-z]+/%E5%8D%8A%E8%BA%AB%E5%83%8F_' + urllib.parse.quote(name) + '_1.png',
        html_str, re.I)
    return url_change(pic_url[0], name)


def url_change(url, name):
    url_data = re.findall(r'/[0-9a-z]+/[0-9a-z]+/%E5%8D%8A%E8%BA%AB%E5%83%8F_' + urllib.parse.quote(name) + '_1.png',
                          url, re.I)
    return "https://prts.wiki//images" + url_data[0]
 */
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
$html=curl_request("https://prts.wiki/w/PRTS:%E6%96%87%E4%BB%B6%E4%B8%80%E8%A7%88/%E5%B9%B2%E5%91%98%E7%B2%BE%E8%8B%B10%E5%8D%8A%E8%BA%AB%E5%83%8F");
$a= preg_match_all('/\/images\/thumb\/[0-9a-z]+\/[0-9a-z]+\/%E5%8D%8A%E8%BA%AB%E5%83%8F_/',$html,$matches);
print_r($matches);

