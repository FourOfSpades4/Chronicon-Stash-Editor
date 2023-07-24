from chronicon import Stash
from os import system
from time import sleep

f = None

def main():
    global f
    system("cls")
    print("Chronicon Stash Editor")
    f = getFileLocation()
    print("Loading Stash. Please wait, this may take a minute.")
    stash = Stash(f)
    print("Stash Loaded.")
    sleep(1)
    start(stash)

def getFileLocation():
    f = input("Enter File Location: ")
    f.strip("\"")
    return f

def start(stash: Stash):
    system("cls")
    print("Chronicon Stash Editor")
    print(f"Version: {stash.version}")
    print(f"Size:    {stash.size}")
    print()
    # print("Commands:")
    # print("list all:                    List All Items")
    # print("list page [number]:          List Items on Stash Page")
    # print("list items [start] [stop]:   List Items Between Indicies")
    # print("edit [item number]:          Edit Item")
    # # print("copy [item number]:          Copy Item to First Empty Slot")
    # # print("copy [item] [dest]:          Copy Item to Destination")
    # print("write:                       Save Changes")

    process_command(stash, input("> "))
    while True:
        process_command(stash, input("> "))

def process_command(stash: Stash, command: str):
    command = tokenize(command)
    if (command[0] == "list"):
        list(stash, command)
    elif (command[0] == "edit"):
        edit(stash, command)
    # if (command[0] == "copy"):
    #     copy(stash, command)
    elif (command[0] == "write"):
        stash.write_to_file(f)
        system("cls")
        print("Chronicon Stash Editor")
        print(f"Version: {stash.version}")
        print(f"Size:    {stash.size}")
    elif (command[0] == "clear"):
        system("cls")
        print("Chronicon Stash Editor")
        print(f"Version: {stash.version}")
        print(f"Size:    {stash.size}")
    else:
        print("Invalid Command")


def edit_item(item):
    command = ""
    while True:
        command = input("> ")
        command = tokenize(command)

        if command[0] == "done":
            break

        if command[0] == "enchants":
            print_item_enchants(item)
            continue

        if command[0] == "sockets":
            print_item_sockets(item)
            continue

        if command[0] == "item":
            print_item(item)
            continue

        if command[0] == "enchant":
            if len(command) == 2:
                if not command[1].isnumeric():
                    print("Error, Invalid Number")
                    continue
                num = int(command[1])
                if int(command[1]) < 1 or int(command[1]) > 10:
                    print("Error, Invalid Number")
                    continue

                print_item_enchant(item, int(command[1]))
            
            elif len(command) == 4:
                if not command[1].isnumeric():
                    print("Error, Invalid Number")
                    continue
                
                if not edit_item_enchant(item, command):
                    print("Error, Invalid Command")
                else:
                    print_item_enchant(item, int(command[1]))

            else:
                print("Error, Invalid Command")

            continue


        if command[0] == "socket":
            if len(command) == 2:
                if not command[1].isnumeric():
                    print("Error, Invalid Number")
                    continue
                num = int(command[1])
                if int(command[1]) < 1 or int(command[1]) > 6:
                    print("Error, Invalid Number")
                    continue

                print_item_socket(item, int(command[1]))
            
            elif len(command) == 4:
                if not command[1].isnumeric():
                    print("Error, Invalid Number")
                    continue
                
                if not edit_item_socket(item, command):
                    print("Error, Invalid Command")

                else:
                    print_item_socket(item, int(command[1]))

            else:
                print("Error, Invalid Command")

            continue

        match command[0]:
            case "quanity": command[0] = "qt"
            case "damage": command[0] = "dmg"
            case "health": command[0] = "hp"
            case "mana": command[0] = "mp"
            case "stamina": command[0] = "stam"

        stat = item.get_stat(command[0])

        if stat == None:
            print("Error, Invalid Key")
            continue

        if stat.type == 0:
            value = stat.value
            try:
                value = float(command[1])
            except ValueError:
                print("Error, Invalid Value")
                continue
        else:
            value = command[1]
        
        stat.value = value

        print_item(item)
    
    system("cls")
    print("Chronicon Stash Editor")

def edit(stash: Stash, command):
    if len(command) < 2:
        print("Invalid Number of Arguements. ")
        print("edit [item number] requires 1 integer.")
        return False
    
    if not command[1].isnumeric():
        print("Invalid Arguements. ")
        print("copy [item number] requires 1 integer.")
        return False
    
    item = stash.items[int(command[1]) - 1]
    
    if item.get_name() == None:
        print("Invalid Arguements. ")
        print("Item could not be found.")
        return False

    print_item(item)
    edit_item(item)

def print_item(item):
    system("cls")
    if item.get_stat('qt').value > 0:
        isEquip = False
    else:
        isEquip = True
    
    print("Chronicon Stash Editor")
    if not isEquip:
        print(f"{item.get_name()}")
        print()
        print(f"ID:      {item.get_stat('id')}")
        print(f"Type:    {item.get_stat('type')}")
        print(f"Quanity: {item.get_stat('qt')}")
        print(f"Quality: {item.get_stat('quality')}")
        print()
    
    else:
        print(f"{item.get_name()}")
        print()
        print(f"ID:           {item.get_stat('id')}")
        print(f"Type:         {item.get_stat('type')}")
        print(f"Quality:      {item.get_stat('quality')}")
        print(f"Level:        {item.get_stat('level')}")
        print()
        print(f"Damage:       {item.get_stat('dmg')}")
        print(f"Health:       {item.get_stat('hp')}")
        print(f"Mana:         {item.get_stat('mp')}")
        print(f"Stamina:      {item.get_stat('stam')}")
        print(f"Attack Speed: {item.get_stat('attackspeed')}")
        print(f"Crit Chance:  {item.get_stat('crit')}")
        print()


def print_item_enchants(item):
    system("cls")
    print("Chronicon Stash Editor")

    print(f"{item.get_name()}")
    print()
    for i in range(10):
        print(f"{i + 1}:     ", end = "")
        if i < 9:
            print(" ", end="")
        print(item.get_stat('enchant' + str(i)))


def print_item_enchant(item, number):
    system("cls")
    print("Chronicon Stash Editor")

    print(f"{item.get_name()}")
    print()
    print(f"Enchant {number}:      {item.get_stat('enchant' + str(number - 1))}")
    print(f"Power   {number}:      {item.get_stat('enchant_value' + str(number - 1))}")
    print(f"Innate  {number}:      {item.get_stat('enchant_solid' + str(number - 1))}")
    print(f"Rune    {number}:      {item.get_stat('enchant_rune' + str(number - 1))}")
    print(f"Locked  {number}:      {item.get_stat('enchant_locked' + str(number - 1))}")


def edit_item_enchant(item, command):
    if not command[1].isnumeric():
        return False
    
    if command[2] not in ["enchant", "power", "innate", "rune", "locked"]:
        return False

    if not command[3].isnumeric():
        return False

    num = int(command[1])

    if num < 1 or num > 10:
        return False

    match command[2]:
        case "enchant": 
            item.change_stat('enchant' + str(num - 1), int(command[3]))
            return True
        case "power": 
            item.change_stat('enchant_value' + str(num - 1), int(command[3]))
            return True
        case "innate": 
            item.change_stat('enchant_solid' + str(num - 1), int(command[3]))
            return True
        case "rune": 
            item.change_stat('enchant_rune' + str(num - 1), int(command[3]))
            return True
        case "locked": 
            item.change_stat('enchant_locked' + str(num - 1), int(command[3]))
            return True
    
    return False
    

def print_item_sockets(item):
    system("cls")
    print("Chronicon Stash Editor")

    print(f"{item.get_name()}")
    print()
    for i in range(6):
        print(f"{i + 1}:     ", end = "")
        if i < 9:
            print(" ", end="")
        print(item.get_stat('socket_gem' + str(i)))



def print_item_socket(item, number):
    system("cls")
    print("Chronicon Stash Editor")

    print(f"{item.get_name()}")
    print()
    print(f"Gem       {number}:      {item.get_stat('socket_gem' + str(number - 1))}")
    print(f"Value     {number}:      {item.get_stat('socket_val' + str(number - 1))}")
    print(f"Type      {number}:      {item.get_stat('socket_type' + str(number - 1))}")
    print(f"Prismatic {number}:      {item.get_stat('socket_prismatic' + str(number - 1))}")


def edit_item_socket(item, command):
    if not command[1].isnumeric():
        return False

    if not command[3].isnumeric():
        return False

    num = int(command[1])

    if num < 1 or num > 6:
        return False

    match command[2]:
        case "gem": 
            item.change_stat('socket_gem' + str(num - 1), int(command[3]))
            return True
        case "value": 
            item.change_stat('socket_val' + str(num - 1), int(command[3]))
            return True
        case "type": 
            item.change_stat('socket_type' + str(num - 1), int(command[3]))
            return True
        case "prismatic": 
            item.change_stat('socket_prismatic' + str(num - 1), int(command[3]))
            return True
    
    return False


def copy(stash: Stash, command):
    if len(command) == 2:
        if not command[1].isnumeric():
            print("Invalid Arguements. ")
            print("copy [item number] requires 1 integer.")
            return False
        
        i = int(command[1])

        if not isValidIndex(stash, i):
            print("Invalid Arguements.")
            print("Item Not Found")
            return False

        for index, item in enumerate(stash.items):
            if item.get_name() == None:
                stash.items[index] = stash.items[i]
                return True
        
        print("No Empty Slots.")
        return False

    elif len(command) == 3:
        if not command[1].isnumeric() or command[2].isnumeric():
            print("Invalid Arguements. ")
            print("copy [item] [dest] requires 2 integers.")
            return False

        item = int(command[1])
        dest = int(command[2])

        if not isValidIndex(stash, item) or not isValidIndex(stash, dest):
            print("Invalid Arguements.")
            print("Item Not Found")
            return False

        stash.items[dest] = stash.items[item]
        return True

    else:
        print("Invalid Command.")
        print("copy [item number]:          Copy Item to First Empty Slot")
        print("copy [item] [dest]:          Copy Item to Destination")
        return False



def list(stash: Stash, command):
    def listItemsByIndex(stash: Stash, start: int, end: int):
        lastItemWasNone = False

        start = max(0, start)
        start = min(stash.size, start)
        end = min(stash.size, end)
        for index in range(start, end):
            item = stash.items[index]
            name = item.get_name()
            if name != None:
                print(f"{index + 1}: {name}")
                lastItemWasNone = False
            else:
                if not lastItemWasNone:
                    print()
                lastItemWasNone = True

    if (command[1] == "all"):
        listItemsByIndex(stash, 0, stash.size)
        return True

    elif (command[1] == "items"):
        if len(command) < 4:
            print("Invalid Number of Arguements. ")
            print("list items [start] [stop] requires 2 integers.")
            return False
        if not command[2].isnumeric() or not command[3].isnumeric():
            print("Invalid Arguements. ")
            print("list items [start] [stop] requires 2 integers.")
            return False
            
        listItemsByIndex(stash, int(command[2]) - 1, int(command[3]))
        return True

    elif (command[1] == "page"):
        if len(command) < 3:
            print("Invalid Number of Arguements. ")
            print("list page [number] requires 1 integer.")
            return False
        if not command[2].isnumeric():
            print("Invalid Arguements. ")
            print("list page [number] requires 1 integer.")
            return False

        listItemsByIndex(stash, (int(command[2]) - 1) * 80, int(command[2]) * 80)
        return True

    else:
        print("Invalid Command.")
        print("list all:                    List All Items")
        print("list page [number]:          List Items on Stash Page")
        print("list items [start] [stop]:   List Items Between Indicies")
        return False


def isValidIndex(stash, index):
    return index >= 1 and index <= stash.size

def tokenize(command: str):
    return [s.strip().lower() for s in command.split(" ")]

if __name__ == "__main__":
    main()