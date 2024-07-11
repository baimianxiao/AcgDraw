# -*- encoding:utf-8 -*-
import json
import re
from urllib.parse import unquote

from lxml import etree, html
from tqdm import tqdm, trange

from AcgDraw.systemAction import json_write
from AcgDraw.update import *


class UpdateHandleArk(UpdateHandle):
    def __init__(self, data_path: str, conf_path: str):
        super().__init__(data_path, conf_path)

    # 获取人物更新信息
    async def get_info(self):
        char_data_list = {}
        simple_star_list = {
            6: [],
            5: [],
            4: [],
            3: []
        }
        limit_activity = {
            "全部活动": [],
            "linkage": {},
            "limit_": {}
        }
        url = "https://wiki.biligame.com/arknights/干员数据表"
        result = await self.get_url(url)
        if not result:
            return ""
        dom = etree.HTML(result, etree.HTMLParser())
        char_list = dom.xpath("//table[@id='CardSelectTr']/tbody/tr")
        char_raw = char_list[1]
        name_list = char_raw.xpath("//center/a/@title")
        profession_list = char_raw.xpath("//tr[@data-param1]/@data-param1")
        star_list = char_raw.xpath("//tr[@data-param2]/@data-param2")
        sources_list = char_raw.xpath("//tr[@data-param6]/@data-param6")
        for char_id in trange(len(name_list), desc="处理人物素材", unit="char"):
            name = name_list[char_id]
            try:
                # 获取半身图/全身立绘
                url_root = "https://prts.wiki/w/文件:半身像_" + name + "_1.png"
                result = await self.get_url(url_root)
                if not result:
                    return ""
                dom = etree.HTML(result, etree.HTMLParser())
                image_url_1 = dom.xpath("//img[@decoding='async' and @width='180'and @height='360']/@src")
                image_url_path = re.search(r"/[a-zA-Z0-9]{1,2}/[a-zA-Z0-9]{1,2}/", str(image_url_1[0]))
            except IndexError:
                continue

            char_dict = {
                "名称": name,
                "职业": str(profession_list[char_id]),
                "星级": int(star_list[char_id][0]),
                "获取途径": [item.strip() for item in sources_list[char_id].split(',')],
                "半身像": "https://media.prts.wiki" + str(image_url_path.group()) + "半身像_" + name + "_1.png",
                "立绘": "https://media.prts.wiki" + str(image_url_path.group()) + "立绘_" + name + "_1.png"
            }
            # print(json.dumps(char_dict, ensure_ascii=False, indent=4))

            # 稀有度分类
            if "标准寻访" in char_dict["获取途径"]:
                if char_dict["星级"] == 6:
                    simple_star_list[6].append(name)
                elif char_dict["星级"] == 5:
                    simple_star_list[5].append(name)
                elif char_dict["星级"] == 4:
                    simple_star_list[4].append(name)
                elif char_dict["星级"] == 3:
                    simple_star_list[3].append(name)

            char_data_list[name] = char_dict
            # print(json.dumps(char_data_list, ensure_ascii=False, indent=2))
        json_write(self.data_path + 'char_star_list.json', simple_star_list)
        json_write(self.data_path + 'char_data_dict.json', char_data_list)
        # print(char_data_list)
        return char_data_list
        """profession = char.xpath("./tr/@data-param1")[0]
            sources = [_.strip('\n') for _ in char.xpath("./td[8]/text()")]
            print("############################################################\n\n\n\n\n")
            
            char_dict = {
                "名称": name_list[id],
                "职业": str(profession[id]),
                "星级": int(str(star).strip()),
                "获取途径": sources,
                "半身像": "https://prts.wiki" + str(image_url_path.group()) + "/半身像_" + name + "_1.png",
                "立绘": "https://prts.wiki" + str(image_url_path.group()) + "/立绘_" + name + "_1.png"
            }        
            print(json.dumps(char_dict, ensure_ascii=False, indent=2))
    """

    # 下载图片数据
    async def char_image_download(self, char_list):
        download_path = "image/char/"
        with tqdm(range(len(char_list)), desc="下载图片素材", unit="char") as pbar:
            for char in range(len(char_list)):
                name = list(char_list)[char]
                await self.download_file(char_list[name]["半身像"], "半身像_" + name + ".png", download_path)
                await self.download_file(char_list[name]["立绘"], "立绘_" + name + ".png", download_path)
                pbar.set_postfix(prograss=str(name) + "下载完毕")
                pbar.update(1)

    def start_update(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        char_list = loop.run_until_complete(self.get_info())
        loop.run_until_complete(self.char_image_download(char_list))


if __name__ == "__main__":
    UpdateHandleArk("../data/Arknights/", "../conf/Arknights/").start_update()



