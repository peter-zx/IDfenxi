import tkinter as tk
from tkinter import scrolledtext, messagebox
import asyncio
import webbrowser

from core.extractor import extract_information
from ui.links_config import STEPS, REMARK

class AppGUI:
    def __init__(self, root, loop):
        self.root = root
        self.loop = loop
        self.setup_ui()

    def setup_ui(self):
        self.root.title("EDU 邮箱注册信息生成器")
        self.root.geometry("1200x500")
        self.root.configure(bg="#F5F5F5")

        top_frame = tk.Frame(self.root, bg="#F5F5F5")
        top_frame.pack(side="top", fill="x", padx=10, pady=(10, 5))

        title_label = tk.Label(top_frame, text="EDU 邮箱注册信息生成器", font=("DengXian", 18, "bold"), fg="black", bg="#F5F5F5")
        title_label.pack(side="left")

        author_label = tk.Label(top_frame, text="人机协作 Grok&竹相左边", font=("DengXian", 10), fg="#666666", bg="#F5F5F5")
        author_label.pack(side="left", padx=(10, 10))

        sponsor_button = tk.Button(top_frame, text="赞助", command=self.show_sponsor_window, font=("DengXian", 10), bg="#FF9500", fg="white", activebackground="#CC7700", relief="flat")
        sponsor_button.pack(side="left")

        main_frame = tk.Frame(self.root, bg="#F5F5F5")
        main_frame.pack(fill="both", expand=True)

        left_frame = tk.Frame(main_frame, bg="#FFFFFF", relief="flat", bd=2, width=400)
        left_frame.pack(side="left", fill="y", padx=10, pady=5)
        left_frame.pack_propagate(False)

        content_frame = tk.Frame(left_frame, bg="#FFFFFF")
        content_frame.pack(anchor="center", pady=20)

        tk.Label(content_frame, text="EDU信息生成的步骤", font=("DengXian", 14, "bold"), fg="#3D3D3D", bg="#FFFFFF").pack(anchor="w", padx=10, pady=(0, 20))

        for i, step in enumerate(STEPS, 1):
            step_frame = tk.Frame(content_frame, bg="#FFFFFF")
            step_frame.pack(anchor="w", padx=10, pady=5)

            tk.Label(step_frame, text=f"{i}. {step['name']}", font=("DengXian", 14), fg="black", bg="#FFFFFF", width=20, anchor="w").pack(side="left")

            tk.Button(step_frame, text="打开", command=lambda url=step['url']: webbrowser.open(url), font=("DengXian", 12), bg="#0078D4", fg="white", activebackground="#005A9E", relief="flat", width=10).pack(side="left", padx=(10, 0))

        tk.Label(content_frame, text=REMARK, font=("DengXian", 10, "italic"), fg="#666666", bg="#FFFFFF", wraplength=350).pack(anchor="w", padx=10, pady=(20, 0))

        input_frame = tk.Frame(main_frame, bg="#FFFFFF", relief="flat", bd=2, width=400)
        input_frame.pack(side="left", fill="both", padx=10, pady=5)
        input_frame.pack_propagate(False)

        tk.Label(input_frame, text="姓名地址邮码:", font=("DengXian", 12, "bold"), fg="black", bg="#FFFFFF").pack(anchor="w", padx=10, pady=(10, 0))
        self.ta_name_addr = scrolledtext.ScrolledText(input_frame, width=60, height=8, font=("DengXian", 12), bg="#F9F9F9", relief="solid", bd=2)
        self.ta_name_addr.pack(fill="x", padx=10, pady=(0, 10))

        tk.Label(input_frame, text="出生日期:", font=("DengXian", 12, "bold"), fg="black", bg="#FFFFFF").pack(anchor="w", padx=10)
        self.ent_birth = scrolledtext.ScrolledText(input_frame, width=60, height=2, font=("DengXian", 12), bg="#F9F9F9", relief="solid", bd=2)
        self.ent_birth.pack(fill="x", padx=10, pady=(0, 10))

        tk.Label(input_frame, text="SSN:", font=("DengXian", 12, "bold"), fg="black", bg="#FFFFFF").pack(anchor="w", padx=10)
        self.ent_ssn = scrolledtext.ScrolledText(input_frame, width=60, height=2, font=("DengXian", 12), bg="#F9F9F9", relief="solid", bd=2)
        self.ent_ssn.pack(fill="x", padx=10, pady=(0, 10))

        self.analyze_button = tk.Button(input_frame, text="分析", command=self.run_analysis, font=("DengXian", 12), bg="#0078D4", fg="white", activebackground="#005A9E", relief="flat", width=20, height=2)
        self.analyze_button.pack(pady=10)

        self.result_frame = tk.Frame(main_frame, bg="#FFFFFF", relief="flat", bd=2, width=400)
        self.result_frame.pack(side="right", fill="both", padx=10, pady=5)
        self.result_frame.pack_propagate(False)

    def run_analysis(self):
        self.analyze_button.config(state="disabled")
        
        name_address = self.ta_name_addr.get("1.0", tk.END).strip()
        birth_date = self.ent_birth.get("1.0", tk.END).strip()
        ssn = self.ent_ssn.get("1.0", tk.END).strip()

        if not name_address:
            messagebox.showwarning("输入缺失", "请在左侧“姓名地址邮码”框内输入内容。")
            self.analyze_button.config(state="normal")
            return
        if not birth_date and not ssn:
            messagebox.showwarning("输入建议", "建议提供出生日期或SSN以获得更完整的结果。")

        async def async_analysis():
            try:
                info = await extract_information(name_address, birth_date, ssn)
                self.root.after(0, lambda: self.display_results(info))
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("解析失败", f"发生异常：\n{e}"))
            finally:
                self.root.after(0, lambda: self.analyze_button.config(state="normal"))

        asyncio.run_coroutine_threadsafe(async_analysis(), self.loop)

    def display_results(self, info):
        for widget in self.result_frame.winfo_children():
            widget.destroy()

        if not any(info.values()):
            messagebox.showinfo("无结果", "未解析到任何有效信息，请检查输入格式。\n"
                                        "示例：\nJohn Doe\n123 Main St, Springfield, IL 62701")
            return

        row = 0
        for key, val in info.items():
            if val is not None:
                tk.Label(self.result_frame, text=f"{key}:", font=("DengXian", 12, "bold"), fg="black", bg="#FFFFFF", anchor="w", width=15).grid(row=row, column=0, sticky="w", padx=5, pady=2)
                content_text = tk.Text(self.result_frame, height=1, width=40, wrap=tk.WORD, borderwidth=0, highlightthickness=0, font=("DengXian", 12), fg="black", bg="#E0E0E0")
                content_text.grid(row=row, column=1, sticky="w", padx=5, pady=2)
                content_text.insert(tk.END, str(val))
                content_text.configure(state="normal")
                row += 1

    def show_sponsor_window(self):
        sponsor_window = tk.Toplevel(self.root)
        sponsor_window.title("赞助支持")
        sponsor_window.geometry("300x200")
        sponsor_window.configure(bg="#F5F5F5")
        
        tk.Label(sponsor_window, text="感谢您的支持！", font=("DengXian", 12, "bold"), fg="black", bg="#F5F5F5").pack(pady=10)
        tk.Label(sponsor_window, text="未来添加收款码\n或赞助方式", font=("DengXian", 10), fg="#666666", bg="#F5F5F5", justify="center").pack(pady=10)
        tk.Button(sponsor_window, text="关闭", command=sponsor_window.destroy, font=("DengXian", 10), bg="#0078D4", fg="white", activebackground="#005A9E", relief="flat").pack(pady=10)