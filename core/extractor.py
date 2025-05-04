import re
from datetime import datetime
from dateutil import parser
from dateutil.relativedelta import relativedelta

from mappings.us_states import US_STATES

async def extract_information(name_address, birth_date, ssn):
    info_list = []
    
    if not name_address:
        return info_list

    # 分割多组数据
    groups = name_address.strip().split('\n\n')
    
    for group in groups:
        info = {
            "名字": None,
            "姓氏": None,
            "州": None,
            "城市": None,
            "详细地址": None,
            "邮编": None,
            "出生日期": None,
            "英文出生日期": None,
            "年龄": None,
            "SSN": None,
        }
        
        lines = group.strip().split('\n')
        if not lines:
            continue
            
        # 提取姓名
        name = lines[0].strip()
        name_parts = name.split()
        if len(name_parts) >= 2:
            info["名字"] = name_parts[0]
            info["姓氏"] = name_parts[-1]
        else:
            info["名字"] = name

        # 提取地址相关信息
        if len(lines) > 1:
            address_line = lines[1].strip()
            info["详细地址"] = address_line

            # 提取城市、州和邮编
            city_state_zip = lines[2].strip() if len(lines) > 2 else address_line

            # 匹配城市、州和邮编
            city_state_zip_match = re.match(r'^(.*?),\s*([A-Za-z\s]+)\s*(\d{5})$', city_state_zip)
            if city_state_zip_match:
                info["城市"] = city_state_zip_match.group(1).strip()
                state_input = city_state_zip_match.group(2).strip()
                info["邮编"] = city_state_zip_match.group(3)

                # 查找州的全称
                for state_abbr, state_full in US_STATES.items():
                    if state_input.lower() in (state_abbr.lower(), state_full.lower()):
                        info["州"] = state_full
                        break
            else:
                # 如果没有邮编，尝试单独匹配城市和州
                city_state_match = re.match(r'^(.*?),\s*([A-Za-z\s]+)$', city_state_zip)
                if city_state_match:
                    info["城市"] = city_state_match.group(1).strip()
                    state_input = city_state_match.group(2).strip()
                    for state_abbr, state_full in US_STATES.items():
                        if state_input.lower() in (state_abbr.lower(), state_full.lower()):
                            info["州"] = state_full
                            break

        # 解析出生日期
        if birth_date:
            try:
                parsed_date = parser.parse(birth_date, fuzzy=True)
                info["出生日期"] = parsed_date.strftime("%Y-%m-%d")
                info["英文出生日期"] = parsed_date.strftime("%B %d, %Y")

                # 计算年龄
                today = datetime.today()
                age = relativedelta(today, parsed_date).years
                info["年龄"] = age
            except ValueError:
                pass

        # 解析 SSN
        if ssn:
            ssn_cleaned = ssn.strip()
            ssn_match = re.match(r'^\d{3}-\d{2}-\d{4}$', ssn_cleaned)
            if ssn_match:
                info["SSN"] = ssn_cleaned.replace("-", "")
            else:
                info["SSN"] = ssn_cleaned

        if any(info.values()):
            info_list.append(info)
    
    return info_list