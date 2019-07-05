import sys
from subprocess import Popen

filename = sys.argv[1]
while True:
    print("\nStarting " + filename)
    p = Popen("python " + filename + " -" + sys.argv[2], shell=True)
    p.wait()
