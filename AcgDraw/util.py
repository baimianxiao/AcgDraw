# -*- coding: utf-8 -*-
import aiofiles
from json import dumps, loads, JSONDecodeError


# 写入json文件
async def json_write(path: str, data) -> bool:
    try:
        async with aiofiles.open(path, 'w', encoding='utf-8') as f:
            await f.write(dumps(data, ensure_ascii=False, indent=2))
        return True
    except Exception as e:
        print(f"将 JSON 写入文件时出错:{e}")
        return False


# 读取json文件
async def json_read(path):
    try:
        async with aiofiles.open(path, mode='r', encoding='utf-8') as f:
            data = await f.read()
        return loads(data)
    except JSONDecodeError:
        return False
