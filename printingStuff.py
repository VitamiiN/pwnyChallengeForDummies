# printing all the stuff. This was hard. I'm stupid af.
# Please ignore all of this. It's messy, it's not meant to be read. It's the dirtiest
# code I've ever written but it works. There is repeating code here. I know.

def printStuff(data,isAllProc=False, isNoSessLeaders=False, isFullFormat=False):
    if isAllProc == False:
        if isNoSessLeaders == False:
            if int(data["self_euid"]) == int(data["uid"]) and data["tty"] != "0" and data["tty"] != "-1" and data["tty"] == data["original_tty"]:
                if isFullFormat == False:
                    print(data["pid"] + "\t" + data["cmdName"])
                else:
                    if "+" in data["username"]:
                        print(data["username"] + "\t" + data["pid"] + "\t" + data["ppid"] + "\t" + data["fullCmdName"])
                    else:
                        print(data["username"] + "\t\t" + data["pid"] + "\t" + data["ppid"] + "\t" + data["fullCmdName"])
        else:
            if data["sessionId"] != data["pid"]:
                if isFullFormat == False:
                    print(data["pid"] + "\t" + data["cmdName"])
                else:
                    if "+" in data["username"]:
                        print(data["username"] + "\t" + data["pid"] + "\t" + data["ppid"] + "\t" + data["fullCmdName"])
                    else:
                        print(data["username"] + "\t\t" + data["pid"] + "\t" + data["ppid"] + "\t" + data["fullCmdName"])
    else:
        if isFullFormat == False:
            print(data["pid"] + "\t" + data["cmdName"])
        else:
            if "+" in data["username"]:
                print(data["username"] + "\t" + data["pid"] + "\t" + data["ppid"] + "\t" + data["fullCmdName"])
            else:
                print(data["username"] + "\t\t" + data["pid"] + "\t" + data["ppid"] + "\t" + data["fullCmdName"])
