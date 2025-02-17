import json
import time
import string
import random
import hashlib
import requests
from . import util

config = util.get_config()

mhyVersion = "2.3.0"


def __md5__(text):
    _md5 = hashlib.md5()
    _md5.update(text.encode())
    return _md5.hexdigest()


def __get_ds__():
    n = "h8w582wxwgqvahcdkpvdhbh2w9casgfl"
    i = str(int(time.time()))
    r = ''.join(random.sample(string.ascii_lowercase + string.digits, 6))
    c = __md5__(f"salt={n}&t={i}&r={r}")
    return f"{i},{r},{c}"


def info(uid):
    server = 'cn_qd01' if uid[0] == "5" else 'cn_gf01'
    req = requests.get(
        url=f"https://api-takumi.mihoyo.com/game_record/genshin/api/index?server={server}&role_id={uid}",
        headers={
            'Accept': 'application/json, text/plain, */*',
            'DS': __get_ds__(),
            'Origin': 'https://webstatic.mihoyo.com',
            'x-rpc-app_version': mhyVersion,
            'User-Agent': 'Mozilla/5.0 (Linux; Android 9; Unspecified Device) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/39.0.0.0 Mobile Safari/537.36 miHoYoBBS/2.2.0',
            'x-rpc-client_type': '5',
            'Referer': 'https://webstatic.mihoyo.com/app/community-game-records/index.html?v=6',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,en-US;q=0.8',
            'X-Requested-With': 'com.mihoyo.hyperion',
            'Cookie': config.cookie,
        },
    )

    return util.dict_to_object(json.loads(req.text))


class stats:
    def __init__(self, data, max_hide=False):
        self.data = data
        self.max_hide = max_hide

    @property
    def active_day(self) -> int:
        return self.data['active_day_number']

    @property
    def active_day_str(self) -> str:
        return f'活跃天数: {self.active_day}'

    @property
    def achievement(self) -> int:
        return self.data['achievement_number']

    @property
    def achievement_str(self) -> str:
        return f'成就达成数: {self.achievement}'

    @property
    def anemoculus(self) -> int:
        return self.data['anemoculus_number']

    @property
    def anemoculus_str(self) -> str:
        if self.max_hide and self.anemoculus == 66:
            return ''
        return f'风神瞳: {self.anemoculus}/66'

    @property
    def geoculus(self) -> int:
        return self.data['geoculus_number']

    @property
    def geoculus_str(self) -> str:
        if self.max_hide and self.geoculus == 131:
            return ''
        return f'岩神瞳: {self.geoculus}/131'

    @property
    def avatar(self) -> int:
        return self.data['avatar_number']

    @property
    def avatar_str(self) -> str:
        return f'获得角色数: {self.avatar}'

    @property
    def way_point(self) -> int:
        return self.data['way_point_number']

    @property
    def way_point_str(self) -> str:
        if self.max_hide and self.way_point == 83:
            return ''
        return f'解锁传送点: {self.way_point}/83'

    @property
    def domain(self) -> int:
        return self.data['domain_number']

    @property
    def domain_str(self) -> str:
        return f'解锁秘境: {self.domain}'

    @property
    def spiral_abyss(self) -> str:
        return self.data['spiral_abyss']

    @property
    def spiral_abyss_str(self) -> str:
        return '' if self.spiral_abyss == '-' else f'当期深境螺旋: {self.spiral_abyss}'

    @property
    def common_chest(self) -> int:
        return self.data['common_chest_number']

    @property
    def common_chest_str(self) -> str:
        return f'普通宝箱: {self.common_chest}'

    @property
    def exquisite_chest(self) -> int:
        return self.data['exquisite_chest_number']

    @property
    def exquisite_chest_str(self) -> str:
        return f'精致宝箱: {self.exquisite_chest}'

    @property
    def luxurious_chest(self) -> int:
        return self.data['luxurious_chest_number']

    @property
    def luxurious_chest_str(self) -> str:
        return f'华丽宝箱: {self.luxurious_chest}'

    @property
    def precious_chest(self) -> int:
        return self.data['precious_chest_number']

    @property
    def precious_chest_str(self) -> str:
        return f'珍贵宝箱: {self.precious_chest}'

    @property
    def string(self):
        str_list = [
            self.active_day_str,
            self.achievement_str,
            self.anemoculus_str,
            self.geoculus_str,
            self.avatar_str,
            self.way_point_str,
            self.domain_str,
            self.spiral_abyss_str,
            self.luxurious_chest_str,
            self.precious_chest_str,
            self.exquisite_chest_str,
            self.common_chest_str
        ]
        return '\n'.join(list(filter(None, str_list)))
