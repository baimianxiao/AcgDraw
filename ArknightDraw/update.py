# -*- encoding:utf-8 -*-
import os
from lxml import etree


class TableData:
    pass


class CharData:
    name: str  # 名称
    star: int  # 星级
    limited: bool  # 限定
    getWay: str  # 获得途径
    pass


class UpdateHandle:

    def __int__(self):
        pass

    def get_char_data(self):
        pass

    def get_table_data(self):
        pass

    def get_up_table(self):
        pass

    def _create_dirs(self):
        pass

    def _download_file(self, url: str, file_name: str, path: str):
        pass

    def _request_data(self, url: str, cookie: list):
        pass

    def get_info(self):
        info = {}
        url = "https://wiki.biligame.com/arknights/干员数据表"
        result = await self.get_url(url)
        if not result:
            logger.warning(f"更新 {self.game_name_cn} 出错")
            return
        dom = etree.HTML(result, etree.HTMLParser())
        char_list = dom.xpath("//table[@id='CardSelectTr']/tbody/tr")
        for char in char_list:
            try:
                avatar = char.xpath("./td[1]/div/div/div/a/img/@srcset")[0]
                name = char.xpath("./td[2]/a/text()")[0]
                star = char.xpath("./td[5]/text()")[0]
                """这里sources修好了干员获取标签有问题的bug，如三星只能抽到卡缇就是这个原因"""
                sources = [_.strip('\n') for _ in char.xpath("./td[8]/text()")]
            except IndexError:
                continue
            member_dict = {
                "头像": unquote(str(avatar).split(" ")[-2]),
                "名称": remove_prohibited_str(str(name).strip()),
                "星级": int(str(star).strip()),
                "获取途径": sources,
            }
            info[member_dict["名称"]] = member_dict

