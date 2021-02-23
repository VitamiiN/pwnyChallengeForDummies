
import os
import subprocess
from pathlib import Path
import sys

def printUsage(suppliedDupArgs=False):
    if suppliedDupArgs == False:
        print("Usage: pyps.py arg1 arg2")
    else:
        print("Error: supplied duplicate args.")
        print("Usage: pyps.py arg1 arg2")

    sys.exit()

def main():
    p = Path("/proc/")

    fullFormat = False
    allProc = False

    if "-h" in sys.argv or "--help" in sys.argv:
        printUsage()

    for param in sys.argv:
        if param == "-f":
            if fullFormat == False:
                print("UID\t\tPID\tPPID\tCMD")
                fullFormat = True
            else:
                printUsage(suppliedDupArgs=True)
        elif param == "-A":
            if allProc == True:
                printUsage(suppliedDupArgs=True)
            allProc = True

    if fullFormat == False:
        print("PID\tCMD")


    for child in p.iterdir():
        if child.is_dir() and child.name.isdigit():
            with open(str(child) + "/status", "r") as proc_info:
                data = proc_info.read()
                pid = data.split("Pid:")[1].split("\n")[0].replace("\t", "")
                uid = data.split("Uid:")[1].split("\n")[0].split("\t")[1].replace("\t", "")
                ppid = data.split("PPid:")[1].split("\n")[0].split("\t")[1].replace("\t", "")
                self_euid = os.geteuid()
                fullCmdName = open(str(child) + "/cmdline", "r").read().replace("\n", "").replace("\0"," ")
                cmdName = open(str(child) + "/comm", "r").read().replace("\n", "")

                if fullCmdName == "":
                    fullCmdName = "[" + cmdName + "]"

                original_tty = open("/proc/" + str(os.getpid()) + "/stat").read().split(" ")[7]
                tty = open(str(child) + "/stat", "r").read().split(" ")[7]

                username = ""

                with open("/etc/passwd", "r") as etc_passwd:
                    for line in etc_passwd.readlines():
                        if line.split(":")[2] == uid:
                            username = line.split(":")[0]
                if len(username) > 7:
                    username = username[:7] + "+"
            if allProc == False:
                if int(self_euid) == int(uid) and tty != "0" and tty != "-1" and tty == original_tty:
                    if fullFormat == False:
                        print(pid + "\t" + cmdName)
                    else:
                        print(username + "\t" + pid + "\t" + ppid + "\t" + fullCmdName)
            else:
                if fullFormat == False:
                    print(pid + "\t" + cmdName)
                else:
                    print(username + "\t" + pid + "\t" + ppid + "\t" + fullCmdName)


if __name__ == '__main__':
    main()
