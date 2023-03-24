import re
from typing import List


_regattr = re.compile('[A-Z]{3}')

class DummyList(list):
    def __init__(self, list: List[int]):
        super().__init__(list)

    def __contains__(self, o: object) -> bool:
        return any(x in o for x in self) if type(o) is set else super().__contains__(o)
def parseCondition(cond: str):
    cond2 = _regattr.sub(lambda m: f'getattr(x, "{m.group()}")', cond).replace('?[', ' in DummyList([').replace('![', 'not in DummyList([').replace(']', '])')
    while True:
        try:
            return eval(f'lambda x: {cond2}')
        except:
            print(f'[WARNING] missing ) in {cond}')
            cond2 += ')'