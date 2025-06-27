import os
import platform

from win32_setctime import setctime

import filedate
#File = filedate.File(input())

#from pathlib import Path

#pathlist = Path("test").glob('**/*.asm')
#for path in pathlist:
#    # because path is object not string
#    path_in_str = str(path)   
#    # print(path_in_str)

def getc(path_to_file):
    """
    Try to get the date that a file was created, falling back to when it was
    last modified if that isn't possible.
    See http://stackoverflow.com/a/39501288/1709587 for explanation.
    """
    if platform.system() == 'Windows':
        return os.path.getctime(path_to_file)
    else:
        stat = os.stat(path_to_file)
        try:
            return stat.st_birthtime
        except AttributeError:
            # We're probably on Linux. No easy way to get creation dates here,
            # so we'll settle for when its content was last modified.

            return stat.st_mtime
def setc(path_to_file):
    File = filedate.File(path_to_file)
    File.created  = "01.01.2000 12:00"

#print(getc("macs are trash"))
#setc("macs are trash")
#print(getc("macs are trash"))


#setctime("bean.txt", 1561675987.509)
