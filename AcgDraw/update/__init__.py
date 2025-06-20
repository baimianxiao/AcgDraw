# -*- encoding:utf-8 -*-
import asyncio
import os
import aiofiles as aiofiles
import aiohttp




from abc import ABC, abstractmethod



class UpdateHandle(ABC):

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

        :param url: 下载链接
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
            # print("文件"+name+"已存在")
            return True
        try:
            async with aiohttp.ClientSession(headers=self.headers) as session:
                async with session.get(url, timeout=10,ssl=False) as response:
                    async with aiofiles.open(str(file_path), "wb") as f:
                        await f.write(await response.read())
            # print(f"下载文件{name}成功")
            # print(f"下载文件{name}成功，url：{url}，储存目录：{path}")
            return True
        except TimeoutError:
            print(f"下载文件{name} 超时，url：{url}")
            return False
        except:
            print(f"下载文件 {name} 链接错误，url：{url}")
            return False

    def request_data(self, url: str, cookie: list):
        pass

    # 获取url链接内容
    async def get_url(self, url: str) -> str:
        result = ""
        retry = 5
        for i in range(retry):

            try:
                async with aiohttp.ClientSession(headers=self.headers) as session:
                    async with session.get(url,ssl=False) as resp:
                        result = await resp.text()
                break
            except TimeoutError:
                await asyncio.sleep(1)
        return result

from .arknights import UpdateHandleArk
from .genshin import UpdateHandleGen

__all__=[
    "UpdateHandle",
    "UpdateHandleArk",
]