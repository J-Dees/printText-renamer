import os
import time

class Instrument:
    def __init__(self, name, type, path):
        self.name = name
        self.type = type
        self.path = path
        self.running = 0

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name
    
    def run(self):
        self.running = 1
        print("Running " + self.name + "...")

    def stop(self):
        self.running = 0

def load():
    '''Load file paths and instrument/software data. If none exists for either, the user will be prompted to create them.'''
    instruments = []
    try:
        with open(os.path.join("instruments"), 'r') as f:
            inst_data = f.readlines()
            if inst_data == []:
                raise FileNotFoundError
            for i in range(len(inst_data)):
                inst_data[i] = inst_data[i].strip().split('=')
    except FileNotFoundError:
        print("No instruments found. Please add instrument(s).")
        inst_data = add_instrument()
    except:
        print("Error loading instruments. Please check instruments file.")
        exit()
    try:
        with open(os.path.join("paths"), 'r') as f:
            path_data = f.readlines()
            if path_data == []:
                raise FileNotFoundError
            for i in range(len(path_data)):
                path_data[i] = path_data[i].strip().split('=')
            for inst in inst_data:
                if inst[0] == path[0]:
                    inst.append(path[1])
    except FileNotFoundError:
        print("No file paths found. Please add path(s).")
        for inst in inst_data:
            path = add_path(inst[0])
            inst.append(path)
    except:
        print("Error loading file paths. Please check file paths file.")
        exit()
    
    instruments = [Instrument(inst[0], inst[1], inst[2]) for inst in inst_data]

    # verify that each instrument has a path
    for instrument in instruments:
        if instrument.path == None:
            print("No file path found for " + instrument.name + ". Please add the file path.")
            instrument.path = add_path(instrument.name)
    return instruments

def add_instrument():
    instruments = []
    cont = ''
    while cont.lower() != 'n':
        instrument = input("Enter an instrument name to add: ")
        type = input("Enter the software type for " + instrument + ": ")
        instruments.append([instrument, type])
        cont = input("Add another instrument? (y/n): ")
    with open(os.path.join("instruments"), 'a') as f:
        for instrument in instruments:
            f.write(instrument[0] + "=" + instrument[1] + "\n")
    return instruments

def add_path(instrument):
    path = input("Enter the file path for " + instrument + ": ")
    # verify that the path is valid
    while not os.path.exists(path):
        print("Invalid path. Please try again.")
        path = input("Enter the file path for " + instrument + ": ")
    with open(os.path.join("paths"), 'a') as f:
        f.write(instrument + "=" + path + "\n")
    return path

def print_menu(instruments):
    title = "Auto File Renamer"
    print("=" * (32 + len(title)))
    print("\t\t" + title)
    print("=" * (32 + len(title)))
    print("\nChoose Instrument:")
    for i in range(len(instruments)):
        print(str(i + 1) + ". " + instruments[i].name, end=' ')
        if instruments[i].running:
            print("(Running)")
        else:
            print()
    print("\n" + "-" * (32 + len(title)) + "\nX. Exit\nAdd. Add Instrument\n")

def main(instruments):
    print_menu(instruments)
    choice = input()
    while choice.lower() != 'x':
        if choice.lower() == 'add':
            os.system('cls')
            new_instruments = add_instrument()
            for inst in new_instruments:
                path = add_path(inst[0])
                inst.append(path)
            instruments += [Instrument(inst[0], inst[1], inst[2]) for inst in new_instruments]
            os.system('cls')
            print_menu(instruments)
            choice = input()
            continue
        try:
            choice = int(choice)
            if choice < 1 or choice > len(instruments):
                raise ValueError
        except ValueError:
            print("Invalid choice. Please enter to continue.")
            input()
            os.system('cls')
            print_menu(instruments)
            choice = input()
            continue
        instrument = instruments[choice - 1]
        instrument.running = 1
        print("Running " + instrument.name + "...")
        time.sleep(2)
        os.system('cls')
        print_menu(instruments)
        choice = input()

if __name__ == "__main__":
    os.system('cls')
    print("Loading...")
    time.sleep(1)
    instruments = load()
    print('Instruments and file paths loaded.')
    time.sleep(1)
    os.system('cls')
    main(instruments)