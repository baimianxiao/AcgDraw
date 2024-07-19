# -*- coding: utf-8 -*-
import aiofiles
from json import dumps, loads, JSONDecodeError


# 异步写入json文件
async def json_write_async(path: str, data) -> bool:
    try:
        async with aiofiles.open(path, 'w', encoding='utf-8') as f:
            await f.write(dumps(data, ensure_ascii=False, indent=2))
        return True
    except Exception as e:
        print(f"将 JSON 写入文件时出错:{e}")
        return False


# 异步读取json文件
async def json_read_async(path):
    try:
        async with aiofiles.open(path, mode='r', encoding='utf-8') as f:
            data = await f.read()
        return loads(data)
    except JSONDecodeError:
        return False


# 同步写入json文件
def json_write(path: str, data) -> bool:
    try:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(dumps(data, ensure_ascii=False, indent=2))
        return True
    except Exception as e:
        print(f"将 JSON 写入文件时出错:{e}")
        return False


# 读取json文件
def json_read(path):
    try:
        with open(path, mode='r', encoding='utf-8') as f:
            data = f.read()
        return loads(data)
    except JSONDecodeError:
        return False
