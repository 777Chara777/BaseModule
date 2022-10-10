from . import BaseModule as bm

import os

def LogError(ctx, start_file, **kargs):
    direct = "./CrashLog" if "savefile" not in kargs else kargs["savefile"]
    if bm.misdir(direct):
        start_file = start_file.split('\\')
        for x in os.getcwd().split('\\'):
            if x in start_file:
                start_file.remove(x)
            elif x.lower() in start_file:
                start_file.remove(x.lower())

        message = f"\n[{'/'.join(start_file)}] [UTC: {bm.Time(0)}]: {ctx}"

        if bm.misfile(f"{direct}/last.log") != True:
            open(f"{direct}/last.log", 'w').write(message)

        save = bm.file_size(f"{direct}/last.log")
        if save[0] >= 2:
            with open(f"{direct}/last.log", 'r', encoding="UTF-8") as save_file_to_zit:
                file_to_zip = save_file_to_zit.read()
            open(f"{direct}/last.log", 'w')
            zipped = file_to_zip
            with open(f"{direct}/last-{bm.Time(0)}.gz", 'w') as zip_save:
                zip_save.write(zipped)
        else:
            open(f"{direct}/last.log", 'a', encoding="UTF-8").write(message)
    else:
        bm.mkdir(direct)