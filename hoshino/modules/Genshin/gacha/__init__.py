from hoshino import Service,priv
from .gacha import gacha_info , FILE_PATH , Gacha , POOL
import os
import json
from hoshino.util import DailyNumberLimiter
from ..config import Gacha10Limit,Gacha90Limit,Gacha180Limit


daily_limiter_10 = DailyNumberLimiter(Gacha10Limit)
daily_limiter_90 = DailyNumberLimiter(Gacha90Limit)
daily_limiter_180 = DailyNumberLimiter(Gacha180Limit)

sv_help = '''
-[@bot相遇之缘] 10连抽卡
-[@bot纠缠之缘] 90连抽卡
-[@bot原之井] 180连抽卡
-[原神卡池] 查看当前UP池
-[原神卡池切换] 切换其他原神卡池
'''.strip()

sv = Service(
    name = '原神抽卡',  #功能名
    use_priv = priv.NORMAL, #使用权限   
    manage_priv = priv.ADMIN, #管理权限
    visible = True, #False隐藏
    enable_on_default = True, #是否默认启用
    bundle = '原神', #属于哪一类
    help_ = sv_help #帮助文本
    )

@sv.on_fullmatch(["帮助原神抽卡"])
async def bangzhu_genshin_gacha(bot, ev):
    await bot.send(ev, sv_help) 
    

group_pool = {
    # 这个字典保存每个群对应的卡池是哪个，群号字符串为key,卡池名为value，群号不包含在字典key里卡池按默认DEFAULT_POOL
}

def save_group_pool():
    with open(os.path.join(FILE_PATH,'gid_pool.json'),'w',encoding='UTF-8') as f:
        json.dump(group_pool,f,ensure_ascii=False)



# 检查gid_pool.json是否存在，没有创建空的
if not os.path.exists(os.path.join(FILE_PATH,'gid_pool.json')):
    save_group_pool()



# 读取gid_pool.json的信息
with open(os.path.join(FILE_PATH,'gid_pool.json'),'r',encoding='UTF-8') as f:
    group_pool = json.load(f)




@sv.on_prefix(["相遇之缘"], only_to_me=True)
async def gacha_(bot, ev):
    gid = str(ev.group_id)
    userid = ev['user_id']
    if not daily_limiter_10.check(userid):
        await bot.send(ev, '今天已经抽了很多次啦，明天再来吧~')
        return
    G = Gacha(group_pool[gid]) if gid in group_pool else Gacha()
    daily_limiter_10.increase(userid)
    await bot.send(ev, G.gacha_10() , at_sender=True)

@sv.on_prefix(["纠缠之缘"], only_to_me=True)
async def gacha_(bot, ev):
    gid = str(ev.group_id)
    userid = ev['user_id']
    if not daily_limiter_90.check(userid):
        await bot.send(ev, '今天已经抽了很多次啦，明天再来吧~')
        return
    G = Gacha(group_pool[gid]) if gid in group_pool else Gacha()
    daily_limiter_90.increase(userid)
    await bot.send(ev, G.gacha_90(90) , at_sender=True)



@sv.on_prefix(["原之井"], only_to_me=True)
async def gacha_(bot, ev):
    gid = str(ev.group_id)
    userid = ev['user_id']
    if not daily_limiter_180.check(userid):
        await bot.send(ev, '今天已经抽了很多次啦，明天再来吧~')
        return
    daily_limiter_180.increase(userid)
    G = Gacha(group_pool[gid]) if gid in group_pool else Gacha()
    await bot.send(ev, G.gacha_90(180) , at_sender=True)



@sv.on_prefix(["原神卡池","原神up","原神UP"])
async def gacha_(bot, ev):
    gid = str(ev.group_id)

    info = gacha_info(group_pool[gid]) if gid in group_pool else gacha_info()
    await bot.send(ev, info , at_sender=True)

@sv.on_prefix(('原神卡池切换','原神切换卡池'))
async def set_pool(bot, ev):

    if not priv.check_priv(ev, priv.ADMIN):
        await bot.finish(ev, '只有群管理才能切换卡池', at_sender=True)

    pool_name = ev.message.extract_plain_text().strip()
    gid = str(ev.group_id)

    if pool_name in POOL.keys():
        if gid in group_pool:
            group_pool[gid] = pool_name
        else:
            group_pool.setdefault(gid,pool_name)
        save_group_pool()
        await bot.send(ev, f"卡池已切换为 {pool_name} ")
        return

    txt = "请使用以下命令来切换卡池\n"
    for i in POOL.keys():
        txt += f"原神卡池切换 {i} \n"

    await bot.send(ev, txt)
