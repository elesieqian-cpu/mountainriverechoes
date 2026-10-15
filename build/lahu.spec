# -*- mode: python ; coding: utf-8 -*-
"""山河回响 · 拉祜族专属版 —— PyInstaller 打包配置(单文件 exe)"""
from PyInstaller.utils.hooks import collect_submodules, collect_data_files, collect_dynamic_libs

ROOT = r'C:\Users\86135\Desktop\workbuddy\mountainriverechoes'

# musicdl 为本地包(入口脚本运行时才把仓库根插入 sys.path), 静态分析抓不到 -> 全量子模块收集
hiddenimports = collect_submodules('musicdl')
hiddenimports += [
    'curl_cffi', 'curl_cffi.requests',           # musicdl 用 optionalimport 动态引入
    'Cryptodome', 'Cryptodome.Cipher', 'Cryptodome.Util',
    'flask', 'werkzeug', 'jinja2', 'jinja2.ext',
]

datas = [
    (ROOT + r'\webui\templates\mountainriverechoes.html', 'webui/templates'),  # 已定稿的拉祜族主题 UI
    # 只打入「当前最新」的拉祜族曲库单文件: 避免 index_snapshot.json / versions/ 等旧缓存副本混入
    (ROOT + r'\webui\ethnos_cache\e22_拉祜族.json', 'webui/ethnos_cache'),
    # ui_state.json 不打入: 专属版从全新界面状态启动, 避免残留其他民族的界面数据
]
datas += collect_data_files('musicdl')       # modules/wvds/*.wvd 等包内资源

binaries = collect_dynamic_libs('curl_cffi')

# 曲库 1166 首全部为直链, 不经过 yt-dlp; av(ffmpeg) 亦未被引用 -> 排除以压缩体积
excludes = [
    'av', 'yt_dlp', 'yt_dlp_plugins', 'nodejs_wheel', 'nodejs_wheel_binaries',
    'tkinter', 'unittest', 'pydoc', 'doctest', 'lib2to3', 'tcl',
]

a = Analysis(
    [ROOT + r'\webui\mountainriverechoes.py'],
    pathex=[ROOT],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[ROOT + r'\build\rthook_open_browser.py'],
    excludes=excludes,
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='MountainRiverEchoes-Lahu-Setup-1.0.0',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)
