"""The privilege of user discribed in an `int` number.

`0` is for Default or NotSet. The other numbers may change in future versions.
"""

from datetime import datetime

import hoshino
from hoshino import config
from hoshino.typing import CQEvent

BLACK = -999
DEFAULT = 0
NORMAL = 1
PRIVATE = 10
ADMIN = 21
OWNER = 22
WHITE = 51
SUPERUSER = 999
SU = SUPERUSER

#===================== block list =======================#
_black_group = {}  # Dict[group_id, expr_time]
_black_user = {}  # Dict[user_id, expr_time]


def set_block_group(group_id, time):
    _black_group[group_id] = datetime.now() + time


def set_block_user(user_id, time):
    if user_id not in hoshino.config.SUPERUSERS:
        _black_user[user_id] = datetime.now() + time


def check_block_group(group_id):
    if group_id in _black_group and datetime.now() > _black_group[group_id]:
        del _black_group[group_id]  # 拉黑时间过期
        return False
    return group_id in _black_group


def check_block_user(user_id):
    if user_id in _black_user and datetime.now() > _black_user[user_id]:
        del _black_user[user_id]  # 拉黑时间过期
        return False
    return user_id in _black_user


#========================================================#


def get_user_priv(ev: CQEvent):
    uid = ev.user_id
    if uid in hoshino.config.SUPERUSERS:
        return SUPERUSER
    if check_block_user(uid):
        return BLACK
    if uid in config.WHITE_LIST:
        return WHITE
    if ev['message_type'] == 'group':
        if not ev.anonymous:
            role = ev.sender.get('role')
            if role in ['admin', 'administrator']:
                return ADMIN
            elif role == 'member':
                return NORMAL
            elif role == 'owner':
                return OWNER
        return NORMAL
    return PRIVATE if ev['message_type'] == 'private' else NORMAL


def check_priv(ev: CQEvent, require: int) -> bool:
    return get_user_priv(ev) >= require if ev['message_type'] == 'group' else False
