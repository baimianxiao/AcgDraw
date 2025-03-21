# -*- encoding：utf-8 -*-

from datetime import datetime
from os import getcwd
from os.path import join
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from contextlib import asynccontextmanager
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
import uvicorn
import os
from fastapi import Request

from AcgDraw import DrawHandleArk, DrawHandleGen
from AcgDraw.image import image_output, ImageHandleArk,ImageHandleGen
from AcgDraw.url_tool import generate_temp_image_url,clean_temp_folder,url_enable

work_dir = getcwd()

temp_dir = os.path.join(os.getcwd(), "temp-images")
os.makedirs(temp_dir, exist_ok=True)

async def initialize_app(app: FastAPI):
    app.state.ark_draw = DrawHandleArk(join(work_dir, "data", "Arknights", "char_star_list.json"))
    app.state.ark_image = ImageHandleArk(join(work_dir, "data", "Arknights", "char_data_dict.json"),
                                         join(work_dir, "data", "Arknights", "image"))
    app.state.gen_draw = DrawHandleGen()
    app.state.gen_image = ImageHandleGen(join(work_dir, "data", "Arknights", "char_data_dict.json"),
                                         join(work_dir, "data", "Arknights", "image"))
    # 装载图片
    await app.state.ark_draw.data_reload()
    await app.state.ark_image.data_reload()
    await app.state.gen_draw.data_reload()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await initialize_app(app)
    await auto_update()
    scheduler.start()
    yield
    scheduler.shutdown()

api_app = FastAPI(lifespan=lifespan)
api_app.mount("/tmp", StaticFiles(directory="temp-images"), name="temp-images")

async def auto_update():
    print("定时任务执行：当前时间:", datetime.now())


scheduler = AsyncIOScheduler()

scheduler.add_job(
    func=auto_update,
    trigger=IntervalTrigger(days=1),
    id="auto_update",
    replace_existing=True,
)

scheduler.add_job(
    func=clean_temp_folder,
    trigger="interval",
    hours=1,
    id="auto_clean",
    replace_existing=True,
)


@api_app.get("/")
async def root():
    return {"message": "又一个AcgDraw的站点被发现了", "version": "1.0", "ArknightsDraw": "/ArknightsDraw"}


@api_app.get("/ArknightsDraw")
async def arknights(request: Request):
    result = await api_app.state.ark_draw.char_ten_pulls()
    pil_image = await api_app.state.ark_image.char_ten_pulls(result)
    img_byte_arr = await image_output(pil_image)

    if url_enable:
        # 检查请求参数 type 是否为 url
        type_param = request.query_params.get("type")
        if type_param == "url":
            temp_image_url = generate_temp_image_url(pil_image)
            return {"image_url": temp_image_url}

    # 使用流式传输返回图片
    response = StreamingResponse(
        img_byte_arr,
        media_type="image/PNG",
    )
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"

    return response


@api_app.get("/GenshinDraw")
async def arknights(request: Request):
    result = await api_app.state.gen_draw.char_ten_pulls()
    pil_image = await api_app.state.gen_image.char_ten_pulls(result)
    img_byte_arr = await image_output(pil_image)

    if url_enable:
        # 检查请求参数 type 是否为 url
        type_param = request.query_params.get("type")
        if type_param == "url":
            temp_image_url = generate_temp_image_url(pil_image)
            return {"image_url": temp_image_url}

    # 使用流式传输返回图片
    response = StreamingResponse(
        img_byte_arr,
        media_type="image/PNG",
    )
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"

    return response


@api_app.get("/api-admin")
async def api_admin():
    return {"message": "管理员"}


if __name__ == "__main__":
    uvicorn.run(api_app, host="0.0.0.0", port=8000)
