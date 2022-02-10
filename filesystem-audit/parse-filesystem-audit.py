#!/usr/bin/env python3

filename = "filesystem-audit.log"

items = []
current = None

with open(filename) as file:
    for line in file:
        # SKIP EMPTY LINES
        if len(line.strip()) == 0:
            pass

        # INFORMATION (START ITEM)
        if line.startswith("Information"):
            current = {
                    'Accesses': [],
                    }

        # ACCESS MASK (END ITEM)
        elif line.startswith("\tAccess Mask:"):
            items.append(current)

        # ACESS REQUEST INFORMATION
        elif line.startswith("\tAccesses:") or line.startswith("\t\t\t\t"):
            access = line.removeprefix("\tAccesses:").strip()
            if len(access) > 0:
                current["Accesses"].append(access)

        # GENERAL
        elif line.startswith("\t"):
            split = line.split(':', 1)
            key = split[0].strip()
            value = split[1].strip()
            current[key] = value

# List all items
def list_all():
    for item in items:
        for key in item:
            print(key, ':', item[key])
        print()

# List all files and access types directly accessed by C:\Users\exper\Desktop\OwOGame.exe
def list_OwOGame_Accesses():
    for item in items:
        if item['Process Name']:
            print('Accesses', ':', item['Accesses'])
            print('Object Name', ':', item['Object Name'])
            print()

# List all files read by C:\Users\exper\Desktop\OwOGame.exe
def list_OwOGame_Reads():
    for item in items:
        if item['Process Name'] and 'ReadData (or ListDirectory)' in item['Accesses']:
            print(item['Object Name'])

# List all files written to by C:\Users\exper\Desktop\OwOGame.exe
def list_OwOGame_Writes():
    for item in items:
        if item['Process Name'] and 'WriteData (or AddFile)' in item['Accesses']:
            print(item['Object Name'])

print("Please edit the script to uncomment the filters you want to view")

#list_all()
#list_OwOGame_Accesses()
#list_OwOGame_Reads()
#list_OwOGame_Writes()
