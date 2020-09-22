# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['demo.py', 'E:\\Computer major\\Python\\pycharmproject\\first_game\\scenes\\begin_scene.py', 'E:\\Computer major\\Python\\pycharmproject\\first_game\\scenes\\scene1.py', 'E:\\Computer major\\Python\\pycharmproject\\first_game\\scenes\\scene2.py', 'E:\\Computer major\\Python\\pycharmproject\\first_game\\scenes\\scene3.py', 'E:\\Computer major\\Python\\pycharmproject\\first_game\\dialog\\Door_dialog.py', 'E:\\Computer major\\Python\\pycharmproject\\first_game\\dialog\\god_dialog.py', 'E:\\Computer major\\Python\\pycharmproject\\first_game\\dialog\\__init__.py', 'E:\\Computer major\\Python\\pycharmproject\\first_game\\scenes\\__init__.py', 'E:\\Computer major\\Python\\pycharmproject\\first_game\\pytmx_study\\utils\\pytmx_module.py', 'E:\\Computer major\\Python\\pycharmproject\\first_game\\object\\Action.py', 'E:\\Computer major\\Python\\pycharmproject\\first_game\\object\\DirAction.py', 'E:\\Computer major\\Python\\pycharmproject\\first_game\\object\\Door.py', 'E:\\Computer major\\Python\\pycharmproject\\first_game\\object\\Gamer.py', 'E:\\Computer major\\Python\\pycharmproject\\first_game\\object\\InteractiveMoveNPC.py', 'E:\\Computer major\\Python\\pycharmproject\\first_game\\object\\Invisible_obstacle.py', 'E:\\Computer major\\Python\\pycharmproject\\first_game\\object\\NPC.py', 'E:\\Computer major\\Python\\pycharmproject\\first_game\\object\\SceneGamer.py', 'E:\\Computer major\\Python\\pycharmproject\\first_game\\object\\Treasure.py'])
             pathex=['E:\\Computer major\\Python\\pycharmproject\\first_game'],
             binaries=[],
             datas=[],
             hiddenimports=[],
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
          [],
          exclude_binaries=True,
          name='demo',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='demo')
