# -*- mode: python ; coding: utf-8 -*-

import sys ;
sys.setrecursionlimit(sys.getrecursionlimit() * 5)
block_cipher = None


a = Analysis(
    ['APP.py'],
    pathex=[],
    binaries=[],
    datas=[('Stock_data.db', '.'), ('Financial_Assistant_new.pkl', '.'), ('Intents.json', '.'), ('sell.png', '.'), ('gains.png', '.'), ('bull-market.png', '.'), ('optimize.png', '.'), ('add.png', '.'), ('chart.png', '.'), ('database.png', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=True,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [('v', None, 'OPTION')],
    exclude_binaries=True,
    name='APP',
    debug=True,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='APP',
)
