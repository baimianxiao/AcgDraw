# -*- encoding:utf-8 -*-
import re
from urllib.parse import unquote

from lxml import etree

from update import *


class UpdateHandleArk(UpdateHandle):
    def __init__(self):
        pass

    async def get_info(self):
        member_data_list = {}
        url = "https://wiki.biligame.com/arknights/干员数据表"
        result = await self.get_url(url)
        if not result:
            return ""
        dom = etree.HTML(result, etree.HTMLParser())
        char_list = dom.xpath("//table[@id='CardSelectTr']/tbody/tr")
        for char in char_list:
            try:
                avatar = char.xpath("./td[1]/div/div/div/a/img/@srcset")[0]
                name = char.xpath("./td[2]/a/text()")[0]
                star = char.xpath("./td[5]/text()")[0]
                sources = [_.strip('\n') for _ in char.xpath("./td[8]/text()")]
                url = "https://prts.wiki/w/文件:半身像_" + name + "_1.png"
            except IndexError:
                continue
            member_dict = {
                "头像": unquote(str(avatar).split(" ")[-2]),
                "名称": name,
                "星级": int(str(star).strip()),
                "获取途径": sources,
                "半身像": None,
                "立绘": None
            }

            # await self.download_file(member_dict["头像"], name + ".png", "image/ch/")
            member_data_list[name] = member_dict

        # 获取半身图
        url = "https://prts.wiki/w/PRTS:文件一览/干员精英0半身像"
        result = await self.get_url(url)
        if not result:
            return ""
        dom = etree.HTML(result, etree.HTMLParser())
        char_list = dom.xpath("//div[@id='mw-content-text']/div/p/a")
        for char in char_list:
            try:
                image_url = unquote(str(char.xpath("./img/@data-srcset")).split(" ")[-2])
                url_root = re.match("/images/thumb(/.*?/.*?)/", image_url)
                image_url_1 = ""
                image_url_2 = ""
                print(image_url)
                print(url_root)

            except IndexError:
                continue

        # print(member_dict)
