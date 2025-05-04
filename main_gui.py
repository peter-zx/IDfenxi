import tkinter as tk
import asyncio
from concurrent.futures import ThreadPoolExecutor
from ui.gui import AppGUI

def run_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()

def main():
    # 创建 Tkinter 根窗口
    root = tk.Tk()

    # 创建新的 asyncio 事件循环
    loop = asyncio.new_event_loop()

    # 创建 GUI 实例
    app = AppGUI(root, loop)

    # 启动 asyncio 事件循环（在单独线程中运行）
    executor = ThreadPoolExecutor(max_workers=1)
    executor.submit(run_loop, loop)

    try:
        # 启动 Tkinter 主循环
        root.mainloop()
    finally:
        # 清理
        loop.call_soon_threadsafe(loop.stop)
        executor.shutdown(wait=True)
        loop.close()

if __name__ == "__main__":
    main()