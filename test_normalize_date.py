import pytest

from normalize_date import normalize_date

def test_full_date():
    assert normalize_date("2026年12月3日") == "2026-12-03"

def test_slash():
    assert normalize_date("2026/12/3") == "2026-12-03"

def test_zero_padding():
    assert normalize_date("2026-1-5") == "2026-01-05"

def test_invalid():
    assert normalize_date("未定") is None


# --- 追加テスト ---

@pytest.mark.parametrize("text, expected", [
    # 各区切り文字で 1 桁の月日をゼロ埋め
    ("2026年1月5日", "2026-01-05"),
    ("2026/1/5", "2026-01-05"),
    ("2026-1-5", "2026-01-05"),
    ("2026.1.5", "2026-01-05"),
    # すでにゼロ埋め済み
    ("2026年01月05日", "2026-01-05"),
    ("2026/01/05", "2026-01-05"),
    ("2026-01-05", "2026-01-05"),
    # 「日」を省略した和文表記
    ("2026年12月3", "2026-12-03"),
    # 年末年始の境界
    ("2026/12/31", "2026-12-31"),
    ("2027/1/1", "2027-01-01"),
])
def test_valid_formats(text, expected):
    assert normalize_date(text) == expected


@pytest.mark.parametrize("text, expected", [
    ("  2026/12/3  ", "2026-12-03"),
    ("\t2026-1-5\n", "2026-01-05"),
    ("2026 年 12 月 3 日", "2026-12-03"),
])
def test_surrounding_whitespace(text, expected):
    assert normalize_date(text) == expected


@pytest.mark.parametrize("text, expected", [
    ("2024/2/29", "2024-02-29"),  # 4 で割り切れる年はうるう年
    ("2000/2/29", "2000-02-29"),  # 400 で割り切れる年はうるう年
])
def test_leap_year_valid(text, expected):
    assert normalize_date(text) == expected


@pytest.mark.parametrize("text", [
    "2026/2/29",   # うるう年ではない
    "1900/2/29",   # 100 で割り切れて 400 で割り切れない年はうるう年ではない
    "2026/2/30",   # 2 月 30 日は存在しない
    "2026/4/31",   # 4 月は 30 日まで
    "2026/13/1",   # 13 月は存在しない
    "2026/0/1",    # 0 月は存在しない
    "2026/1/0",    # 0 日は存在しない
    "2026/1/32",   # 32 日は存在しない
])
def test_nonexistent_dates(text):
    assert normalize_date(text) is None


@pytest.mark.parametrize("text", [
    "",               # 空文字
    "   ",            # 空白のみ
    "未定",
    "TBD",
    "2026/12",        # 日が欠けている
    "2026年12月",     # 日が欠けている（和文）
    "12/3",           # 年が欠けている
    "26/12/3",        # 2 桁の年
    "2026/123/1",     # 3 桁の月
    "2026/12/3/4",    # 要素が多すぎる
    "2026/12/3 10:00",  # 時刻付き
    "2026/12/3です",  # 末尾に余計な文字
    "締切は2026/12/3",  # 先頭に余計な文字
    "abcd/ef/gh",     # 数字ではない
])
def test_invalid_strings(text):
    assert normalize_date(text) is None


@pytest.mark.parametrize("value", [None, 20261203, 2026.12, ["2026/12/3"]])
def test_non_string_input(value):
    assert normalize_date(value) is None
