# 左侧栏目的步骤和链接配置
# 格式：每个步骤是一个字典，包含 "name"（步骤名称）和 "url"（链接地址）
STEPS = [
    {"name": "角色信息", "url": "https://www.fakenamegenerator.com/advanced.php"},
    {"name": "SSN", "url": "https://www.fakexy.com"},
    {"name": "sms接码", "url": "https://temp-number.com"},
]

# 备注信息
REMARK = "备注：注意网络环境设置为规则国际网络"


# 如何添加新按钮和链接
# 1. 编辑 ui/links_config.py
# 打开 ui/links_config.py 文件。
# 在 STEPS 列表中添加一个新字典，包含 name（步骤名称）和 url（链接地址）。

# STEPS = [
#     {"name": "角色信息", "url": "https://www.fakenamegenerator.com/advanced.php"},
#     {"name": "SSN", "url": "https://www.fakexy.com"},
#     {"name": "sms接码", "url": "https://temp-number.com"},
#     {"name": "邮箱生成", "url": "https://example.com/email"},  # 新增步骤
# ]