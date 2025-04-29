import re
from datetime import datetime
from dateutil.relativedelta import relativedelta
import spacy
from mappings.us_states import us_state_abbreviations

# 加载 spacy 模型
nlp = spacy.load("en_core_web_sm")

def extract_information(name_address: str = "", birth_date: str = "", ssn: str = "") -> dict:
    """
    使用复合型分析方式解析姓名/地址、出生日期和 SSN。
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
        # 使用 spacy 解析姓名和地址
        doc = nlp(" ".join(lines))
        
        # 提取姓名（PERSON 实体）
        for ent in doc.ents:
            if ent.label_ == "PERSON" and not data["名字 (First Name)"]:
                name_parts = ent.text.split()
                if len(name_parts) >= 2:
                    data["名字 (First Name)"] = name_parts[0]
                    data["姓氏 (Last Name)"] = name_parts[-1]
                elif len(name_parts) == 1:
                    data["名字 (First Name)"] = name_parts[0]
                break

        # 提取地址（GPE 实体和规则匹配）
        address_line = " ".join(lines[1:]) if len(lines) > 1 else ""
        if address_line:
            doc = nlp(address_line)
            city = None
            state = None
            street = None
            
            # 提取城市和州（GPE 实体）
            for ent in doc.ents:
                if ent.label_ == "GPE":
                    # 州：检查是否为州缩写
                    if re.match(r"^[A-Z]{2}$", ent.text):
                        state = ent.text.upper()
                        data["州 (State)"] = us_state_abbreviations.get(state, state)
                    else:
                        # 城市：通常是 GPE 但不是州缩写
                        city = ent.text.strip()

            # 提取街道和 ZIP 码（规则匹配）
            m_addr = re.search(
                r"(?P<street>\d+\s+[A-Za-z\s]+?)\s*(?:,?\s*(?P<city>[A-Za-z\s]+?))?\s*,?\s*(?P<state>[A-Z]{2})?\s*(?P<zip>\d{5})?$",
                address_line
            )
            if m_addr:
                street = m_addr.group("street").strip()
                if not city and m_addr.group("city"):
                    city = m_addr.group("city").strip()
                if not state and m_addr.group("state"):
                    state = m_addr.group("state").upper()
                    data["州 (State)"] = us_state_abbreviations.get(state, state)

            # 后处理：清理城市名，确保不包含街道名
            if city and street:
                street_words = street.split()
                for word in street_words:
                    if word.lower() in city.lower():
                        city = city.replace(word, "").strip()
            
            data["详细地址 (Street Address)"] = street
            data["城市 (City)"] = city if city else None

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