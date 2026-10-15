# -*- coding: utf-8 -*-
"""PyInstaller runtime hook: 启动后自动打开浏览器, 并在控制台输出拉祜族专属版横幅。"""
import os
import sys
import time
import threading

# 拉祜族专属版标识: 后端据此收敛歌手权威归类, 界面只呈现拉祜族
os.environ['MRE_LAHU_ONLY'] = '1'

URL = 'http://127.0.0.1:8766'
BANNER = """
============================================================
  山河回响 · 拉祜族专属版  MountainRiverEchoes-Lahu 1.0.0
  ------------------------------------------------------
  曲库: 拉祜族 806 首    服务地址: http://127.0.0.1:8766
  正在启动本地服务, 浏览器将自动打开...
  关闭此窗口即可退出程序。
============================================================
"""


def _set_console_title():
    try:
        import ctypes
        ctypes.windll.kernel32.SetConsoleTitleW('山河回响 · 拉祜族专属版')
    except Exception:
        pass


def _open_browser():
    # 等 Flask 真正监听后再打开, 避免用户看到"无法访问"
    for _ in range(60):
        time.sleep(0.5)
        try:
            import urllib.request
            with urllib.request.urlopen(URL, timeout=2) as _r:
                if _r.status == 200:
                    break
        except Exception:
            continue
    try:
        import webbrowser
        webbrowser.open(URL)
    except Exception:
        pass


try:
    sys.stdout.write(BANNER)
    sys.stdout.flush()
except Exception:
    pass

_set_console_title()
threading.Thread(target=_open_browser, daemon=True).start()
