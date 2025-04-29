import tkinter as tk
from tkinter import scrolledtext
from tkinter import ttk
import asyncio
from core.extractor import extract_information_async

def analyze_and_display():
    input_text = input_text_area.get("1.0", tk.END)
    manual_address_text = address_input_area.get("1.0", tk.END).strip()
    extracted_info = asyncio.run(extract_information_async(input_text, manual_address_text))

    # 清空之前的表格内容
    for item in result_tree.get_children():
        result_tree.delete(item)

    # 将提取的信息插入表格
    result_tree.insert("", tk.END, values=(extracted_info.get("名字 (First Name)"),
                                           extracted_info.get("姓氏 (Last Name)"),
                                           extracted_info.get("详细地址 (Street Address)"),
                                           extracted_info.get("城市 (City)"),
                                           extracted_info.get("州 (State)"),
                                           extracted_info.get("SSN (社会安全号码)"),
                                           extracted_info.get("出生日期 (Date of Birth)")))

def run_analysis():
    analyze_and_display()

# 创建主窗口
root = tk.Tk()
root.title("异步信息提取小工具")

# 创建输入文本框
input_label = tk.Label(root, text="输入文本:")
input_label.pack(pady=5)
input_text_area = scrolledtext.ScrolledText(root, width=50, height=10) # 缩小高度
input_text_area.pack(padx=10, pady=5)

# 创建地址输入框
address_label = tk.Label(root, text="手动输入地址 (街道, 城市 ST Zip):")
address_label.pack(pady=5)
address_input_area = scrolledtext.ScrolledText(root, width=50, height=3) # 较小的高度
address_input_area.pack(padx=10, pady=5)

# 创建分析按钮
analyze_button = tk.Button(root, text="分析", command=run_analysis)
analyze_button.pack(pady=10)

# 创建结果展示区域 (使用 Treeview 作为表格)
result_label = tk.Label(root, text="分析结果:")
result_label.pack(pady=5)
result_tree = ttk.Treeview(root, columns=("first_name", "last_name", "street_address", "city", "state", "ssn", "birth_date"), show="headings")
result_tree.heading("first_name", text="名字 (First Name)")
result_tree.heading("last_name", text="姓氏 (Last Name)")
result_tree.heading("street_address", text="详细地址 (Street Address)")
result_tree.heading("city", text="城市 (City)")
result_tree.heading("state", text="州 (State)")
result_tree.heading("ssn", text="SSN (社会安全号码)")
result_tree.heading("birth_date", text="出生日期 (Date of Birth)")
result_tree.column("first_name", width=100)
result_tree.column("last_name", width=100)
result_tree.column("street_address", width=200)
result_tree.column("city", width=100)
result_tree.column("state", width=100) # 增加宽度以显示完整州名
result_tree.column("ssn", width=150)
result_tree.column("birth_date", width=150)
result_tree["displaycolumns"] = ("first_name", "last_name", "street_address", "city", "state", "ssn", "birth_date")
result_tree.pack(padx=10, pady=5, expand=True, fill="both")

# 运行主循环
root.mainloop()