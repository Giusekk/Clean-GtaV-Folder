import os
import shutil
import sys
import win32api
from pathlib import Path
from glob import glob
from distutils.dir_util import copy_tree


def folder_exists(path: str) -> bool:
    return Path(path).exists()


def folder_is_empty(path: str) -> bool:
    return not any(Path(path).iterdir())


gta_v_folder = "C:\Program Files\Epic Games\GTAV"
epic_folder = "C:\Program Files (x86)\Epic Games"
modcleaned_folder = os.path.join(gta_v_folder, "modcleaned")

whitelist_files = [
    'Installers',
    'update',
    'x64',
    '_CommonRedist',
    'bink2w64.dll',
    'commandline.txt',
    'common.rpf',
    'd3dcompiler_46.dll',
    'd3dcsx_46.dll',
    'GFSDK_ShadowLib.win64.dll',
    'GFSDK_TXAA.win64.dll',
    'GFSDK_TXAA_AlphaResolve.win64.dll',
    'GTA5.exe',
    'GTAVLanguageSelect.exe',
    'GTAVLauncher.exe',
    'PlayGTAV.exe',
    'x64a.rpf',
    'x64b.rpf',
    'x64c.rpf',
    'x64d.rpf',
    'x64e.rpf',
    'x64f.rpf',
    'x64g.rpf',
    'x64h.rpf',
    'x64i.rpf',
    'x64j.rpf',
    'x64k.rpf',
    'x64l.rpf',
    'x64m.rpf',
    'x64n.rpf',
    'x64o.rpf',
    'x64p.rpf',
    'x64q.rpf',
    'x64r.rpf',
    'x64s.rpf',
    'x64t.rpf',
    'x64u.rpf',
    'x64v.rpf',
    'x64w.rpf',
    'steam_api64.dll',
    'steam_appid.txt',
    'installscript.vdf',
    'EntryPoints.txt',
    '.egstore',
    'GPUPerfAPIDX11-x64.dll',
    'NvPmApi.Core.win64.dll',
    'version.txt',
    'Readme',
    'Redistributables',
    'EOSSDK-Win64-Shipping.dll',
    'Clean GtaV Folder.exe',
    'modcleaned'
]

def is_gtav_installed() -> bool:
    if folder_exists(gta_v_folder):
        return True
    return False


def get_all_files(folder, exclude_list=None):
    all_files = glob(f"{folder}/*")
    if not exclude_list:
        return all_files
    filteredResults = [f for f in all_files if Path(f).name not in exclude_list]
    return filteredResults


def action():
    if not is_gtav_installed():
        win32api.MessageBox(0, "GtaV is not installed on your machine.", "Error!")
        sys.exit(1)
    while True:
        choice = input("Do you want to clean mods or restore them? (type exit for quit): ")
        match choice.lower().translate(str.maketrans('', '', ' \n\t\r')):
            case "clean":
                i = 1 # counter for see if is first clean
                if not folder_exists(modcleaned_folder):
                    try:
                        os.mkdir(modcleaned_folder)
                        i = 0
                    except Exception as e:
                        win32api.MessageBox(0, str(e), "Error!")

                for mod_to_copy in get_all_files(gta_v_folder, exclude_list=whitelist_files):
                    if Path(mod_to_copy).is_file():
                        shutil.copy2(mod_to_copy, modcleaned_folder)
                        try:
                            os.remove(mod_to_copy)
                        except OSError as e:
                            pass
                    else:
                        copy_tree(mod_to_copy, modcleaned_folder)
                else:
                    if i == 1:
                        print("The gtav folder is already clean.")
                    else:
                        print("GtaV folder cleaned.")
            case "restore":
                if not Path(modcleaned_folder).exists():
                    print("You have already brought the mods back!")
                else:
                    copy_tree(modcleaned_folder, gta_v_folder)
                    try:
                        shutil.rmtree(modcleaned_folder)
                    except OSError as e:
                        pass
                    print("GtaV folder restored with mods.")
            case "exit":
                print("Exiting...")
                break
            case _:
                print("Invalid choice.")

if __name__ == "__main__":
    action()
    sys.exit(0)