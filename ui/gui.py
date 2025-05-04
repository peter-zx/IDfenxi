import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog
import asyncio
import webbrowser
import pyperclip
import csv
import os
import glob
from datetime import datetime
from PIL import Image, ImageTk

from core.extractor import extract_information
from ui.links_config import STEPS, REMARK, ANNOUNCEMENT
from ui.sponsor_config import SPONSOR_CONTENT

class AppGUI:
    def __init__(self, root, loop):
        self.root = root
        self.loop = loop
        self.current_results = []
        self.history_records = []
        self.records_dir = "records"
        self.setup_ui()
        self.load_history()

    def setup_ui(self):
        self.root.title("EDU 邮箱注册信息生成器")
        self.root.geometry("1200x600")
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

        # 步骤区域（占 7/10）
        steps_frame = tk.Frame(left_frame, bg="#FFFFFF", height=420)
        steps_frame.pack(fill="x", pady=(10, 5))
        steps_frame.pack_propagate(False)

        tk.Label(steps_frame, text="EDU信息生成的步骤", font=("DengXian", 14, "bold"), fg="#3D3D3D", bg="#FFFFFF").pack(anchor="w", padx=10, pady=(10, 20))

        for i, step in enumerate(STEPS[:-1], 1):
            step_frame = tk.Frame(steps_frame, bg="#FFFFFF")
            step_frame.pack(anchor="w", padx=10, pady=5)

            tk.Label(step_frame, text=f"{i}. {step['name']}", font=("DengXian", 14), fg="black", bg="#FFFFFF", width=20, anchor="w").pack(side="left")

            tk.Button(step_frame, text="打开", command=lambda url=step['url']: webbrowser.open(url), font=("DengXian", 12), bg="#0078D4", fg="white", activebackground="#005A9E", relief="flat", width=10).pack(side="left", padx=(10, 0))

        # 公告区域（占 3/10）
        announcement_frame = tk.Frame(left_frame, bg="#FFFFFF", height=180)
        announcement_frame.pack(fill="x", pady=(5, 10))
        announcement_frame.pack_propagate(False)

        tk.Label(announcement_frame, text=ANNOUNCEMENT, font=("DengXian", 10, "italic"), fg="#666666", bg="#FFFFFF", wraplength=300, justify="center").pack(anchor="center", padx=10, pady=(10, 10))

        global_network_step = STEPS[-1]
        global_network_button = tk.Button(
            announcement_frame,
            text=global_network_step['name'],
            command=lambda: webbrowser.open(global_network_step['url']),
            font=("DengXian", 10),
            bg="#E0E0E0",
            fg="#666666",
            activebackground="#CCCCCC",
            relief="flat",
            width=12
        )
        global_network_button.pack(anchor="center", pady=(0, 10))

        input_frame = tk.Frame(main_frame, bg="#FFFFFF", relief="flat", bd=2, width=400)
        input_frame.pack(side="left", fill="both", padx=10, pady=5)
        input_frame.pack_propagate(False)

        tk.Label(input_frame, text="姓名地址邮码（每组用空行分隔）:", font=("DengXian", 12, "bold"), fg="black", bg="#FFFFFF").pack(anchor="w", padx=10, pady=(10, 0))
        self.ta_name_addr = scrolledtext.ScrolledText(input_frame, width=60, height=8, font=("DengXian", 12), bg="#F9F9F9", relief="solid", bd=2)
        self.ta_name_addr.pack(fill="x", padx=10, pady=(0, 10))

        tk.Label(input_frame, text="出生日期（YYYY-MM-DD）:", font=("DengXian", 12, "bold"), fg="black", bg="#FFFFFF").pack(anchor="w", padx=10)
        self.ent_birth = scrolledtext.ScrolledText(input_frame, width=60, height=2, font=("DengXian", 12), bg="#F9F9F9", relief="solid", bd=2)
        self.ent_birth.pack(fill="x", padx=10, pady=(0, 10))

        tk.Label(input_frame, text="SSN（XXX-XX-XXXX）:", font=("DengXian", 12, "bold"), fg="black", bg="#FFFFFF").pack(anchor="w", padx=10)
        self.ent_ssn = scrolledtext.ScrolledText(input_frame, width=60, height=2, font=("DengXian", 12), bg="#F9F9F9", relief="solid", bd=2)
        self.ent_ssn.pack(fill="x", padx=10, pady=(0, 10))

        button_frame = tk.Frame(input_frame, bg="#FFFFFF")
        button_frame.pack(pady=10)
        self.analyze_button = tk.Button(button_frame, text="分析", command=self.run_analysis, font=("DengXian", 12), bg="#0078D4", fg="white", activebackground="#005A9E", relief="flat", width=10)
        self.analyze_button.pack(side="left", padx=5)
        self.copy_button = tk.Button(button_frame, text="复制结果", command=self.copy_results, font=("DengXian", 12), bg="#28A745", fg="white", activebackground="#1E7E34", relief="flat", width=10)
        self.copy_button.pack(side="left", padx=5)
        self.export_button = tk.Button(button_frame, text="导出结果", command=self.export_results, font=("DengXian", 12), bg="#FFC107", fg="black", activebackground="#E0A800", relief="flat", width=10)
        self.export_button.pack(side="left", padx=5)

        self.result_frame = tk.Frame(main_frame, bg="#FFFFFF", relief="flat", bd=2, width=400)
        self.result_frame.pack(side="right", fill="both", padx=10, pady=5)
        self.result_frame.pack_propagate(False)

        self.current_result_frame = tk.Frame(self.result_frame, bg="#FFFFFF")
        self.current_result_frame.pack(side="top", fill="both", expand=True)
        tk.Label(self.current_result_frame, text="当前分析结果", font=("DengXian", 12, "bold"), fg="#3D3D3D", bg="#FFFFFF").pack(anchor="w", padx=5, pady=5)

        self.history_frame = tk.Frame(self.result_frame, bg="#FFFFFF")
        self.history_frame.pack(side="bottom", fill="x", pady=10)
        tk.Label(self.history_frame, text="最近历史记录", font=("DengXian", 12, "bold"), fg="#3D3D3D", bg="#FFFFFF").pack(anchor="w", padx=5)
        self.history_list = tk.Frame(self.history_frame, bg="#FFFFFF")
        self.history_list.pack(fill="x", padx=5)

    def load_history(self):
        for widget in self.history_list.winfo_children():
            widget.destroy()
        self.history_records = []

        if not os.path.exists(self.records_dir):
            os.makedirs(self.records_dir)

        csv_files = glob.glob(os.path.join(self.records_dir, "*.csv"))
        csv_files.sort(key=os.path.getmtime, reverse=True)
        csv_files = csv_files[:6]

        for file_path in csv_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    record = next(reader)
                    timestamp = os.path.basename(file_path).split('_')[-1].replace('.csv', '')
                    self.history_records.append({
                        'file_path': file_path,
                        'record': record,
                        'timestamp': timestamp
                    })
            except Exception:
                continue

        for idx, item in enumerate(self.history_records):
            name = item['record'].get('名字', '') + ' ' + item['record'].get('姓氏', '')
            label_text = f"{name.strip()} ({item['timestamp']})"
            tk.Button(self.history_list, text=label_text, command=lambda r=item['record']: self.display_history_record(r), font=("DengXian", 10), bg="#E0E0E0", fg="black", relief="flat", anchor="w", width=40).pack(fill="x", pady=2)

    def run_analysis(self):
        self.analyze_button.config(state="disabled")
        self.current_results = []
        
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
                results = await extract_information(name_address, birth_date, ssn)
                self.root.after(0, lambda: self.save_records(results))
                self.root.after(0, lambda: self.display_results(results))
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("解析失败", f"发生异常：\n{e}"))
            finally:
                self.root.after(0, lambda: self.analyze_button.config(state="normal"))

        asyncio.run_coroutine_threadsafe(async_analysis(), self.loop)

    def save_records(self, results):
        if not os.path.exists(self.records_dir):
            os.makedirs(self.records_dir)

        for info in results:
            first_name = info.get('名字', '').replace(' ', '')
            last_name = info.get('姓氏', '').replace(' ', '')
            name = (first_name + last_name) or 'Unknown'
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            file_name = f"{name}_{timestamp}.csv"
            file_path = os.path.join(self.records_dir, file_name)

            ssn = info.get('SSN', '')
            if self.is_duplicate(info, first_name, last_name, ssn):
                messagebox.showinfo("重复记录", f"记录 {name} 已存在，跳过保存。")
                continue

            try:
                with open(file_path, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=["名字", "姓氏", "州", "城市", "详细地址", "邮编", "出生日期", "英文出生日期", "年龄", "SSN"], extrasaction='ignore')
                    writer.writeheader()
                    writer.writerow(info)
            except Exception as e:
                messagebox.showerror("保存失败", f"保存记录 {name} 时发生错误：\n{e}")
                continue

        self.load_history()

    def is_duplicate(self, info, first_name, last_name, ssn):
        for item in self.history_records:
            existing = item['record']
            if (existing.get('名字', '') == first_name and
                existing.get('姓氏', '') == last_name and
                existing.get('SSN', '') == ssn):
                return True
        return False

    def display_results(self, results):
        for widget in self.current_result_frame.winfo_children():
            if widget.winfo_name() != "label":
                widget.destroy()

        if not results:
            messagebox.showinfo("无结果", "未解析到任何有效信息，请检查输入格式。\n"
                                        "示例：\nJohn Doe\n123 Main St\nSpringfield, IL 62701\n\nJane Smith\n456 Oak St\nChicago, IL 60601")
            return

        self.current_results = results
        canvas = tk.Canvas(self.current_result_frame, bg="#FFFFFF")
        scrollbar = tk.Scrollbar(self.current_result_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#FFFFFF")

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        for idx, info in enumerate(results, 1):
            tk.Label(scrollable_frame, text=f"记录 {idx}", font=("DengXian", 12, "bold"), fg="#0078D4", bg="#FFFFFF").grid(row=(idx-1)*12, column=0, columnspan=2, sticky="w", padx=5, pady=5)
            row = (idx-1)*12 + 1
            for key, val in info.items():
                if val is not None:
                    tk.Label(scrollable_frame, text=f"{key}:", font=("DengXian", 12, "bold"), fg="black", bg="#FFFFFF", anchor="w", width=15).grid(row=row, column=0, sticky="w", padx=5, pady=2)
                    content_text = tk.Text(scrollable_frame, height=1, width=40, wrap=tk.WORD, borderwidth=0, highlightthickness=0, font=("DengXian", 12), fg="black", bg="#E0E0E0")
                    content_text.grid(row=row, column=1, sticky="w", padx=5, pady=2)
                    content_text.insert(tk.END, str(val))
                    content_text.configure(state="disabled")
                    row += 1

    def display_history_record(self, record):
        for widget in self.current_result_frame.winfo_children():
            if widget.winfo_name() != "label":
                widget.destroy()

        canvas = tk.Canvas(self.current_result_frame, bg="#FFFFFF")
        scrollbar = tk.Scrollbar(self.current_result_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#FFFFFF")

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        tk.Label(scrollable_frame, text="历史记录", font=("DengXian", 12, "bold"), fg="#0078D4", bg="#FFFFFF").grid(row=0, column=0, columnspan=2, sticky="w", padx=5, pady=5)
        row = 1
        for key, val in record.items():
            if val:
                tk.Label(scrollable_frame, text=f"{key}:", font=("DengXian", 12, "bold"), fg="black", bg="#FFFFFF", anchor="w", width=15).grid(row=row, column=0, sticky="w", padx=5, pady=2)
                content_text = tk.Text(scrollable_frame, height=1, width=40, wrap=tk.WORD, borderwidth=0, highlightthickness=0, font=("DengXian", 12), fg="black", bg="#E0E0E0")
                content_text.grid(row=row, column=1, sticky="w", padx=5, pady=2)
                content_text.insert(tk.END, str(val))
                content_text.configure(state="disabled")
                row += 1

    def copy_results(self):
        if not self.current_results:
            messagebox.showwarning("无结果", "当前没有可复制的解析结果。")
            return
        result_text = ""
        for idx, info in enumerate(self.current_results, 1):
            result_text += f"记录 {idx}:\n"
            for key, val in info.items():
                if val is not None:
                    result_text += f"{key}: {val}\n"
            result_text += "\n"
        pyperclip.copy(result_text)
        messagebox.showinfo("成功", "结果已复制到剪贴板！")

    def export_results(self):
        if not self.current_results:
            messagebox.showwarning("无结果", "当前没有可导出的解析结果。")
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
        if not file_path:
            return
        try:
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=["名字", "姓氏", "州", "城市", "详细地址", "邮编", "出生日期", "英文出生日期", "年龄", "SSN"], extrasaction='ignore')
                writer.writeheader()
                for info in self.current_results:
                    writer.writerow(info)
            messagebox.showinfo("成功", f"结果已导出到 {file_path}")
        except Exception as e:
            messagebox.showerror("导出失败", f"导出时发生错误：\n{e}")

    def show_sponsor_window(self):
        sponsor_window = tk.Toplevel(self.root)
        sponsor_window.title("赞助支持")
        sponsor_window.geometry("400x500")
        sponsor_window.configure(bg="#F5F5F5")

        content_frame = tk.Frame(sponsor_window, bg="#F5F5F5")
        content_frame.pack(pady=20, padx=20, fill="both", expand=True)

        tk.Label(content_frame, text=SPONSOR_CONTENT["title"], font=("DengXian", 16, "bold"), fg="#333333", bg="#F5F5F5").pack(pady=(0, 20))

        if SPONSOR_CONTENT["image_path"]:
            try:
                image = Image.open(SPONSOR_CONTENT["image_path"])
                image = image.resize((200, 200), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(image)
                image_label = tk.Label(content_frame, image=photo, bg="#F5F5F5")
                image_label.image = photo
                image_label.pack(pady=(0, 20))
            except Exception as e:
                tk.Label(content_frame, text=f"无法加载图片: {str(e)}", font=("DengXian", 10), fg="#666666", bg="#F5F5F5").pack(pady=(0, 20))

        tk.Label(content_frame, text=SPONSOR_CONTENT["description"], font=("DengXian", 12), fg="#666666", bg="#F5F5F5", wraplength=350, justify="center").pack(pady=(0, 20))

        tk.Button(content_frame, text="关闭", command=sponsor_window.destroy, font=("DengXian", 12), bg="#0078D4", fg="white", activebackground="#005A9E", relief="flat", width=12).pack(pady=10)