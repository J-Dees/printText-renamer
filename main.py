import os
import time
import re
from process import process_instrument
from multiprocessing import Process

class Instrument:

    CHEMSTATION = 0
    PEAKSIMPLE = 1

    def __init__(self, name, type, path):
        self.name = name
        self.type = type
        self.path = path
        self.running = 0
        self.process = None

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
                inst_data[i] = re.split(':|,', inst_data[i], maxsplit=2)
                inst_name = inst_data[i][0]
                inst_type = inst_data[i][1]
                inst_path = inst_data[i][2]
                instruments.append(Instrument(inst_name, int(inst_type[inst_type.find('=') + 1:]), inst_path[inst_path.find('=') + 1:]))
    except FileNotFoundError:
        print("No instruments found. Please add instrument(s).")
        instruments += add_instrument()
    except:
        print("Error loading instruments. Please check instruments file.")
        time.sleep(2)
        print("Exiting...")
        exit()

    return instruments

def save_instruments(instruments):
    with open(os.path.join("instruments"), 'w') as f:
        for instrument in instruments:
            f.write(instrument.name + ":type=" + str(instrument.type) + ",path=" + instrument.path + "\n")

def add_instrument():
    try:
        instruments = []
        cont = ''
        while cont.lower() != 'n':
            inst_name = input("Enter an instrument name to add: ")
            print("Enter the software type for " + inst_name + ".")
            inst_type = input("0. ChemStation\n1. PeakSimple\n")
            while inst_type not in ['0', '1']:
                print("Invalid choice. Please try again.")
                inst_type = input("0. ChemStation\n1. PeakSimple\n")
            inst_type = int(inst_type)
            inst_path = input("Enter the file path for " + inst_name + ": ")
            while not os.path.exists(inst_path):
                print("Invalid path. Please try again.")
                inst_path = input("Enter the file path for " + inst_name + ": ")
            instruments.append(Instrument(inst_name, inst_type, inst_path))
            cont = input("Add another instrument? (y/n): ")
        with open(os.path.join("instruments"), 'a') as f:
            for instrument in instruments:
                f.write(instrument.name + ":type=" + str(instrument.type) + ",path=" + instrument.path + "\n")
        return instruments
    except Exception as e:
        print("Error adding instruments. Please try again.")
        log("Error adding instruments: " + str(e))
        time.sleep(2)
        return []

def toggle_instrument(instrument):
    try:
        if instrument.running:
            if instrument.process.is_alive():
                instrument.process.terminate()
            instrument.running = 0
            print("Stopping " + instrument.name + "...")
            log(instrument.name + " Stopped")
        else:
            p = Process(target=process_instrument, args=(instrument,))
            p.start()
            instrument.process = p
            instrument.running = 1
            print("Running " + instrument.name + " with process " + str(instrument.process.pid) + "...")
            log(instrument.name + " Started: " + str(instrument.process.pid))
    except Exception as e:
        log("Error toggling instrument: " + str(e))

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
    print("\n" + "-" * (32 + len(title)) + "\nX. Exit\nAdd. Add Instrument\nRm. Remove Instrument\n")

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
        elif choice.lower() == 'rm':
            remove = input("Choose an instrument to remove: ")
            instruments.pop(int(remove) - 1)
            save_instruments(instruments)
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
        # create process for pdf renaming here
        toggle_instrument(instruments[choice - 1])
        time.sleep(2)
        os.system('cls')
        print_menu(instruments)
        choice = input()
    for instrument in instruments:
        if instrument.running:
            if instrument.process.is_alive():
                instrument.process.terminate()

def log(string):
    with open("log.txt", 'a') as f:
        f.write(string + "\n")

if __name__ == "__main__":
    os.system('cls')
    print("Loading...")
    time.sleep(1)
    instruments = load()
    print('Instruments successfully loaded.')
    time.sleep(1)
    os.system('cls')
    main(instruments)