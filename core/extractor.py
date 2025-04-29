import asyncio
import re

# 州份缩写到全称的映射
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

async def extract_information_async(text: str, manual_address: str = "") -> dict:
    """
    异步地从文本中提取信息，并处理手动输入的地址。
    """
    await asyncio.sleep(0.01)

    extracted_data = {
        "名字 (First Name)": None,
        "姓氏 (Last Name)": None,
        "详细地址 (Street Address)": None,
        "城市 (City)": None,
        "州 (State)": None,
        "SSN (社会安全号码)": None,
        "出生日期 (Date of Birth)": None
    }

    # 提取姓名
    name_match = re.search(r"([A-Za-z]+)\s+([A-Za-z.]+)", text)
    if name_match:
        extracted_data["名字 (First Name)"] = name_match.group(1).strip()
        extracted_data["姓氏 (Last Name)"] = name_match.group(2).strip()
    else:
        name_match_reversed = re.search(r"([A-Za-z.]+),\s+([A-Za-z]+)", text)
        if name_match_reversed:
            extracted_data["姓氏 (Last Name)"] = name_match_reversed.group(1).strip()
            extracted_data["名字 (First Name)"] = name_match_reversed.group(2).strip()
        else:
            name_match_single = re.search(r"^(Alice R\. Meli)", text, re.MULTILINE) # 针对特定姓名
            if name_match_single:
                parts = name_match_single.group(1).split()
                if len(parts) >= 2:
                    extracted_data["名字 (First Name)"] = parts[0].strip()
                    extracted_data["姓氏 (Last Name)"] = " ".join(parts[1:]).strip()

    # 处理手动输入的地址
    if manual_address:
        address_parts = manual_address.split(',')
        if len(address_parts) >= 2:
            street_address = address_parts[0].strip()
            city_state_zip = address_parts[1].strip().split()
            if len(city_state_zip) >= 2:
                city = city_state_zip[0].strip()
                state_abbrev = city_state_zip[1].strip()
                extracted_data["详细地址 (Street Address)"] = street_address
                extracted_data["城市 (City)"] = city
                extracted_data["州 (State)"] = state_abbreviations.get(state_abbrev.upper(), state_abbrev) # 尝试补全州名

    # 提取 SSN
    ssn_matches = re.findall(r"(?:SSN|Social Security Number)?\s*(\d{3}-\d{2}-\d{4}|\d{9})", text)
    if ssn_matches:
        extracted_data["SSN (社会安全号码)"] = ssn_matches[0]

    # 提取出生日期
    birthday_match = re.search(r"(?:Birthday)?\s*([A-Za-z]+\s+\d{1,2},\s+\d{4})", text)
    if birthday_match:
        extracted_data["出生日期 (Date of Birth)"] = birthday_match.group(1).strip()
    else:
        birthday_match_alt = re.search(r"(?:Birthday)?\s*([A-Za-z]+\s+\d{1,2},\s+\d{2,4})", text)
        if birthday_match_alt:
            extracted_data["出生日期 (Date of Birth)"] = birthday_match_alt.group(1).strip()

    return extracted_data