
import os
import subprocess
from pathlib import Path
import sys
import printingStuff

def printUsage(suppliedDupArgs=False, suppliedNEArgs=False):
    if suppliedDupArgs == True:
        print("Error: supplied duplicate args.")
    if suppliedNEArgs == True:
        print("Error: supplied non existing args.")

    print("Usage: python3 pyps.py arg1 arg2")

    sys.exit()


def main():
    p = Path("/proc/")

    fullFormat = False
    allProc = False
    noSessLeaders = False
    onlyThoseWithTTY = False

    if "-h" in sys.argv or "--help" in sys.argv:
        printUsage()

    for param in sys.argv[1:]:
        if param == "-f":
            if fullFormat == False:
                print("UID\t\tPID\tPPID\tCMD")
                fullFormat = True
            else:
                printUsage(suppliedDupArgs=True)
        elif param == "-e":
            if allProc == True:
                printUsage(suppliedDupArgs=True)
            allProc = True
        elif param == "-d":
            if noSessLeaders == True:
                printUsage(suppliedDupArgs=True)
            noSessLeaders = True
        else:
            printUsage(suppliedNEArgs=True)


    if fullFormat == False:
        print("PID\tCMD")

    # iterate over every item in the directory
    for child in p.iterdir():
        if child.is_dir() and child.name.isdigit():
            with open(str(child) + "/status", "r") as proc_info:
                data = proc_info.read()
                # Retrieve process ID
                pid = data.split("Pid:")[1].split("\n")[0].replace("\t", "")
                # Retrieve User ID of the user who initiated the process
                uid = data.split("Uid:")[1].split("\n")[0].split("\t")[1].replace("\t", "")
                # Retrieve the parent process ID
                ppid = data.split("PPid:")[1].split("\n")[0].split("\t")[1].replace("\t", "")

            # Retrieve the effective user ID of the current process (pyps.py)
            self_euid = os.geteuid()
            # Retrieve the full command line used to initiate the process
            fullCmdName = open(str(child) + "/cmdline", "r").read().replace("\n", "").replace("\0"," ")
            # Only retireve the command name used to initiate the process, without arguments.
            cmdName = open(str(child) + "/comm", "r").read().replace("\n", "")
            # Retrieve a number representing the TTY of the process
            original_tty = open("/proc/" + str(os.getpid()) + "/stat").read().split(" ")[7]
            # Retrieve a number representing the TTY of the CURRENT process.
            tty = open(str(child) + "/stat", "r").read().split(" ")[7]
            username = ""
            # Retrieve the session ID (SID) of the process
            sessionId = open(str(child) + "/stat", "r").read().split(" ")[5]

            # Later used as printing convention in case the full command name isn't available.
            # In such case, the command name becomes cmdName inside of brackets.
            if fullCmdName == "":
                fullCmdName = "[" + cmdName + "]"

            # From /etc/passwd, we can extract a username based on the UID.
            with open("/etc/passwd", "r") as etc_passwd:
                for line in etc_passwd.readlines():
                    if line.split(":")[2] == uid:
                        username = line.split(":")[0]
            # the original ps program cuts and puts a "+" ahead of usernames that are longer than 7 chars.
            if len(username) > 7:
                username = username[:7] + "+"

            # Data we gathered which we send to the printing function printStuff
            data = {
                "pid": pid, "uid": uid, "ppid": ppid,
                "self_euid": self_euid, "fullCmdName": fullCmdName, "cmdName": cmdName,
                "original_tty": original_tty, "tty":tty, "username": username,
                "sessionId": sessionId
            }
            # Printing everything according to data gathered and arguments specified
            printingStuff.printStuff(data, isAllProc=allProc, isNoSessLeaders=noSessLeaders, isFullFormat=fullFormat)


            # Overall, my coding standards are shit, as you can see. I don't know OOP in Python (only in Java),
            # and the printingStuff function was pure cancer, but I had to write something that works in the time given,
            # and I did. Also, I forgot how to implement optparse / argparse, and I knew I don't have a lot of time for that,
            # so I did something on my own with sys.argv . I liked this assignment. I loved every damn second of the research,
            # less so when it came to writing code. The man pages were the most helpful to me, didn't get much by stracing and ltracing,
            # and live gdb debugging wasn't an option since I only did that a long time ago on the most basic level and forgot
            # pretty much everything.
            # The only internet resource I used was Python documentation pages as per the rules.

            # Thank you for every second reading my shit in Telegram and pretty much anywhere and helping me out.
            # I appreciate that. Yes, yes I will stop be nigger and i will sniff man dem Active Directory traffic.

if __name__ == '__main__':
    main()
