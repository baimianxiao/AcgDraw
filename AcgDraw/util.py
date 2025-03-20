# -*- coding: utf-8 -*-
from typing import Union

import aiofiles
from json import dumps, loads, JSONDecodeError
import os
import aiohttp
import asyncio
from aiohttp import ClientError


# 异步下载GitHub文件
async def download_github_file(github_url: str, save_path: str) -> bool:
    """
    异步从GitHub下载文件并保存到本地
    :param github_url: GitHub文件页面URL或原始文件URL
    :param save_path: 本地保存路径（包含文件名）
    """
    try:
        # 转换普通页面URL为原始文件URL
        if "github.com" in github_url and "/blob/" in github_url:
            raw_url = github_url.replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")
        else:
            raw_url = github_url

        async with aiohttp.ClientSession() as session:
            async with session.get(raw_url, ssl=False) as response:
                response.raise_for_status()  # 检查HTTP状态码
                content = await response.read()

        # 创建保存目录（如果不存在）
        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        # 写入文件（同步写入）
        with open(save_path, "wb") as f:
            f.write(content)

        print(f"文件已成功下载到：{save_path}")
        return True

    except ClientError as e:
        print(f"下载失败：网络请求错误 - {str(e)}")
    except Exception as e:
        print(f"发生未知错误：{str(e)}")
    return False



def mkdir(paths: Union[str, list], root_dir: str = "") -> dict:
    """
    判断目录是否存在，并且在不存在时创建目录
    :param paths: 单个路径或路径列表
    :param root_dir: 根目录
    :return: 返回创建结果
    """
    if isinstance(paths, str):
        paths = [paths]
    results = {}
    for path in paths:
        full_path = os.path.join(root_dir, path)
        is_exists = os.path.exists(full_path)
        if not is_exists:
            os.makedirs(full_path.encode("utf-8"))
            results[path] = True
        else:
            results[path] = False
    return results


async def json_write_async(path: str, data) -> bool:
    """
    异步写入json文件
    :param path: 写入路径
    :param data: 写入数据
    :return: 是否成功
    """
    try:
        async with aiofiles.open(path, 'w', encoding='utf-8') as f:
            await f.write(dumps(data, ensure_ascii=False, indent=2))
        return True
    except Exception as e:
        print(f"将 JSON 写入文件时出错:{e}")
        return False


async def json_read_async(path):
    """
    异步读取json文件
    :param path: 读取路径
    :return: 读取数据
    """
    try:
        async with aiofiles.open(path, mode='r', encoding='utf-8') as f:
            data = await f.read()
        return loads(data)
    except JSONDecodeError:
        return False


def json_write(path: str, data) -> bool:
    """
    同步写入json文件
    :param path: 写入路径
    :param data: 写入数据
    :return: 是否成功
    """
    try:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(dumps(data, ensure_ascii=False, indent=2))
        return True
    except Exception as e:
        print(f"将 JSON 写入文件时出错:{e}")
        return False


# 读取json文件
def json_read(path):
    """
        同步读取json文件
        :param path: 读取路径
        :return: 读取数据
        """
    try:
        with open(path, mode='r', encoding='utf-8') as f:
            data = f.read()
        return loads(data)
    except JSONDecodeError:
        return False
