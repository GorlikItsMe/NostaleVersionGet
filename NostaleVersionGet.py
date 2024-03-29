import requests
import hashlib
from pefile import PE
import time
import json
import os


def NostaleVersionGet(filecache=False):
    data = {"savetime": 0}
    if filecache:
        try:
            fp = open("NostaleVersionCache.json", "r")
            data = json.load(fp)
        except Exception:
            data = {"savetime": 0}

    if data["savetime"] < int(time.time()) - (5 * 60):  # cache 5min
        files = requests.get(
            "https://spark.gameforge.com/api/v1/patching/download/latest/nostale/default?locale=pl&architecture=x64&branchToken"
        ).json()["entries"]
        for f in files:
            if f["file"] == "NostaleClientX.exe":
                download_file("http://patches.gameforge.com" + f["path"], f["file"])
                hashNostaleClientX = md5(f["file"])
            if f["file"] == "NostaleClient.exe":
                download_file("http://patches.gameforge.com" + f["path"], f["file"])
                hashNostaleClient = md5(f["file"])

        version = fileversion("NostaleClient.exe")
        os.remove("NostaleClient.exe")
        os.remove("NostaleClientX.exe")
        data = {
            "savetime": int(time.time()),
            "hashNostaleClientX": hashNostaleClientX,
            "hashNostaleClient": hashNostaleClient,
            "version": version,
        }
        if filecache:
            fp = open("NostaleVersionCache.json", "w+")
            json.dump(data, fp)
            fp.close()

    return data


def download_file(url, filename):
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(filename, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
            f.close()


def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def fileversion(pename):
    pe = PE(pename)
    verinfo = pe.VS_FIXEDFILEINFO[0]
    filever = (
        verinfo.FileVersionMS >> 16,
        verinfo.FileVersionMS & 0xFFFF,
        verinfo.FileVersionLS >> 16,
        verinfo.FileVersionLS & 0xFFFF,
    )
    pe.close()
    return "%d.%d.%d.%d" % filever
