import tkinter as tk
from tkinter import scrolledtext
import asyncio
from core.extractor import extract_information_async

def analyze_and_display():
    name_address_text = name_address_input_area.get("1.0", tk.END).strip()
    birth_date_text = birth_date_input_area.get()
    ssn_text = ssn_input_area.get()

    extracted_info = asyncio.run(extract_information_async(name_address_text, birth_date_text, ssn_text))

    name_address_result_label.config(text=f"姓名地址: {extracted_info['姓名地址']}")
    birth_date_result_label.config(text=f"出生日期: {extracted_info['出生日期']}")
    ssn_result_label.config(text=f"SSN: {extracted_info['SSN']}")

def run_analysis():
    analyze_and_display()

# 创建主窗口
root = tk.Tk()
root.title("信息提取小工具")

# 输入框 1: 姓名地址邮编
name_address_label = tk.Label(root, text="姓名地址邮编:")
name_address_label.pack(pady=5)
name_address_input_area = scrolledtext.ScrolledText(root, width=50, height=5)
name_address_input_area.pack(padx=10, pady=5)

# 输入框 2: 出生日期
birth_date_label = tk.Label(root, text="出生日期:")
birth_date_label.pack(pady=5)
birth_date_input_area = tk.Entry(root, width=50)
birth_date_input_area.pack(padx=10, pady=5)

# 输入框 3: SSN
ssn_label = tk.Label(root, text="SSN:")
ssn_label.pack(pady=5)
ssn_input_area = tk.Entry(root, width=50)
ssn_input_area.pack(padx=10, pady=5)

# 分析按钮
analyze_button = tk.Button(root, text="分析", command=run_analysis)
analyze_button.pack(pady=10)

# 结果展示标签
result_label = tk.Label(root, text="分析结果:")
result_label.pack(pady=5)

name_address_result_label = tk.Label(root, text="姓名地址: ")
name_address_result_label.pack(padx=10, pady=2, anchor="w")

birth_date_result_label = tk.Label(root, text="出生日期: ")
birth_date_result_label.pack(padx=10, pady=2, anchor="w")

ssn_result_label = tk.Label(root, text="SSN: ")
ssn_result_label.pack(padx=10, pady=2, anchor="w")

# 运行主循环
root.mainloop()