# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['Files', '(x86)\\Windows', 'Kits\\10\\Redist\\10.0.19041.0\\ucrt\\DLLs\\x86', 'main.py'],
             pathex=['C:\\Program', 'C:\\Users\\USer\\PycharmProjects\\ITIS_PRODUCTION3'],
             binaries=[],
             datas=[],
             hiddenimports=['PyQt5.sip'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='Files',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False )
