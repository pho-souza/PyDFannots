#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pip/pyinstaller build script for PyDFannots.

Install as Python package:
    python3 setup.py install

Create EXE/APP:
    python3 setup.py build_binary
"""

import os
import sys
import shutil
import setuptools
import distutils.cmd
from PyDFannots import __version__

OSX_INFO_PLIST = "other/osx/Info.plist"

NAME = 'PyDFannots'
MAIN = 'pydfannots.py'
VERSION = __version__


class BuildBinaryCommand(distutils.cmd.Command):
    description = 'build binary release'
    user_options = []
    
    def initialize_options(self):
        pass
    
    def finalize_options(self):
        pass
    
    # noinspection PyShadowingNames
    def run(self):
        if sys.platform == 'darwin':
            with open(OSX_INFO_PLIST, 'r') as file:
                filedata = file.read()
            filedata = filedata.replace('5.5.2', VERSION)
            with open(OSX_INFO_PLIST, 'w') as file:
                file.write(filedata)

            os.system('pyinstaller -y -F -i PyDFannots/gui_assets/icon.ico -n "PyDF Annots GUI" -w -s "pydfannots-gui.py"')
            os.makedirs('dist/PyDFAnnots.app/Contents/Resources/Codecs')
            shutil.copy('other/osx/7z', 'dist/PyDFAnnots.app/Contents/Resources')
            shutil.copy('other/osx/7z.so', 'dist/PyDFAnnots.app/Contents/Resources')
            shutil.copy('other/osx/Rar.so', 'dist/PyDFAnnots.app/Contents/Resources/Codecs')
            shutil.copy('other/osx/Info.plist', 'dist/PyDFAnnots.app/Contents')
            shutil.copy('LICENSE.txt', 'dist/PyDFAnnots.app/Contents/Resources')
            shutil.copy('other/windows/Additional-LICENSE.txt', 'dist/PyDFAnnots.app/Contents/Resources')
            # os.chmod('dist/PyDFAnnots.app/Contents/Resources/7z', 0o777)
            # TODO /usr/bin/codesign --force -s "$MACOS_CERTIFICATE_NAME" --options runtime dist/Applications/Kindle\ Comic\ Converter.app -v
            # os.system('appdmg kcc.json dist/KindleComicConverter_osx_' + VERSION + '.dmg')
            exit(0)
        elif sys.platform == 'win32':
            # command_gui = 'pyinstaller --noconfirm --onedir --windowed --noupx --icon "PyDFannots/gui_assets/logo.ico" --name "PyDFAnnots GUI" --ascii --clean --add-data "PyDFannots/gui_assets/;PyDFannots/gui_assets/" --add-data "PyDFannots/templates;PyDFannots/templates/" --additional-hooks-dir "."  "PyDFannots-gui.py"'
            command_gui = f'pyinstaller --noconfirm --onefile --windowed --noupx --icon "PyDFannots/gui_assets/logo.ico" --name "pydfannotsgui" --ascii --clean --additional-hooks-dir "."  "PyDFannots-gui.py"'
            command_cli = f'pyinstaller --noconfirm --onefile  --name "pydfannots" --ascii --clean  "PyDFannots.py"'
            # command_cli = 'pyinstaller --noconfirm --onedir --noupx --name "PyDFAnnots" --ascii --clean --add-data "PyDFannots/templates;PyDFannots/templates/"  "PyDFannots.py"'
            # os.system('pyinstaller -y -F -i PyDFannots\\gui_assets\\logo.ico -n PyDFannots_' + VERSION + ' -w --noupx pydfannots-gui.py')
            os.system(command_gui)
            os.system(command_cli)
            os.makedirs(f'dist/PyDFAnnots_win_{VERSION}', exist_ok=True)
            os.makedirs(f'dist/PyDFAnnots_linux_{VERSION}/PyDFannots', exist_ok=True)
            shutil.move(f'dist/pydfannots.exe',f'dist/PyDFAnnots_win_{VERSION}/pydfannots.exe')
            shutil.move(f'dist/pydfannotsgui.exe',f'dist/PyDFAnnots_win_{VERSION}/pydfannotsgui_win.exe')
            try:
                shutil.copytree(f'PyDFannots/gui_assets', f'dist/PyDFAnnots_win_{VERSION}/PyDFannots/gui_assets', dirs_exist_ok=True, ignore_dangling_symlinks=True)
            except:
                pass
            try:
                shutil.copytree(f'PyDFannots/templates', f'dist/PyDFAnnots_win_{VERSION}/PyDFannots/templates', dirs_exist_ok=True, ignore_dangling_symlinks=True)
            except:
                pass
            exit(0)
        elif sys.platform == 'linux':
            command_gui = f'pyinstaller --noconfirm --onefile --windowed --noupx --icon "PyDFannots/gui_assets/logo.ico" --name "pydfannotsgui_linux" --ascii --clean --additional-hooks-dir "."  "PyDFannots-gui.py"'
            command_cli = f'pyinstaller --noconfirm --onefile  --name "pydfannots_linux" --ascii --clean  "PyDFannots.py"'
            # # os.system('pyinstaller -y -F -i PyDFannots\\gui_assets\\logo.ico -n PyDFannots_' + VERSION + ' -w --noupx pydfannots-gui.py')
            os.system(command_gui)
            os.system(command_cli)
            if os.path.exists(f'dist/PyDFAnnots_linux_{VERSION}'):
                shutil.rmtree(f'dist/PyDFAnnots_linux_{VERSION}')
            os.makedirs(f'dist/PyDFAnnots_linux_{VERSION}', exist_ok=True)
            shutil.move(f'dist/pydfannots_linux',f'dist/PyDFAnnots_linux_{VERSION}/pydfannots_linux')
            shutil.move(f'dist/pydfannotsgui_linux',f'dist/PyDFAnnots_linux_{VERSION}/pydfannotsgui_linux')
            os.makedirs(f'dist/PyDFAnnots_linux_{VERSION}/PyDFannots', exist_ok=True)
            try:
                shutil.copytree(f'PyDFannots/gui_assets', f'dist/PyDFAnnots_linux_{VERSION}/PyDFannots/gui_assets', dirs_exist_ok=True, ignore_dangling_symlinks=True)
            except:
                pass
            try:
                shutil.copytree(f'PyDFannots/templates', f'dist/PyDFAnnots_linux_{VERSION}/PyDFannots/templates', dirs_exist_ok=True, ignore_dangling_symlinks=True)
            except:
                pass
            
            exit(0)
        else:
            exit(0)

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setuptools.setup(
    cmdclass={
        'build_binary': BuildBinaryCommand,
    },
    name=NAME,
    version=VERSION,
    author='Pedro Souza',
    author_email='pho.souza.mail@gmail.com',
    description='PDF annotations extract using PyMuPDF.',
    long_description=readme,
    url='https://github.com/pho-souza/PyDFannots',
    license=license,
    keywords=['pdf', 'annotations', 'highlight', 'pymupdf', 'obsidian'],
    entry_points={
        'console_scripts': [
            'pydfannots=PyDFannots.cli:main',
        ],
        'gui_scripts': [
            'pydfannots=PyDFannots.gui:main',
        ],
    },
    packages=['pydfannots'],
    install_requires=[
        'PyMuPDF>=1.21.1',
        'tkinterdnd2',
        'Jinja2'
    ],
    classifiers=[],
    zip_safe=False,
)