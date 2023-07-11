# -*- encoding:utf-8 -*-
import os

import drawHandleArk
from flask import Flask, send_file

# import numpy as np
import io

app = Flask(__name__)


@app.route("/arknights/arknightsdraw", methods=['POST', 'GET'])
def arknights():
    img = drawHandleArk.ten_draw()
    file_object = io.BytesIO()
    img.save(file_object, 'PNG')
    file_object.seek(0)
    return send_file(file_object, mimetype='image/PNG')


@app.route('/', methods=['POST', 'GET'])
def arknights_draw():
    img = drawHandleArk.ten_draw()
    file_object = io.BytesIO()
    img.save(file_object, 'PNG')
    file_object.seek(0)
    return send_file(file_object, mimetype='image/PNG')


if __name__ == "__main__":
    app.run(debug=True)
    print("servers start")
