# coding=utf-8
from bs4 import BeautifulSoup
import urllib.request
import urllib.error
import urllib.parse
import json
import time

baseurl = "https://ak-data-2.sapk.ch/api/v2/pl4"
tribaseurl = "https://ak-data-2.sapk.ch/api/v2/pl3"


def getURL(url):
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
    }
    try:
        response = urllib.request.Request(url=url, headers=headers, method="GET")
        req = urllib.request.urlopen(response,timeout=3)
        info = str(BeautifulSoup(req.read().decode('utf-8'), "html.parser"))
    except urllib.error.URLError as e:
        return e
    return info

def getID(nickname):#获取牌谱屋角色ID
    nickname = urllib.parse.quote(nickname) #UrlEncode转换
    url = f"{baseurl}/search_player/{nickname}?limit=9"
    data = getURL(url)
    if isinstance(data,urllib.error.URLError):
        return -404
    datalist = json.loads(data)
    return -1 if datalist == [] else datalist

def gettriID(nickname):
    nickname = urllib.parse.quote(nickname) #UrlEncode转换
    url = f"{tribaseurl}/search_player/{nickname}?limit=9"
    data = getURL(url)
    if isinstance(data,urllib.error.URLError):
        return -404
    datalist = json.loads(data)
    return -1 if datalist == [] else datalist


def selectLevel(room_level):
    level_list = []
    if room_level == "0":
        level_list.extend(("16.12.9", "15.11.8"))
    elif room_level == "1":
        level_list.extend(("9", "8"))
    elif room_level == "2":
        level_list.extend(("12", "11"))
    elif room_level == "3":
        level_list.extend(("16", "15"))
    return level_list

def select_triLevel(room_level):
    level_list = []
    if room_level == "0":
        level_list.extend(("22.24.26", "21.23.25"))
    elif room_level == "1":
        level_list.extend(("22", "21"))
    elif room_level == "2":
        level_list.extend(("24", "23"))
    elif room_level == "3":
        level_list.extend(("26", "25"))
    return level_list

def select_triInfo(id,room_level): #信息查询
    localtime = time.time()
    urltime = str(int(localtime*1000)) #时间戳
    basicurl = f"{tribaseurl}/player_stats/{str(id)}/1262304000000/{urltime}?mode="
    extendurl = f"{tribaseurl}/player_extended_stats/{str(id)}/1262304000000/{urltime}?mode="
    data_list = []
    level_list = select_triLevel(room_level)
    for i in range(2):
        data_list.extend(
            (
                getURL(basicurl + level_list[i]),
                getURL(extendurl + level_list[i]),
            )
        )
    return data_list


def selectInfo(id,room_level): #信息查询
    localtime = time.time()
    urltime = str(int(localtime*1000)) #时间戳
    basicurl = f"{baseurl}/player_stats/{str(id)}/1262304000000/{urltime}?mode="
    extendurl = f"{baseurl}/player_extended_stats/{str(id)}/1262304000000/{urltime}?mode="
    data_list = []
    level_list = selectLevel(room_level)
    for i in range(2):
        data_list.extend(
            (
                getURL(basicurl + level_list[i]),
                getURL(extendurl + level_list[i]),
            )
        )
    return data_list

def selectRecord(id):
    localtime = time.time()
    urltime = str(int(localtime * 1000))  # 时间戳
    basicurl = f"{baseurl}/player_stats/{str(id)}/1262304000000/{urltime}?mode=16.12.9.15.11.8"
    count = str(json.loads(getURL(basicurl))["count"])
    recordurl = f"{baseurl}/player_records/{str(id)}/{urltime}/1262304000000?limit=5&mode=16.12.9.15.11.8&descending=true&tag={count}"
    return getURL(recordurl)

def select_triRecord(id):
    localtime = time.time()
    urltime = str(int(localtime * 1000))  # 时间戳
    basicurl = f"{tribaseurl}/player_stats/{str(id)}/1262304000000/{urltime}?mode=16.12.9.15.11.8"
    count = str(json.loads(getURL(basicurl))["count"])
    recordurl = f"{tribaseurl}/player_records/{str(id)}/{urltime}/1262304000000?limit=5&mode=16.12.9.15.11.8&descending=true&tag={count}"
    return getURL(recordurl)
