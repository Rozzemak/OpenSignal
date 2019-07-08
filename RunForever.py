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
        p.wait(2)
        p.wait()
    except:
        "(Exception!) Trying to create server again."
    p.wait()
    os.system(
        "runas /savecred /profile /user:slavka \"powershell.exe Stop-Process -ID (Get-Process -Id (Get-NetTCPConnection -LocalPort 5000).OwningProcess).Id -Force\"")
    # prog.communicate()
    # print(prog)
