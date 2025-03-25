import os
import time
import re

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
                inst_data[i] = inst_data[i].strip()
                inst_data[i] = re.split(':|,', inst_data[i])
                inst_name = inst_data[i][0]
                inst_type = inst_data[i][1]
                inst_path = inst_data[i][2]
                instruments.append(Instrument(inst_name, inst_type[inst_type.find('=') + 1:], inst_path[inst_path.find('=') + 1:]))
    except FileNotFoundError:
        print("No instruments found. Please add instrument(s).")
        instruments += add_instrument()
    except:
        print("Error loading instruments. Please check instruments file.")
        time.sleep(2)
        print("Exiting...")
        exit()

    return instruments

def add_instrument():
    instruments = []
    cont = ''
    while cont.lower() != 'n':
        inst_name = input("Enter an instrument name to add: ")
        inst_type = input("Enter the software type for " + inst_name + ": ")
        inst_path = input("Enter the file path for " + inst_name + ": ")
        while not os.path.exists(inst_path):
            print("Invalid path. Please try again.")
            inst_path = input("Enter the file path for " + inst_name + ": ")
        instruments.append(Instrument(inst_name, inst_type, inst_path))
        cont = input("Add another instrument? (y/n): ")
    with open(os.path.join("instruments"), 'a') as f:
        for instrument in instruments:
            f.write(instrument.name + ":type=" + instrument.type + ",path=" + instrument.path + "\n")
    return instruments

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
            instruments += add_instrument()
            os.system('cls')
            print_menu(instruments)
            choice = input()
            continue
        try:
            choice = int(choice)
            if choice < 1 or choice > len(instruments):
                raise ValueError
        except ValueError:
            print("Invalid choice. Press enter to continue.")
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
    print('Instruments successfully loaded.')
    time.sleep(1)
    os.system('cls')
    main(instruments)