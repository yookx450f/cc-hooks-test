import re
from datetime import date

_PATTERN = re.compile(r"^\s*(\d{4})\s*[年/\-.]\s*(\d{1,2})\s*[月/\-.]\s*(\d{1,2})\s*日?\s*$")


def normalize_date(text):
    """日付文字列を YYYY-MM-DD 形式に正規化する。解釈できなければ None を返す。"""
    if not isinstance(text, str):
        return None
    m = _PATTERN.match(text)
    if not m:
        return None
    try:
        d = date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    except ValueError:
        return None
    return d.isoformat()
