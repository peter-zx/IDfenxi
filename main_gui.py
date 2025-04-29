import tkinter as tk
from tkinter import scrolledtext, messagebox
from core.extractor import extract_information

def run_analysis():
    # 调试：确认回调触发
    print("调试：分析按钮被点击")

    # 1. 读取输入
    name_address = ta_name_addr.get("1.0", tk.END).strip()
    birth_date = ent_birth.get().strip()
    ssn = ent_ssn.get().strip()

    # 2. 输入验证
    if not name_address:
        messagebox.showwarning("输入缺失", "请在左侧“姓名地址邮编”框内输入内容。")
        return
    if not birth_date and not ssn:
        messagebox.showwarning("输入建议", "建议提供出生日期或SSN以获得更完整的结果。")

    # 3. 调用解析函数
    try:
        info = extract_information(name_address, birth_date, ssn)
        print("调试：解析结果 =", info)  # 打印结果便于调试
    except Exception as e:
        messagebox.showerror("解析失败", f"发生异常：\n{e}")
        return

    # 4. 清空结果区
    for widget in result_frame.winfo_children():
        widget.destroy()

    # 5. 显示解析结果
    if not any(info.values()):  # 如果所有字段都为空
        messagebox.showinfo("无结果", "未解析到任何有效信息，请检查输入格式。\n"
                                    "示例：\nJohn Doe\n123 Main St, Springfield, IL 62701")
        return

    # 创建标题和内容的框架
    row = 0
    for key, val in info.items():
        if val is not None:  # 只显示非空字段
            # 标题：使用 Label，加粗，不可选中
            tk.Label(result_frame, text=f"{key}:", font=("Arial", 10, "bold"), anchor="w", width=25).grid(row=row, column=0, sticky="w", padx=5, pady=2)
            # 内容：使用 Text，可复制
            content_text = tk.Text(result_frame, height=1, width=30, wrap=tk.WORD, borderwidth=0, highlightthickness=0)
            content_text.grid(row=row, column=1, sticky="w", padx=5, pady=2)
            content_text.insert(tk.END, str(val))
            content_text.configure(state="normal")  # 允许复制
            row += 1

    # 添加作者信息
    tk.Label(result_frame, text="作者：人机协作Grok&竹相左边，由xAI创建", font=("Arial", 8), anchor="e").grid(row=row, column=0, columnspan=2, sticky="se", pady=10)

# 主程序
root = tk.Tk()
root.title("信息提取小工具")

# 左侧：输入区
left = tk.Frame(root, padx=10, pady=10)
left.pack(side="left", fill="both", expand=True)

tk.Label(left, text="姓名地址邮编:").pack(anchor="w")
ta_name_addr = scrolledtext.ScrolledText(left, width=40, height=6)
ta_name_addr.pack(fill="x", pady=(0, 10))

tk.Label(left, text="出生日期 (e.g. September 7, 2002):").pack(anchor="w")
ent_birth = tk.Entry(left, width=40)
ent_birth.pack(fill="x", pady=(0, 10))

tk.Label(left, text="SSN (XXX-XX-XXXX 或 9 位数字):").pack(anchor="w")
ent_ssn = tk.Entry(left, width=40)
ent_ssn.pack(fill="x", pady=(0, 10))

tk.Button(left, text="分析", command=run_analysis, width=15, height=1).pack(pady=10)

# 右侧：结果区
result_frame = tk.Frame(root, padx=10, pady=10, relief="groove", bd=1)
result_frame.pack(side="right", fill="both", expand=True)

root.mainloop()