import asyncio
import re

async def extract_information_async(text: str) -> dict:
    """
    异步地从文本中提取姓名、地址、SSN 和出生日期。
    """
    await asyncio.sleep(0.01)  # 模拟一个小的异步操作

    extracted_data = {
        "姓名 (Name)": None,
        "详细地址 (Address)": None,
        "SSN (社会安全号码)": None,
        "出生日期 (Date of Birth)": None
    }

    name_match = re.search(r"^(.*)\n", text)
    if name_match:
        extracted_data["姓名 (Name)"] = name_match.group(1).strip()

    address_match = re.search(r"(\d+ [^\n]+\n[^\n]+, [A-Z]{2} \d{5})", text)
    if address_match:
        extracted_data["详细地址 (Address)"] = address_match.group(1).strip()

    ssn_match = re.search(r"(?:SSN|Social Security Number)\s*(\d{3}-\d{2}-\d{4}|\d{9})", text)
    if ssn_match:
        extracted_data["SSN (社会安全号码)"] = ssn_match.group(1)

    birthday_match = re.search(r"Birthday\s*(.*?)(?:\n|Age)", text)
    if birthday_match:
        extracted_data["出生日期 (Date of Birth)"] = birthday_match.group(1).strip()

    return extracted_data