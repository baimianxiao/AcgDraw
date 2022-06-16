# -*- encoding:utf-8 -*-

from flask import Flask

app = Flask(__name__)


@app.route("/")
def hiworld():
    return "successful!"



if __name__ == "__main__":
    app.run()
