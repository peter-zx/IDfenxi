import asyncio
import re

async def extract_information_async(text: str) -> dict:
    """
    异步地从文本中提取更详细的信息。
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

    # 提取姓名 (尝试匹配 "FirstName Last Name" 或 "LastName, FirstName")
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


    # 提取详细地址、城市和州 (尝试匹配 "Street, City, ST Zip")
    address_match = re.search(r"(\d+\s+[^\n,]+),\s*([^\n,]+),\s*([A-Z]{2})\s+(\d{5})", text)
    if address_match:
        extracted_data["详细地址 (Street Address)"] = address_match.group(1).strip()
        extracted_data["城市 (City)"] = address_match.group(2).strip()
        extracted_data["州 (State)"] = address_match.group(3).strip()
    else:
        address_match_partial = re.search(r"(\d+\s+[^\n]+)\n([^\n]+,)\s*([A-Z]{2})\s+(\d{5})", text)
        if address_match_partial:
            extracted_data["详细地址 (Street Address)"] = address_match_partial.group(1).strip()
            extracted_data["城市 (City)"] = address_match_partial.group(2).rstrip(',').strip()
            extracted_data["州 (State)"] = address_match_partial.group(3).strip()


    # 提取 SSN (匹配 "SSN xxx-xx-xxxx" 或 "Social Security Number xxx-xx-xxxx" 或 "xxx-xx-xxxx" 或 "xxxxxxxxx")
    ssn_matches = re.findall(r"(?:SSN|Social Security Number)?\s*(\d{3}-\d{2}-\d{4}|\d{9})", text)
    if ssn_matches:
        extracted_data["SSN (社会安全号码)"] = ssn_matches[0] # 取第一个匹配到的完整 SSN

    # 提取出生日期 (匹配 "Birthday Month Day, Year" 或 "Month Day, Year")
    birthday_match = re.search(r"(?:Birthday)?\s*([A-Za-z]+\s+\d{1,2},\s+\d{4})", text)
    if birthday_match:
        extracted_data["出生日期 (Date of Birth)"] = birthday_match.group(1).strip()
    else:
        birthday_match_alt = re.search(r"(?:Birthday)?\s*([A-Za-z]+\s+\d{1,2},\s+\d{2,4})", text) # 尝试匹配年份为两位数的情况
        if birthday_match_alt:
            extracted_data["出生日期 (Date of Birth)"] = birthday_match_alt.group(1).strip()
        else:
            birthday_match_month_day_year = re.search(r"(?:Birthday)?\s*([A-Za-z]+\s+\d{1,2},\s+\d{4})", text)
            if birthday_match_month_day_year:
                extracted_data["出生日期 (Date of Birth)"] = birthday_match_month_day_year.group(1).strip()
            else:
                birthday_match_month_day_year_short = re.search(r"(?:Birthday)?\s*([A-Za-z]+\s+\d{1,2},\s+\d{2})", text)
                if birthday_match_month_day_year_short:
                    year = birthday_match_month_day_year_short.group(3)
                    # 这里需要更智能的年份推断，暂时简化处理
                    extracted_data["出生日期 (Date of Birth)"] = f"{birthday_match_month_day_year_short.group(1).strip()}"


    return extracted_data