# -*- encoding:utf-8 -*-
import json
import re
from urllib.parse import unquote

from update import *


class UpdateHandleArk(UpdateHandle):
    def __init__(self, data_path: str, conf_path: str):
        super().__init__(data_path, conf_path)

    async def get_info(self):
        char_data_list = {}
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
            except IndexError:
                continue
            char_dict = {
                "头像": unquote(str(avatar).split(" ")[-2]),
                "名称": name,
                "星级": int(str(star).strip()),
                "获取途径": sources,
                "半身像": None,
                "立绘": None
            }
            # print(json.dumps(char_dict,ensure_ascii=False,indent=2))
            # await self.download_file(member_dict["头像"], name + ".png", "image/ch/")
            char_data_list[name] = char_dict
        # print(json.dumps(member_data_list,ensure_ascii=False,indent=2))

        # 获取半身图/全身立绘
        for char in char_data_list:
            url_root = "https://prts.wiki/w/文件:半身像_" + char + "_1.png"
            result = await self.get_url(url_root)
            if not result:
                return ""
            dom = etree.HTML(result, etree.HTMLParser())
            image_url_1 = dom.xpath("//img[@decoding='async' and @width='180'and @height='360']/@src")
            print(image_url_1)
            image_url_1=re.match("/image",image_url_1[0])
            print(image_url_1)
            char_dict=char_data_list[char]



    def test(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.get_info())


if __name__ == "__main__":
    UpdateHandleArk("../data/", "../conf/").test()
