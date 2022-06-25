# -*- encoding:utf-8 -*-
import asyncio
import os
from urllib.parse import unquote

import aiofiles as aiofiles
import aiohttp
from lxml import etree, html


class TableData:
    pass


class CharData:
    name: str  # 名称
    star: int  # 星级
    limited: bool  # 限定
    getWay: str  # 获得途径
    pass


class UpdateHandle:

    def __init__(self, data_path: str, conf_path: str):
        self.headers = {
            "User-Agent": '"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)"'
        }
        self.data_path = data_path
        self.conf_path = conf_path
        pass

    def get_char_data(self):
        pass

    def get_table_data(self):
        pass

    def get_up_table(self):
        pass

    async def download_file(self, url: str, name: str, path: str) -> bool:
        r"""下载文件

        :param url: 指定发送群号
        :param name: 文件名
        :param path: 储存目录
        :rtype bool
        """
        dir_path = self.data_path + path
        file_path = self.data_path + path + name
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
            return True
        if os.path.exists(file_path):
            return True
        try:
            async with aiohttp.ClientSession(headers=self.headers) as session:
                async with session.get(url, timeout=10) as response:
                    async with aiofiles.open(str(file_path), "wb") as f:
                        await f.write(await response.read())
            print(f"下载文件{name}成功，url：{url}，储存目录：{path}")
            return True
        except TimeoutError:
            print(f"下载文件{name} 超时，url：{url}")
            return False
        except:
            print(f"下载文件 {name} 链接错误，url：{url}")
            return False

    def request_data(self, url: str, cookie: list):
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
                """这里sources修好了干员获取标签有问题的bug，如三星只能抽到卡缇就是这个原因"""
                sources = [_.strip('\n') for _ in char.xpath("./td[8]/text()")]
                url = "https://prts.wiki/w/文件:半身像_" + name + "_1.png"
                result = await self.get_url(url)

                if not result:
                    return ""
            except IndexError:
                continue
            member_dict = {
                "头像": unquote(str(avatar).split(" ")[-2]),
                "名称": name,
                "星级": int(str(star).strip()),
                "获取途径": sources,
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
                # char = html.tostring(char, encoding='utf-8').decode('utf-8')
                # print(char)
                image_url = char.xpath("./img/@data-srcset")
                print(image_url)
            except IndexError:
                continue

        # print(member_dict)

    async def get_url(self, url: str) -> str:
        result = ""
        retry = 5
        for i in range(retry):

            try:
                async with aiohttp.ClientSession(headers=self.headers) as session:
                    async with session.get(url) as resp:
                        result = await resp.text()
                break
            except TimeoutError:
                self.log_print()
                await asyncio.sleep(1)
        return result

    def log_print(self, message: str) -> bool:
        pass

    def test(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.get_info())


if __name__ == "__main__":
    app = UpdateHandle("../data/", "../conf/")
    app.test()
