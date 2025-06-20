# -*- encoding:utf-8 -*-
from lxml import etree, html
from tqdm import tqdm, trange
import re
import os
import aiofiles as aiofiles
import aiohttp
import asyncio

from . import UpdateHandle
from AcgDraw.util import json_write_async
from AcgDraw.update import UpdateHandle

class UpdateHandleArk(UpdateHandle
                      ):
    def __init__(self, data_path: str, conf_path: str):
        super().__init__(data_path, conf_path)

    # 获取人物更新信息
    async def get_info(self):
        char_data_dict = {}
        char_rarity_dict = {
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
        # 过滤掉空值和逗号
        name_list = [item for item in name_list if item not in ("", ",")]
        profession_list = [item for item in profession_list if item not in ("", ",")]
        star_list = [item for item in star_list if item not in ("", ",")]
        sources_list = [item for item in sources_list if item not in ("", ",")]

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
            try:
                char_dict = {
                    "名称": name,
                    "职业": str(profession_list[char_id]),
                    "星级": int(star_list[char_id][0]),
                    "获取途径": [item.strip() for item in sources_list[char_id].split(',')],
                    "半身像": "https://media.prts.wiki" + str(image_url_path.group()) + "半身像_" + name + "_1.png",
                    "立绘": "https://media.prts.wiki" + str(image_url_path.group()) + "立绘_" + name + "_1.png"
                }
            except:
                continue
            # print(json.dumps(char_dict, ensure_ascii=False, indent=4))

            # 稀有度分类
            if "标准寻访" in char_dict["获取途径"]:
                if char_dict["星级"] == 6:
                    char_rarity_dict[6].append(name)
                elif char_dict["星级"] == 5:
                    char_rarity_dict[5].append(name)
                elif char_dict["星级"] == 4:
                    char_rarity_dict[4].append(name)
                elif char_dict["星级"] == 3:
                    char_rarity_dict[3].append(name)

            char_data_dict[name] = char_dict
            # print(json.dumps(char_data_list, ensure_ascii=False, indent=2))
        rarity_dict={}
        data_dict={}
        rarity_dict['char_list']=char_rarity_dict
        data_dict['char_data_dict']=char_data_dict
        await json_write_async(self.data_path + 'rarity_dict.json', char_rarity_dict)
        await json_write_async(self.data_path + 'data_dict.json', char_data_dict)
        # print(char_data_list)
        return char_data_dict

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