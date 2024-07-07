# -*- encoding:utf-8 -*-
import os
from datetime import datetime

from flask import Flask, send_file, make_response
from flask_apscheduler import APScheduler
from io import BytesIO
from gevent import pywsgi
from AcgDraw.systemAction import log_output
import AcgDraw.drawHandleArk
import AcgDraw.updateArk


class Config(object):
    SCHEDULER_API_ENABLED = True


app = Flask(__name__)

scheduler = APScheduler()


# 方舟抽卡API地址
@app.route("/arknightsdraw", methods=['POST', 'GET'])
def arknights():
    img = AcgDraw.drawHandleArk.ten_draw()
    file_object = BytesIO()
    img.save(file_object, 'PNG')
    file_object.seek(0)
    response = make_response(file_object)
    response.headers["Content-Type"] = "image/png"
    return response


# 根目录
@app.route('/', methods=['POST', 'GET'])
def arknights_draw():
    img = AcgDraw.drawHandleArk.ten_draw()
    file_object = BytesIO()
    img.save(file_object, 'PNG')
    file_object.seek(0)
    response = make_response(file_object)
    response.headers["Content-Type"] = "image/png"
    return response


# 自动更新任务
@scheduler.task('interval', id='api_auto_update', days=1, misfire_grace_time=900)
def api_auto_update():
    log_output("INFO", "开始自动更新任务")
    AcgDraw.updateArk.UpdateHandleArk("../data/Arknights/", "../conf/Arknights/").start_update()


def server_start(mode="", host="127.0.0.1", port=11451):
    if mode == "debug":
        app.run(debug=True)
        print("测试环境")
    else:
        try:
            app.config.from_object(Config())
            scheduler.init_app(app)
            scheduler.start()
            server = pywsgi.WSGIServer((host, port), app)
            print("图片服务器已启动：http://" + host + ":" + str(port))
            server.serve_forever()
        except OSError:
            print("端口被占用，请修改端口")
            input("回车关闭")


if __name__ == "__main__":
    server_start()
