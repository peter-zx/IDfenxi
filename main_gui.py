import tkinter as tk
from tkinter import scrolledtext, ttk
import asyncio
from core.extractor import extract_information_async
from tkinter import font

def analyze_and_display():
    name_address_text = name_address_input_area.get("1.0", tk.END).strip()
    birth_date_text = birth_date_input_area.get().strip()
    ssn_text = ssn_input_area.get().strip()

    extracted_info = asyncio.run(extract_information_async(name_address_text, birth_date_text, ssn_text))

    # 清空结果文本框
    for widget in result_frame.winfo_children():
        widget.destroy()

    # 设置结果标题样式
    result_title_font = font.Font(size=14, weight="bold")
    tk.Label(result_frame, text="分析结果", font=result_title_font).grid(row=0, column=0, columnspan=2, sticky="w", pady=(5, 10))

    # 设置字段标题样式
    field_title_font = font.Font(weight="bold")

    # 结果字段和值
    fields = [
        ("名字 (First Name):", extracted_info.get("名字 (First Name)", "N/A")),
        ("姓氏 (Last Name):", extracted_info.get("姓氏 (Last Name)", "N/A")),
        ("州 (State):", extracted_info.get("州 (State)", "N/A")),
        ("城市 (City):", extracted_info.get("城市 (City)", "N/A")),
        ("详细地址 (Street Address):", extracted_info.get("详细地址 (Street Address)", "N/A")),
        ("出生日期:", extracted_info.get("出生日期", "N/A")),
        ("年龄:", extracted_info.get("年龄", "N/A")),
        ("SSN:", extracted_info.get("SSN", "N/A"))
    ]

    for i, (label_text, value_text) in enumerate(fields, start=1):
        tk.Label(result_frame, text=label_text, font=field_title_font, anchor="w").grid(row=i, column=0, sticky="w", padx=10, pady=2)
        tk.Label(result_frame, text=value_text, anchor="w", justify="left").grid(row=i, column=1, sticky="ew", padx=10, pady=2)

    # 配置结果框架列的权重
    result_frame.grid_columnconfigure(1, weight=1)

def run_analysis():
    analyze_and_display()

# 创建主窗口
root = tk.Tk()
root.title("信息提取小工具")

# 左右布局使用 PanedWindow
paned_window = ttk.Panedwindow(root, orient=tk.HORIZONTAL)
paned_window.pack(fill=tk.BOTH, expand=True)

# 输入区域 Frame
input_frame = tk.Frame(paned_window, padx=10, pady=10)
paned_window.add(input_frame, weight=1)

name_address_label = tk.Label(input_frame, text="姓名地址邮编:")
name_address_label.pack(pady=(0, 5), anchor="w")
name_address_input_area = scrolledtext.ScrolledText(input_frame, width=40, height=8)
name_address_input_area.pack(pady=(0, 10), fill="x", expand=True)

birth_date_label = tk.Label(input_frame, text="出生日期 (Month Day, Year):")
birth_date_label.pack(pady=(5, 5), anchor="w")
birth_date_input_area = tk.Entry(input_frame, width=40)
birth_date_input_area.pack(pady=(0, 10), fill="x")

ssn_label = tk.Label(input_frame, text="SSN (XXX-XX-XXXX 或 XXXXXXXXX):")
ssn_label.pack(pady=(5, 5), anchor="w")
ssn_input_area = tk.Entry(input_frame, width=40)
ssn_input_area.pack(pady=(0, 10), fill="x")

analyze_button_font = font.Font(size=12, weight="bold")
analyze_button = tk.Button(input_frame, text="分析", command=run_analysis, font=analyze_button_font, padx=20, pady=10)
analyze_button.pack(pady=20)

# 结果显示区域 Frame
result_frame = tk.Frame(paned_window, padx=10, pady=10)
paned_window.add(result_frame, weight=1)

# 作者信息
author_info_font = font.Font(size=8, slant="italic")
author_label = tk.Label(root, text="AIGC创意人竹相左边  2025.4.29", font=author_info_font)
author_label.pack(pady=5, anchor="se")

# 运行主循环
root.mainloop()