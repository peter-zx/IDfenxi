import tkinter as tk
from tkinter import scrolledtext
import asyncio
from core.extractor import extract_information_async

def analyze_and_display():
    name_address_text = name_address_input_area.get("1.0", tk.END).strip()
    birth_date_text = birth_date_input_area.get().strip()
    ssn_text = ssn_input_area.get().strip()

    extracted_info = asyncio.run(extract_information_async(name_address_text, birth_date_text, ssn_text))

    # 清空结果文本框
    result_text_area.delete("1.0", tk.END)

    # 插入格式化的结果
    result_text_area.insert(tk.END, f"名字 (First Name):\t{extracted_info.get('名字 (First Name)', 'N/A')}\n")
    result_text_area.insert(tk.END, f"姓氏 (Last Name):\t{extracted_info.get('姓氏 (Last Name)', 'N/A')}\n")
    result_text_area.insert(tk.END, f"州 (State):\t\t{extracted_info.get('州 (State)', 'N/A')}\n")
    result_text_area.insert(tk.END, f"城市 (City):\t\t{extracted_info.get('城市 (City)', 'N/A')}\n")
    result_text_area.insert(tk.END, f"详细地址 (Street Address):\t{extracted_info.get('详细地址 (Street Address)', 'N/A')}\n")
    result_text_area.insert(tk.END, f"出生日期:\t\t{extracted_info.get('出生日期', 'N/A')}\n")
    result_text_area.insert(tk.END, f"年龄:\t\t\t{extracted_info.get('年龄', 'N/A')}\n")
    result_text_area.insert(tk.END, f"SSN:\t\t\t{extracted_info.get('SSN', 'N/A')}\n")

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

birth_date_label = tk.Label(input_frame, text="出生日期 (Month Day, Year):")
birth_date_label.grid(row=2, column=0, sticky="w", pady=(5, 0))
birth_date_input_area = tk.Entry(input_frame, width=50)
birth_date_input_area.grid(row=3, column=0, sticky="ew")

ssn_label = tk.Label(input_frame, text="SSN (XXX-XX-XXXX 或 XXXXXXXXX):")
ssn_label.grid(row=4, column=0, sticky="w", pady=(5, 0))
ssn_input_area = tk.Entry(input_frame, width=50)
ssn_input_area.grid(row=5, column=0, sticky="ew")

# 分析按钮
analyze_button = tk.Button(root, text="分析", command=run_analysis)
analyze_button.pack(pady=10)

# 结果展示
result_label = tk.Label(root, text="分析结果:")
result_label.pack(pady=5)

result_text_area = scrolledtext.ScrolledText(root, width=50, height=10)
result_text_area.pack(padx=10, pady=5, fill="both", expand=True)

# 运行主循环
root.mainloop()