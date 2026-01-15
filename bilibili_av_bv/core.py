import re

# Bilibili AV/BV 转换参数
_XOR = 2275242641476827
_TABLE = "FcwAPNKTMug3GV5Lj7EJnHpWsx4tb8haYeviqBz6rkCy12mUSDQX9RdoZf"
_POS = [8, 7, 0, 5, 1, 3, 2, 4, 6]


def _av_to_bv(av: int) -> str:
    """将 AV 号转为 BV 号"""
    if av <= 0:
        raise ValueError("AV号必须为正整数")
    bv_num = av ^ _XOR
    s = [''] * 9
    for p in _POS:
        s[p] = _TABLE[bv_num % 58]
        bv_num //= 58
    return 'BV1' + ''.join(s)


def _bv_to_av(bv: str) -> int:
    """将 BV 号转为 AV 号"""
    if not bv.startswith('BV1') or len(bv) != 12:
        raise ValueError("无效的 BV 号格式")
    bv = bv[3:]  # 去掉 'BV1'
    num = 0
    for i, p in enumerate(_POS):
        char = bv[p]
        if char not in _TABLE:
            raise ValueError(f"非法字符 '{char}' 在 BV 号中")
        idx = _TABLE.index(char)
        num += idx * (58**i)
    av = num ^ _XOR
    return av


def convert(text: str) -> str:
    """
    自动识别并转换文本中的 av/BV 号：
    - av12345 → BV1xxxxxx
    - BV1xxxxxx → av12345
    保留其他内容不变。
    """

    def replacer(match):
        full = match.group(0)
        prefix = full[:2].lower()
        body = full[2:]

        try:
            if prefix == 'av':
                av_id = int(body)
                if av_id <= 0:
                    return full  # 无效 AV 号，原样返回
                bv = _av_to_bv(av_id)
                # 验证可逆性（可选，增强鲁棒性）
                if _bv_to_av(bv) == av_id:
                    return bv
                else:
                    return full
            elif prefix == 'bv':
                bv_id = full
                av_id = _bv_to_av(bv_id)
                if av_id > 0 and _av_to_bv(av_id) == bv_id:
                    return f'av{av_id}'
                else:
                    return full
            else:
                return full
        except Exception:
            # 任何解析/转换错误都返回原文，避免崩溃
            return full

    # 匹配 av\d+ 或 BV1[1-9A-Za-z]{9}（不区分大小写）
    pattern = r'\b(?:av\d+|BV1[1-9A-Za-z]{9})\b'
    result = re.sub(pattern, replacer, text, flags=re.IGNORECASE)
    return result


if __name__ == '__main__':
    pass
