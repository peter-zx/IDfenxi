import re
import asyncio
from datetime import datetime
from dateutil.relativedelta import relativedelta
from mappings.us_states import us_state_abbreviations

async def extract_information(name_address: str = "", birth_date: str = "", ssn: str = "") -> dict:
    """
    异步解析姓名/地址、出生日期和 SSN。
    返回的字典包含以下键：
      - 名字
      - 姓氏
      - 州
      - 城市
      - 详细地址
      - 邮编
      - 出生日期
      - 英文出生日期
      - 年龄
      - SSN
    """
    data = {
        "名字": None,
        "姓氏": None,
        "州": None,
        "城市": None,
        "详细地址": None,
        "邮编": None,
        "出生日期": None,
        "英文出生日期": None,
        "年龄": None,
        "SSN": None
    }

    # 解析姓名与地址
    lines = [L.strip() for L in name_address.splitlines() if L.strip()]
    if lines:
        # 提取姓名
        name_line = lines[0]
        name_parts = name_line.split()
        if len(name_parts) >= 2:
            data["名字"] = name_parts[0]
            data["姓氏"] = name_parts[-1]
        elif len(name_parts) == 1:
            data["名字"] = name_parts[0]

        # 提取地址
        address_line = " ".join(lines[1:]) if len(lines) > 1 else ""
        if address_line:
            # 改进正则表达式，确保街道名和城市名正确分隔
            m_addr = re.search(
                r"(?P<street>\d+\s+[A-Za-z\s]+?)(?:,?\s*)(?P<city>[A-Za-z\s]+?),\s*(?P<state>[A-Z]{2})\s*(?P<zip>\d{5})?$",
                address_line
            )
            if m_addr:
                street = m_addr.group("street").strip()
                city = m_addr.group("city").strip()
                state = m_addr.group("state").upper()
                zip_code = m_addr.group("zip")

                # 后处理：清理城市名，确保不包含街道名
                street_words = street.split()[1:]  # 跳过数字部分（如“1252”）
                for word in street_words:
                    if word.lower() in city.lower():
                        city = city.replace(word, "").replace("  ", " ").strip()

                data["详细地址"] = street
                data["城市"] = city
                data["州"] = us_state_abbreviations.get(state, state)
                data["邮编"] = zip_code
            else:
                print("调试：地址解析失败，输入 =", address_line)

    # 解析出生日期 & 计算年龄
    bd = birth_date.strip()
    if bd:
        # 支持 "September 7, 2002" 或 "2002-09-07"
        m_bd = re.search(r"([A-Za-z]+\s+\d{1,2},\s*\d{4})|(\d{4}-\d{2}-\d{2})", bd)
        if m_bd:
            try:
                if m_bd.group(1):  # 格式如 "September 7, 2002"
                    dt = datetime.strptime(m_bd.group(1), "%B %d, %Y")
                else:  # 格式如 "2002-09-07"
                    dt = datetime.strptime(m_bd.group(2), "%Y-%m-%d")
                data["出生日期"] = dt.strftime("%Y-%m-%d")
                data["英文出生日期"] = dt.strftime("%B %d, %Y")
                current_date = datetime(2025, 4, 29)
                age = relativedelta(current_date, dt).years
                data["年龄"] = age
            except ValueError as e:
                print(f"调试：出生日期解析失败，错误 = {e}, 输入 = {bd}")
        else:
            # 支持仅年份，如 "2002"
            m_year = re.search(r"(\d{4})", bd)
            if m_year:
                y = int(m_year.group(1))
                data["出生日期"] = f"{y}-01-01"
                data["英文出生日期"] = f"January 01, {y}"
                current_date = datetime(2025, 4, 29)
                data["年龄"] = current_date.year - y
            else:
                print("调试：出生日期格式不匹配，输入 =", bd)

    # 提取 SSN
    s = ssn.strip()
    if s:
        # 支持 "XXX-XX-XXXX" 或 "XXXXXXXXX"
        m_ssn = re.search(r"(\d{3}-\d{2}-\d{4}|\d{9})", s)
        if m_ssn:
            data["SSN"] = m_ssn.group(0)
        else:
            print("调试：SSN 格式不匹配，输入 =", s)

    return data