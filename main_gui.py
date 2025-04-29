import tkinter as tk
from tkinter import scrolledtext
import asyncio
from core.extractor import extract_information_async

def analyze_and_display():
    """
    获取输入框中的文本，调用信息提取函数，并在结果标签中显示提取的信息。
    """
    name_address_text = name_address_input_area.get("1.0", tk.END).strip()
    birth_date_text = birth_date_input_area.get().strip()
    ssn_text = ssn_input_area.get().strip()

    # 调用异步信息提取函数
    extracted_info = asyncio.run(extract_information_async(name_address_text, birth_date_text, ssn_text))

    # 更新结果标签的文本
    first_name_result_label.config(text=extracted_info.get("名字 (First Name)", "N/A"))
    last_name_result_label.config(text=extracted_info.get("姓氏 (Last Name)", "N/A"))
    state_result_label.config(text=extracted_info.get("州 (State)", "N/A"))
    city_result_label.config(text=extracted_info.get("城市 (City)", "N/A"))
    street_address_result_label.config(text=extracted_info.get("详细地址 (Street Address)", "N/A"))
    birth_date_result_label.config(text=extracted_info.get("出生日期", "N/A"))
    age_result_label.config(text=extracted_info.get("年龄", "N/A"))
    ssn_result_label.config(text=extracted_info.get("SSN", "N/A"))

def run_analysis():
    """
    点击分析按钮时调用的函数。
    """
    analyze_and_display()

# 创建主窗口
root = tk.Tk()
root.title("信息提取小工具")

# 输入框框架
input_frame = tk.Frame(root)
input_frame.pack(padx=10, pady=5, fill="x")

# 姓名地址邮编输入框
name_address_label = tk.Label(input_frame, text="姓名地址邮编:")
name_address_label.grid(row=0, column=0, sticky="w")
name_address_input_area = scrolledtext.ScrolledText(input_frame, width=50, height=5)
name_address_input_area.grid(row=1, column=0, sticky="ew")

# 出生日期输入框
birth_date_label = tk.Label(input_frame, text="出生日期 (Month Day, Year):")
birth_date_label.grid(row=2, column=0, sticky="w", pady=(5, 0))
birth_date_input_area = tk.Entry(input_frame, width=50)
birth_date_input_area.grid(row=3, column=0, sticky="ew")

# SSN 输入框
ssn_label = tk.Label(input_frame, text="SSN (XXX-XX-XXXX 或 XXXXXXXXX):")
ssn_label.grid(row=4, column=0, sticky="w", pady=(5, 0))
ssn_input_area = tk.Entry(input_frame, width=50)
ssn_input_area.grid(row=5, column=0, sticky="ew")

# 分析按钮
analyze_button = tk.Button(root, text="分析", command=run_analysis)
analyze_button.pack(pady=10)

# 结果展示框架
result_frame = tk.Frame(root)
result_frame.pack(padx=10, pady=5, fill="x")

result_label = tk.Label(result_frame, text="分析结果:")
result_label.grid(row=0, column=0, sticky="w")

# 结果标签
tk.Label(result_frame, text="名字 (First Name):").grid(row=1, column=0, sticky="w", padx=5)
first_name_result_label = tk.Label(result_frame, text="", anchor="w", justify="left")
first_name_result_label.grid(row=1, column=1, sticky="ew", padx=5)

tk.Label(result_frame, text="姓氏 (Last Name):").grid(row=2, column=0, sticky="w", padx=5)
last_name_result_label = tk.Label(result_frame, text="", anchor="w", justify="left")
last_name_result_label.grid(row=2, column=1, sticky="ew", padx=5)

tk.Label(result_frame, text="州 (State):").grid(row=3, column=0, sticky="w", padx=5)
state_result_label = tk.Label(result_frame, text="", anchor="w", justify="left")
state_result_label.grid(row=3, column=1, sticky="ew", padx=5)

tk.Label(result_frame, text="城市 (City):").grid(row=4, column=0, sticky="w", padx=5)
city_result_label = tk.Label(result_frame, text="", anchor="w", justify="left")
city_result_label.grid(row=4, column=1, sticky="ew", padx=5)

tk.Label(result_frame, text="详细地址 (Street Address):").grid(row=5, column=0, sticky="w", padx=5)
street_address_result_label = tk.Label(result_frame, text="", anchor="w", justify="left")
street_address_result_label.grid(row=5, column=1, sticky="ew", padx=5)

tk.Label(result_frame, text="出生日期:").grid(row=6, column=0, sticky="w", padx=5, pady=(5, 0))
birth_date_result_label = tk.Label(result_frame, text="", anchor="w", justify="left")
birth_date_result_label.grid(row=6, column=1, sticky="ew", padx=5, pady=(5, 0))

tk.Label(result_frame, text="年龄:").grid(row=7, column=0, sticky="w", padx=5)
age_result_label = tk.Label(result_frame, text="", anchor="w", justify="left")
age_result_label.grid(row=7, column=1, sticky="ew", padx=5)

tk.Label(result_frame, text="SSN:").grid(row=8, column=0, sticky="w", padx=5, pady=(5, 0))
ssn_result_label = tk.Label(result_frame, text="", anchor="w", justify="left")
ssn_result_label.grid(row=8, column=1, sticky="ew", padx=5, pady=(5, 0))

# 配置结果框架的列权重，使结果值可以水平扩展
result_frame.grid_columnconfigure(1, weight=1)

# 运行主循环
root.mainloop()
