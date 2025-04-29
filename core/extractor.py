import re
from datetime import datetime
from dateutil.relativedelta import relativedelta
from mappings.us_states import us_state_abbreviations

def extract_information(name_address: str = "", birth_date: str = "", ssn: str = "") -> dict:
    """
    同步地解析姓名/地址、出生日期和 SSN。
    返回的字典包含以下键：
      - 名字 (First Name)
      - 姓氏 (Last Name)
      - 州 (State)
      - 城市 (City)
      - 详细地址 (Street Address)
      - 出生日期
      - 年龄
      - SSN
    """
    data = {
        "名字 (First Name)": None,
        "姓氏 (Last Name)": None,
        "州 (State)": None,
        "城市 (City)": None,
        "详细地址 (Street Address)": None,
        "出生日期": None,
        "年龄": None,
        "SSN": None
    }

    # 解析姓名与地址
    lines = [L.strip() for L in name_address.splitlines() if L.strip()]
    if lines:
        # 姓名：支持 "First Last" 或 "First Middle Last"
        m_name = re.match(r"^(?P<first>[A-Za-z]+)\s+(?P<middle>[A-Z]\.)?\s*(?P<last>[A-Za-z]+)", lines[0])
        if m_name:
            data["名字 (First Name)"] = m_name.group("first")
            data["姓氏 (Last Name)"] = m_name.group("last")
        else:
            print("调试：姓名解析失败，输入 =", lines[0])

        if len(lines) >= 2:
            addr = " ".join(lines[1:])
            # 地址：支持多种格式，如 "123 Main St, Springfield, IL 62701" 或 "123 Main St Springfield IL 62701"
            m_addr = re.search(
                r"(?P<street>\d+\s+[\w\s]+?)\s*,?\s*"
                r"(?P<city>[\w\s]+?)\s*,?\s*(?P<state>[A-Z]{2})\s*(?P<zip>\d{5})?",
                addr
            )
            if m_addr:
                data["详细地址 (Street Address)"] = m_addr.group("street").strip()
                data["城市 (City)"] = m_addr.group("city").strip()
                st = m_addr.group("state").upper()
                data["州 (State)"] = us_state_abbreviations.get(st, st)
            else:
                print("调试：地址解析失败，输入 =", addr)

    # 解析出生日期 & 计算年龄
    bd = birth_date.strip()
    if bd:
        # 支持 "September 7, 2002" 或 "2002-09-07"
        m_bd = re.search(r"([A-Za получай_z]+\s+\d{1,2},\s*\d{4})|(\d{4}-\d{2}-\d{2})", bd)
        if m_bd:
            try:
                if m_bd.group(1):  # 格式如 "September 7, 2002"
                    dt = datetime.strptime(m_bd.group(1), "%B %d, %Y")
                else:  # 格式如 "2002-09-07"
                    dt = datetime.strptime(m_bd.group(2), "%Y-%m-%d")
                data["出生日期"] = dt.strftime("%Y-%m-%d")
                data["年龄"] = relativedelta(datetime.now(), dt).years
            except ValueError as e:
                print(f"调试：出生日期解析失败，错误 = {e}, 输入 = {bd}")
        else:
            # 支持仅年份，如 "2002"
            m_year = re.search(r"(\d{4})", bd)
            if m_year:
                y = int(m_year.group(1))
                data["出生日期"] = f"{y}-01-01"
                data["年龄"] = datetime.now().year - y
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