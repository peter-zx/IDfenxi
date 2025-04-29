import tkinter as tk
from tkinter import scrolledtext
from tkinter import ttk
import asyncio
from tabulate import tabulate
from core.extractor import extract_information_async

def analyze_and_display():
    input_text = input_text_area.get("1.0", tk.END)
    extracted_info = asyncio.run(extract_information_async(input_text))

    # 清空之前的表格内容
    for item in result_tree.get_children():
        result_tree.delete(item)

    # 将提取的信息插入表格
    for key, value in extracted_info.items():
        result_tree.insert("", tk.END, values=(key, value if value else "N/A"))

def run_analysis():
    analyze_and_display()

def copy_results():
    headers = ["字段 (Field)", "值 (Value)"]
    table_data = []
    for item in result_tree.get_children():
        values = result_tree.item(item, 'values')
        table_data.append(list(values))

    if table_data:
        formatted_table = tabulate(table_data, headers=headers, tablefmt="grid")
        root.clipboard_clear()
        root.clipboard_append(formatted_table)
        root.update()
        status_label.config(text="结果已复制到剪贴板")
    else:
        status_label.config(text="没有可复制的结果")

# 创建主窗口
root = tk.Tk()
root.title("异步信息提取小工具")

# 创建输入框
input_label = tk.Label(root, text="输入文本:")
input_label.pack(pady=5)
input_text_area = scrolledtext.ScrolledText(root, width=50, height=20)
input_text_area.pack(padx=10, pady=5)

# 创建分析按钮
analyze_button = tk.Button(root, text="分析", command=run_analysis)
analyze_button.pack(pady=10)  # 确保按钮被 pack 到界面中

# 创建结果展示区域 (使用 Treeview 作为表格)
result_label = tk.Label(root, text="分析结果:")
result_label.pack(pady=5)
result_tree = ttk.Treeview(root, columns=("字段", "值"), show="headings")
result_tree.heading("字段", text="字段 (Field)")
result_tree.heading("值", text="值 (Value)")
result_tree.column("字段", width=150)
result_tree.column("值", width=350)
result_tree.pack(padx=10, pady=5)

# 创建复制按钮
copy_button = tk.Button(root, text="复制结果", command=copy_results)
copy_button.pack(pady=10)

# 创建状态标签
status_label = tk.Label(root, text="")
status_label.pack(pady=5)

# 运行主循环
root.mainloop()