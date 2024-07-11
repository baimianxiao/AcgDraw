# -*- encoding：utf-8 -*-

from datetime import datetime
from io import BytesIO
from os import getcwd
from os.path import join

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from contextlib import asynccontextmanager
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
import uvicorn

from AcgDraw import DrawHandleArk
from AcgDraw.image import ImageHandleArk

work_dir = getcwd()


async def initialize_app(app: FastAPI):
    app.state.draw = DrawHandleArk(join(work_dir, "data", "Arknights", "char_star_list.json"))
    app.state.image = ImageHandleArk(join(work_dir, "data", "Arknights", "char_data_dict.json"),
                                     join(work_dir, "data", "Arknights", "image"))
    await app.state.draw.data_reload()
    await app.state.image.data_reload()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await initialize_app(app)
    await auto_update()
    scheduler.start()
    yield
    scheduler.shutdown()


api_app = FastAPI(lifespan=lifespan)


async def auto_update():
    print("定时任务执行：当前时间:", datetime.now())


scheduler = AsyncIOScheduler()

scheduler.add_job(
    func=auto_update,
    trigger=IntervalTrigger(days=1),
    id="auto_update",
    replace_existing=True,
)


@api_app.get("/")
async def root():
    return {"message": "又一个AcgDraw的站点被发现了", "version": "1.0","ArknightsDraw":"/arknightsdraw"}


@api_app.get("/arknightsdraw")
async def arknights():
    result = await api_app.state.draw.char_ten_pulls()
    pil_image = await api_app.state.image.char_ten_pulls(result)
    # 将PIL图片保存到BytesIO对象中
    img_byte_arr = BytesIO()
    pil_image.save(img_byte_arr, format="PNG")
    # 重置BytesIO对象指针到开始位置
    img_byte_arr.seek(0)
    # 使用流式传输返回图片
    response= StreamingResponse(
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
