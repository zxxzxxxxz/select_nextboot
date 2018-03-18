import os
import subprocess
import re


def GetBootEntry():
    identifier = {}
    description = {}

    if os.name == "posix":
        proc = subprocess.run("/bin/efibootmgr", stdout=subprocess.PIPE)

        res = proc.stdout.decode()
        res = re.sub("^(?!Boot[0-9]{4}).*$", "", res, flags=re.MULTILINE)
        res = re.sub("^" + os.linesep, "", res, flags=re.MULTILINE)
        res = re.sub(os.linesep + "$", "", res)

        identifier = re.sub("^Boot", "", res, flags=re.MULTILINE)
        identifier = re.sub("(\*| ) .*$", "", identifier, flags=re.MULTILINE)
        identifier = identifier.split(os.linesep)

        description = re.sub("^Boot[0-9]{4}(\*| ) ", "", res, flags=re.MULTILINE)
        description = description.split(os.linesep)

    elif os.name == "nt":
        proc = subprocess.run("bcdedit /enum firmware", stdout=subprocess.PIPE)

        res = proc.stdout.decode()

        identifier = re.sub("^(?!identifier).*$", "", res, flags=re.MULTILINE)
        identifier = re.sub("bootmgr", "", identifier, flags=re.MULTILINE)
        identifier = re.sub("^identifier *", "", identifier, flags=re.MULTILINE)
        identifier = identifier.split(os.linesep)

        description = re.sub("^(?!description).*$", "", res, flags=re.MULTILINE)
        description = re.sub("Windows Boot Manager", "", description, flags=re.MULTILINE)
        description = re.sub("^description *", "", description, flags=re.MULTILINE)
        description = description.split(os.linesep)

    return identifier, description


def SetBootEntry(identifier):
    result = False

    if os.name == "posix":
        proc = subprocess.run("/bin/efibootmgr --bootnext " + identifier)
        result = not bool(proc.returncode)
    elif os.name == "nt":
        proc = subprocess.run("bcdedit /set{fwbootmgr} bootsequence {" + identifier + "}")
        result = not bool(proc.returncode)

    return result


def Reboot():
    result = False

    if os.name == "posix":
        proc = subprocess.run("reboot")
        result = not bool(proc.returncode)
    elif os.name == "nt":
        proc = subprocess.run("shutdown /r /t 0")
        result = not bool(proc.returncode)

    return result


def Main():
    identifier, description = GetBootEntry()
    for i in range(len(identifier)):
        print("[" + str(i) + "] " + description[i])
    num = input()
    SetBootEntry(identifier[num])
    Reboot()


if __name__ == "__main__":
    Main()
