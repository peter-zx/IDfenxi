import asyncio

async def extract_information_async(name_address: str = "", birth_date: str = "", ssn: str = "") -> dict:
    """
    异步地接收各个字段的输入，并直接返回。
    """
    await asyncio.sleep(0.01)

    extracted_data = {
        "姓名地址": name_address.strip(),
        "出生日期": birth_date.strip(),
        "SSN": ssn.strip()
    }
    return extracted_data