import re
from datetime import date

# 和文表記: 2026年12月3日（「日」は省略可、各要素間の空白は許容）
_JP = re.compile(r"([0-9]{4})\s*年\s*([0-9]{1,2})\s*月\s*([0-9]{1,2})\s*日?")
# 区切り文字表記: 2026/12/3, 2026-12-3, 2026.12.3（区切り文字は統一されている必要あり）
_SEP = re.compile(r"([0-9]{4})([/\-.])([0-9]{1,2})\2([0-9]{1,2})")


def normalize_date(text):
    """日付文字列を YYYY-MM-DD 形式に正規化する。解釈できなければ None を返す。"""
    if not isinstance(text, str):
        return None
    s = text.strip()

    m = _JP.fullmatch(s)
    if m:
        y, mo, d = m.group(1), m.group(2), m.group(3)
    else:
        m = _SEP.fullmatch(s)
        if not m:
            return None
        y, mo, d = m.group(1), m.group(3), m.group(4)

    try:
        return date(int(y), int(mo), int(d)).isoformat()
    except ValueError:
        return None
