from flask import Flask, jsonify
from NostaleVersionGet import NostaleVersionGet
import json
import time
import NostaleServerStatusBot
import os

app = Flask(__name__)
COMMENT = "Cache is every 2min. Try dont spam this api (heroku can close it)"


@app.route("/")
def index():
    try:
        f = open("cache.json")
        d = json.load(f)
        if d["lastUpdateTime"] + 120 < int(time.time()):
            raise Exception("Too old data, refresh")
        d["cache"] = True
    except Exception:
        d = json.loads(version().data)

        # if config is specifed
        if os.environ.get("LOGIN_SERVER_IP", default=None) is not None:
            status = NostaleServerStatusBot.CanConnect(nostale_version_json=d)
            if status is True:
                d["canConnectLoginServer"] = True
                d["canConnectLoginServerMsg"] = "OK"
            else:
                d["canConnectLoginServer"] = False
                d["canConnectLoginServerMsg"] = status

        d["lastUpdateTime"] = int(time.time())
        d["cache"] = False
        f = open("cache.json", "w")
        json.dump(d, f)

    f.close()
    d["_comment"] = COMMENT
    return jsonify(d)


@app.route("/version")
def version():
    try:
        f = open("cache_version.json")
        d = json.load(f)
        if d["lastUpdateTime"] + 120 < int(time.time()):
            raise Exception("Too old data, refresh")
        d["cache"] = True
    except Exception:
        d = NostaleVersionGet()
        d["lastUpdateTime"] = int(time.time())
        d["cache"] = False
        f = open("cache_version.json", "w")
        json.dump(d, f)

    f.close()
    d["_comment"] = COMMENT
    return jsonify(d)


if __name__ == "__main__":
    app.run(threaded=True, port=5000)
