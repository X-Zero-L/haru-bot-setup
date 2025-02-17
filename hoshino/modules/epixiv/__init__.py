import time
from nonebot import *
from . import util, pixiv, permission, download, short_url

from hoshino import Service, priv  # 如果使用hoshino的分群管理取消注释这行

sv_help = '''
- [pixiv]
'''.strip()

sv = Service(
    name = 'epixiv',  #功能名
    use_priv = priv.NORMAL, #使用权限   
    manage_priv = priv.ADMIN, #管理权限
    visible = True, #False隐藏
    enable_on_default = False, #是否默认启用
    bundle = '娱乐', #属于哪一类
    help_ = sv_help #帮助文本
    )

@sv.on_fullmatch(["帮助换脸"])
async def bangzhu_pixiv(bot, ev):
    await bot.send(ev, sv_help, at_sender=True)
# 初始化配置文件

config = util.get_config()

db = util.init_db(config.cache_dir)
db_recommend = util.init_db(config.cache_dir, 'recommend')
# 初始化nonebot
_bot = get_bot()
admins = _bot.config.SUPERUSERS

rules = config.rules

# 初始化p站配置
epixiv = pixiv.epixiv(
    rules.refresh_day,
    rules.search_sanity_level_count
)

try:
    epixiv.auth(refresh_token=config.pixiv.refresh_token)
except Exception as e:
    print(f'登录p站失败了 请检查配置. {e.body}')


@sv.on_message('group')
async def epixiv_main(*params):
    bot, ctx = (_bot, params[0]) if len(params) == 1 else params

    msg = str(ctx['message']).strip()
    if keyword := util.get_msg_keyword(
        config.comm.get_image_header, msg, True
    ):
        comm, footer = util.get_msg_keyword(config.comm.get_image_footer, keyword)
        keyword = await search(ctx, footer + comm)
        await ptag(ctx, keyword)
    if keyword := util.get_msg_keyword(config.comm.show_meta_pages, msg, True):
        await show_meta_pages(ctx, keyword)
    if keyword := util.get_msg_keyword(config.comm.recommend, msg, True):
        await recommend(ctx, keyword)
    if keyword := util.get_msg_keyword(config.comm.ptag, msg, True):
        await ptag(ctx, keyword)


async def search(ctx, keyword: str):
    keyword = keyword.strip()
    comm = ''
    next_page = util.get_msg_keyword(config.comm.next_page, keyword)
    if next_page:
        comm, keyword = next_page
        next_page = True

    is_r18 = util.get_msg_keyword(rules.r18_flag, keyword + comm) or ''
    if is_r18:
        comm, keyword = is_r18
        is_r18 = 'r18'

    sanity_level = 6
    is_noh = util.get_msg_keyword(rules.noh_flag, keyword + comm) or ''
    if is_noh:
        comm, keyword = is_noh
        is_noh = 'noh'
        sanity_level = 2

    if not keyword:
        return ''

    uid = ctx.user_id
    is_group = ctx.detail_type == 'group'
    page_flag = str(ctx.group_id if is_group else uid)

    if is_r18 and is_group and not rules.group_r18:
        await _bot.send(ctx, '群内不许ghs')
        return ''

    ps = permission.user(uid, timeout=5 * 60)

    if ps.check() and uid not in admins:
        await _bot.send(ctx, f'正在处理啦 等一等哈  {ps.msg()}')
        return ''
    ps.running('搜索中...')
    await _bot.send(ctx, '正在搜索 请稍等')
    db_key = keyword + is_r18 + is_noh
    search_db = db.get(db_key, {})
    search_db.setdefault('create_time', time.time())
    search_db.setdefault('keyword', db_key)
    search_db.setdefault('illusts', [])
    search_db.setdefault(page_flag, 1)
    search_db = util.dict_to_object(search_db)

    illusts = search_db.illusts
    if search_db.create_time + rules.refresh_day * 24 * 60 * 60 < time.time() or not illusts:
        print('pixiv refresh cache..')
        illusts = await epixiv.search(keyword, search_sort_num=rules.search_sort_num, is_r18=bool(is_r18),
                                      sanity_level=sanity_level)
        if not illusts:
            ps.done()
            await _bot.send(ctx, '嗨呀 都没搜索到, 要不你换个搜')
            return keyword
        search_db.illusts = illusts
        db[db_key] = search_db
    else:
        print(f'use cache len: {len(illusts)}')

    ps.running('下载图片中...')
    workers = rules.show_image_count
    start = 0
    if next_page:
        start = search_db[page_flag] * workers
        search_db[page_flag] += 1
        db[db_key] = search_db

    illusts = illusts[start:start + workers]

    if next_page and not illusts:
        illusts = illusts[:workers]
        search_db[page_flag] = 1
        db[db_key] = search_db

    data = epixiv.download_illusts_img(illusts)
    ps.running('处理消息中...')
    await print_illusts(ctx, data)
    ps.done()
    return keyword


async def print_illusts(ctx, illusts):
    show_image_comm = '此图有%s张, 使用下面的命令查看剩下的图\n全部图片#%s'
    for illust in illusts:
        image_urls = illust.image_urls
        original = short_url.short(image_urls.original) if config.setting.short_url_enable else image_urls.original
        msg = {
            'title': illust.title,
            'id': illust.id,
            'original': show_image_comm % (len(illust.meta_pages), illust.id)
            if illust.meta_pages
            else original,
            'recommend': f'相同口味#{illust.id}',
            'img': MessageSegment.image(illust.local_img),
        }
        await _bot.send(ctx, config.str.print.format(**msg))


async def show_meta_pages(ctx, keyword: str):
    illust_id = util.get_illust_id(keyword)

    if not illust_id:
        return ''
    uid = ctx.user_id
    ps = permission.user(uid, timeout=5 * 60)

    if ps.check() and uid not in admins:
        await _bot.send(ctx, f'正在处理啦 等一等哈  {ps.msg()}')
        return ''
    ps.running('查找中..')
    await _bot.send(ctx, '嗯嗯, 现在就去看看')
    illust, images = epixiv.get_meta_pages(illust_id)

    if epixiv.illust_is_r18(illust) and not rules.group_r18 and ctx.detail_type == 'group':
        ps.done()
        await _bot.send(ctx, '这是限制级组图 群内不许ghs!')
        return ''

    ps.running('解密中..')
    local_list = list(map(lambda x: download.get_img(x), images))

    for index, value in enumerate(images):
        original = short_url.short(value) if config.setting.short_url_enable else value
        msg = {
            'original': original,
            'img': MessageSegment.image(local_list[index])
        }
        await _bot.send(ctx, config.str.show_meta_pages.format(**msg))

    ps.done()


async def recommend(ctx, keyword: str):
    illust_id = util.get_illust_id(keyword)
    if not illust_id:
        return ''

    uid = ctx.user_id
    is_group = ctx.detail_type == 'group'
    page_flag = str(ctx.group_id if is_group else uid)
    ps = permission.user(uid, timeout=5 * 60)
    # can_r18 = is_group and rules.group_r18
    can_r18 = not is_group and rules.private_r18
    if ps.check() and uid not in admins:
        await _bot.send(ctx, f'正在处理啦 等一等哈  {ps.msg()}')
        return ''
    await _bot.send(ctx, '现在就去做一份.')

    rc_db = db_recommend.get(str(illust_id), {})
    rc_db.setdefault('create_time', time.time())
    rc_db.setdefault('illust_id', str(illust_id))
    rc_db.setdefault('illusts', [])
    rc_db.setdefault(page_flag, 1)
    rc_db = util.dict_to_object(rc_db)
    illusts = rc_db.illusts
    ps.running('搜索数据中...')
    if rc_db.create_time + rules.refresh_day * 24 * 60 * 60 < time.time() or not illusts:
        print('pixiv refresh recommend cache..')
        illusts = epixiv.recommend(illust_id, can_r18=can_r18)
        if not illusts:
            ps.done()
            await _bot.send(ctx, '阿勒 , 没有什么推荐呢')
            return keyword
        rc_db.illusts = illusts
        db_recommend[keyword] = rc_db
    ps.running('下载图片中...')
    data = epixiv.download_illusts_img(illusts[:rules.show_image_count])
    await print_illusts(ctx, data)
    ps.done()
    return ''


async def ptag(ctx, keyword: str):
    keyword = keyword.strip()
    if ac := epixiv.auto_complete(keyword):
        tag_info = epixiv.get_tag_img(ac[0]['text'])
        if not tag_info:
            await _bot.send(ctx, '没有搜索到标签信息呢')
            return
        ac_str = '\n'.join(map(lambda x: f"{x['translation']}  {x['text']}", ac))
        tag_info['local_img'] = MessageSegment.image(tag_info['local_img'])
        tag_info['ac'] = ac_str
        await _bot.send(ctx, config.str.auto_complete.format(**tag_info))
