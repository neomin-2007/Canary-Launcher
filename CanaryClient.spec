# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_all

# coleta tudo que o PyQt6 precisa (DLLs, plugins, traduções, etc.)
pyqt6_datas, pyqt6_binaries, pyqt6_hiddenimports = collect_all('PyQt6')

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=pyqt6_binaries,  # inclui os binários do Qt
    datas=[
        ('updater.py', '.'),
        ('launcher.py', '.'),
        ('assets/background.png', 'assets'),
        ('assets/banner.png', 'assets'),
        ('assets/icon.ico', 'assets'),
        ('assets/icon.png', 'assets'),
        ('assets/modification_icon.png', 'assets'),
        ('assets/settings_icon.png', 'assets'),
        ('assets/discord_icon.png', 'assets'),
    ] + pyqt6_datas,  # adiciona também os arquivos de dados do Qt
    hiddenimports=pyqt6_hiddenimports,  # adiciona os módulos ocultos do Qt
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='CanaryClient',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # True se quiser console junto
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['assets/icon.png'],  # mantém o ícone
)
