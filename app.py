from flask import Flask, request, jsonify
from NostaleVersionGet import NostaleVersionGet
import json
import time

app = Flask(__name__)

@app.route('/')
def index():
    try:
        f = open("cache.json")
        d = json.load(f)
        if d['lastUpdateTime'] + 120 < int(time.time()):
            raise Exception("Too old data, refresh")
        d['cache'] = True
    except:
        f = open("cache.json", "w")
        d = NostaleVersionGet()
        d['lastUpdateTime'] = int(time.time())
        d['cache'] = False
        json.dump(d, f)

    f.close()
    d['_comment'] = "Cache is every 2min. Try dont spam this api (heroku can close it)"
    return jsonify(d)

if __name__ == '__main__':
    app.run(threaded=True, port=5000)