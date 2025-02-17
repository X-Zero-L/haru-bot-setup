# -*- coding: utf-8 -*-
import hoshino
from hoshino import Service, priv
from hoshino.typing import CQEvent

from urllib.parse import quote, unquote

sv_help = '''
懒到极致了捏
群聊发送搜索词bot发送对应链接
- [百度一下+关键词]
- [bing一下+关键词]
- [谷歌一下+关键词]
- [github一下+关键词]
- [微博一下+关键词]
- [哔哩一下+关键词]
- [知乎一下+关键词]
'''.strip()

sv = Service(
    name = '百度一下',  #功能名
    use_priv = priv.NORMAL, #使用权限   
    manage_priv = priv.ADMIN, #管理权限
    visible = True, #False隐藏
    enable_on_default = True, #是否默认启用
    bundle = '通用', #属于哪一类
    help_ = sv_help #帮助文本
    )

@sv.on_fullmatch(["帮助百度一下"])
async def bangzhu_baidu(bot, ev):
    await bot.send(ev, sv_help)

@sv.on_prefix(("百度一下"))
async def search_baidu(bot, ev: CQEvent):
    if input := ev.message.extract_plain_text():
        words = quote(input)
        search_data = {
            "type": "share",
            "data": {
                "url": f"https://www.baidu.com/s?wd={words}",
                "title": f"百度一下:{input}",
                "content": "baidu.com",
            },
        }
        await bot.send(ev, search_data)
    else:
        share_data = {
            "type": "share",
            "data": {
                "url": "https://www.baidu.com/",
                "title": "百度一下，你就知道",
                "content": "baidu.com",
            },
        }
        await bot.send(ev, share_data)

@sv.on_prefix(("github一下"))
async def search_github(bot, ev: CQEvent):
    if input := ev.message.extract_plain_text():
        words = quote(input)
        search_data = {
            "type": "share",
            "data": {
                "url": f"https://github.com/search?q={words}",
                "title": f"GitHub一下:{input}",
                "content": "github.com",
            },
        }
        await bot.send(ev, search_data)
    else:
        share_data = {
            "type": "share",
            "data": {
                "url": "https://github.com/",
                "title": "GitHub: Where the world builds software · GitHub",
                "content": "github.com",
            },
        }
        await bot.send(ev, share_data)

@sv.on_prefix(("必应一下", "bing一下"))
async def search_bing(bot, ev: CQEvent):
    if input := ev.message.extract_plain_text():
        words = quote(input)
        search_data = {
            "type": "share",
            "data": {
                "url": f"https://cn.bing.com/search?q={words}",
                "title": f"必应(国内版)一下:{input}",
                "content": "cn.bing.com",
            },
        }
        await bot.send(ev, search_data)
    else:
        share_data = {
            "type": "share",
            "data": {
                "url": "https://cn.bing.com/",
                "title": "必应：Microsoft Bing",
                "content": "cn.bing.com",
            },
        }
        await bot.send(ev, share_data)

@sv.on_prefix(("谷歌一下", "google一下"))
async def search_google(bot, ev: CQEvent):
    if input := ev.message.extract_plain_text():
        words = quote(input)
        search_data = {
            "type": "share",
            "data": {
                "url": f"https://google.com/search?q={words}",
                "title": f"谷歌一下:{input}",
                "content": "google.com",
            },
        }
        await bot.send(ev, search_data)
    else:
        share_data = {
            "type": "share",
            "data": {
                "url": "https://google.com/",
                "title": "谷歌Google",
                "content": "google.com",
            },
        }
        await bot.send(ev, share_data)

@sv.on_prefix(("知乎一下"))
async def search_zhihu(bot, ev: CQEvent):
    if input := ev.message.extract_plain_text():
        words = quote(input)
        search_data = {
            "type": "share",
            "data": {
                "url": f"https://www.zhihu.com/search?type=content&q={words}",
                "title": f"知乎一下:{input}",
                "content": "zhihu.com",
            },
        }
        await bot.send(ev, search_data)
    else:
        share_data = {
            "type": "share",
            "data": {
                "url": "https://www.zhihu.com/",
                "title": "知乎 - 有问题，就会有答案",
                "content": "zhihu.com",
            },
        }
        await bot.send(ev, share_data)

@sv.on_prefix(("微博一下"))
async def search_weibo(bot, ev: CQEvent):
    if input := ev.message.extract_plain_text():
        words = quote(input)
        search_data = {
            "type": "share",
            "data": {
                "url": f"https://s.weibo.com/weibo?q={words}",
                "title": f"微博一下:{input}",
                "content": "weibo.com",
            },
        }
        await bot.send(ev, search_data)
    else:
        share_data = {
            "type": "share",
            "data": {
                "url": "https://weibo.com/",
                "title": "微博-随时随地发现新鲜事",
                "content": "weibo.com",
            },
        }
        await bot.send(ev, share_data)

@sv.on_prefix(("哔哩一下", "bili一下"))
async def search_bilibili(bot, ev: CQEvent):
    if input := ev.message.extract_plain_text():
        words = quote(input)
        search_data = {
            "type": "share",
            "data": {
                "url": f"https://search.bilibili.com/all?keyword={words}",
                "title": f"哔哩哔哩一下:{input}",
                "content": "bilibili是国内知名的视频弹幕网站，这里有及时的动漫新番，活跃的ACG氛围，有创意的Up主。大家可以在这里找到许多欢乐。",
            },
        }
        await bot.send(ev, search_data)
    else:
        share_data = {
            "type": "share",
            "data": {
                "url": "https://www.bilibili.com/",
                "title": "哔哩哔哩 (゜-゜)つロ 干杯~-bilibili",
                "content": "bilibili是国内知名的视频弹幕网站，这里有及时的动漫新番，活跃的ACG氛围，有创意的Up主。大家可以在这里找到许多欢乐。",
            },
        }
        await bot.send(ev, share_data)

@sv.on_prefix(("萌娘百科一下"))
async def search_moe(bot, ev: CQEvent):
    if input := ev.message.extract_plain_text():
        words = quote(input)
        search_data = {
            "type": "share",
            "data": {
                "url": f"https://zh.moegirl.org.cn/index.php?search={words}",
                "title": f"萌娘百科一下:{input}",
                "content": "萌娘百科是一个综合性ACGN百科站点，旨在完整准确收录动画、漫画、游戏、文学相关内容，以及青少年间流行的事物。",
            },
        }
        await bot.send(ev, search_data)
    else:
        share_data = {
            "type": "share",
            "data": {
                "url": "https://zh.moegirl.org.cn/",
                "title": "萌娘百科 万物皆可萌的百科全书 - zh.moegirl.org.cn",
                "content": "萌娘百科是一个综合性ACGN百科站点，旨在完整准确收录动画、漫画、游戏、文学相关内容，以及青少年间流行的事物。",
            },
        }
        await bot.send(ev, share_data)