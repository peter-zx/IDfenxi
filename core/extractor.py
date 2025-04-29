import asyncio
import re
from datetime import datetime
from dateutil.relativedelta import relativedelta

# 州份缩写到全称的映射 (保持不变)
state_abbreviations = {
    "AL": "Alabama", "AK": "Alaska", "AZ": "Arizona", "AR": "Arkansas", "CA": "California",
    "CO": "Colorado", "CT": "Connecticut", "DE": "Delaware", "DC": "District of Columbia",
    "FL": "Florida", "GA": "Georgia", "HI": "Hawaii", "ID": "Idaho", "IL": "Illinois",
    "IN": "Indiana", "IA": "Iowa", "KS": "Kansas", "KY": "Kentucky", "LA": "Louisiana",
    "ME": "Maine", "MD": "Maryland", "MA": "Massachusetts", "MI": "Michigan",
    "MN": "Minnesota", "MS": "Mississippi", "MO": "Missouri", "MT": "Montana",
    "NE": "Nebraska", "NV": "Nevada", "NH": "New Hampshire", "NJ": "New Jersey",
    "NM": "New Mexico", "NY": "New York", "NC": "North Carolina", "ND": "North Dakota",
    "OH": "Ohio", "OK": "Oklahoma", "OR": "Oregon", "PA": "Pennsylvania",
    "RI": "Rhode Island", "SC": "South Carolina", "SD": "South Dakota", "TN": "Tennessee",
    "TX": "Texas", "UT": "Utah", "VT": "Vermont", "VA": "Virginia", "WA": "Washington",
    "WV": "West Virginia", "WI": "Wisconsin", "WY": "Wyoming"
}

async def extract_information_async(name_address: str = "", birth_date: str = "", ssn: str = "") -> dict:
    """
    异步地解析姓名地址、出生日期和 SSN。
    """
    await asyncio.sleep(0.01)

    extracted_data = {
        "名字 (First Name)": None,
        "姓氏 (Last Name)": None,
        "州 (State)": None,
        "城市 (City)": None,
        "详细地址 (Street Address)": None,
        "出生日期": None,
        "年龄": None,
        "SSN": None
    }

    # 解析姓名地址
    name_address_lines = [line.strip() for line in name_address.split('\n')]
    if name_address_lines:
        # 尝试提取姓名 (假设第一行是姓名)
        name_match = re.search(r"^(?P<first>\w+)\s+(?P<middle>[A-Z]\.\s*)?(?P<last>\w+)", name_address_lines[0])
        if name_match:
            extracted_data["名字 (First Name)"] = name_match.group("first")
            extracted_data["姓氏 (Last Name)"] = name_match.group("last")
        elif len(name_address_lines[0].split()) == 2: # 尝试简单空格分隔的名字
            parts = name_address_lines[0].split()
            extracted_data["名字 (First Name)"] = parts[0]
            extracted_data["姓氏 (Last Name)"] = parts[1]

        # 尝试提取地址 (假设剩余行包含地址信息)
        if len(name_address_lines) >= 2:
            address_part = " ".join(name_address_lines[1:])
            address_match = re.search(r"^(?P<street>[\d]+\s+[\w\s]+)\s*(?P<city>[\w\s]+),\s*(?P<state>[A-Z]{2})\s*(?P<zip>\d{5})", address_part)
            if address_match:
                extracted_data["详细地址 (Street Address)"] = address_match.group("street").strip()
                extracted_data["城市 (City)"] = address_match.group("city").strip()
                extracted_data["州 (State)"] = state_abbreviations.get(address_match.group("state").upper(), address_match.group("state"))

    # 解析出生日期和计算年龄
    birth_date = birth_date.strip()
    date_match = re.search(r"([A-Za-z]+\s*\d{1,2},\s*\d{4})", birth_date)
    if date_match:
        try:
            birth_date_obj = datetime.strptime(date_match.group(1), "%B %d, %Y")
            extracted_data["出生日期"] = birth_date_obj.strftime("%Y-%m-%d")
            today = datetime.now()
            age = relativedelta(today, birth_date_obj).years
            extracted_data["年龄"] = age
        except ValueError:
            pass
    elif re.search(r"(\d{4})", birth_date): # 尝试只提取年份
        year_match = re.search(r"(\d{4})", birth_date)
        try:
            birth_year = int(year_match.group(1))
            extracted_data["出生日期"] = f"{birth_year}-01-01" # 仅供参考
            extracted_data["年龄"] = datetime.now().year - birth_year
        except ValueError:
            pass

    # 提取 SSN
    ssn = ssn.strip()
    ssn_match = re.search(r"(\d{3}-\d{2}-\d{4})", ssn)
    if ssn_match:
        extracted_data["SSN"] = ssn_match.group(1)
    elif re.search(r"(\d{9})", ssn):
        extracted_data["SSN"] = re.search(r"(\d{9})", ssn).group(1)

    return extracted_data