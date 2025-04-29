import tkinter as tk
from tkinter import scrolledtext
import asyncio
from core.extractor import extract_information_async

def analyze_and_display():
    name_address_text = name_address_input_area.get("1.0", tk.END).strip()
    birth_date_text = birth_date_input_area.get()
    ssn_text = ssn_input_area.get()

    extracted_info = asyncio.run(extract_information_async(name_address_text, birth_date_text, ssn_text))

    name_address_result_label.config(text=extracted_info['姓名地址'])
    birth_date_result_label.config(text=extracted_info['出生日期'])
    ssn_result_label.config(text=extracted_info['SSN'])

def run_analysis():
    analyze_and_display()

# 创建主窗口
root = tk.Tk()
root.title("信息提取小工具")

# 输入框
input_frame = tk.Frame(root)
input_frame.pack(padx=10, pady=5, fill="x")

name_address_label = tk.Label(input_frame, text="姓名地址邮编:")
name_address_label.grid(row=0, column=0, sticky="w")
name_address_input_area = scrolledtext.ScrolledText(input_frame, width=50, height=5)
name_address_input_area.grid(row=1, column=0, sticky="ew")

birth_date_label = tk.Label(input_frame, text="出生日期:")
birth_date_label.grid(row=2, column=0, sticky="w", pady=(5, 0))
birth_date_input_area = tk.Entry(input_frame, width=50)
birth_date_input_area.grid(row=3, column=0, sticky="ew")

ssn_label = tk.Label(input_frame, text="SSN:")
ssn_label.grid(row=4, column=0, sticky="w", pady=(5, 0))
ssn_input_area = tk.Entry(input_frame, width=50)
ssn_input_area.grid(row=5, column=0, sticky="ew")

# 分析按钮
analyze_button = tk.Button(root, text="分析", command=run_analysis)
analyze_button.pack(pady=10)

# 结果展示
result_frame = tk.Frame(root)
result_frame.pack(padx=10, pady=5, fill="x")

result_label = tk.Label(result_frame, text="分析结果:")
result_label.grid(row=0, column=0, sticky="w")

name_address_title_label = tk.Label(result_frame, text="姓名地址邮编:")
name_address_title_label.grid(row=1, column=0, sticky="w", padx=5)
name_address_result_label = tk.Label(result_frame, text="", anchor="w", justify="left")
name_address_result_label.grid(row=1, column=1, sticky="ew", padx=5)

birth_date_title_label = tk.Label(result_frame, text="出生日期:")
birth_date_title_label.grid(row=2, column=0, sticky="w", padx=5)
birth_date_result_label = tk.Label(result_frame, text="", anchor="w", justify="left")
birth_date_result_label.grid(row=2, column=1, sticky="ew", padx=5)

ssn_title_label = tk.Label(result_frame, text="SSN:")
ssn_title_label.grid(row=3, column=0, sticky="w", padx=5)
ssn_result_label = tk.Label(result_frame, text="", anchor="w", justify="left")
ssn_result_label.grid(row=3, column=1, sticky="ew", padx=5)

# 配置列的权重，使结果值可以扩展
result_frame.grid_columnconfigure(1, weight=1)

# 运行主循环
root.mainloop()