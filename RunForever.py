import ctypes
import os
import sys
import subprocess as sb
from subprocess import Popen

filename = sys.argv[1]
while True:
    print("\nStarting " + filename)

    try:
        p = Popen("python " + filename, shell=True)
        p.wait(100)
    except:
        "(Exception!) Trying to create server again."
    p.wait(100)
    os.system(
        "runas /savecred /profile /user:slavka \"powershell.exe Stop-Process -ID (Get-Process -Id (Get-NetTCPConnection -LocalPort 5000).OwningProcess).Id -Force\"")
    p.wait(100)
    # prog.communicate()
    # print(prog)
