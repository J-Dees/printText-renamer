import os
import time
import re
from process import process_instrument
from multiprocessing import Process

class Instrument:
    """
    This class represents an instrument computer that will be monitored for new PDF files.

    name (str): The name of the instrument.
    itype (int): The type of software used by the instrument (0 for ChemStation, 1 for PeakSimple).
    path (str): The file path to the instrument computer's PDF file.
    running (int): A flag to indicate whether the instrument is currently running.
    process (Process): The process that will monitor the instrument for new PDF files.
    """

    def __init__(self, name, itype, path):
        self.name = name
        self.itype = itype
        self.path = path
        self.running = 0
        self.process = None

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name
    
    def toggle(self):
        """
        Toggles the instrument to start or stop running.
        Starting the instrument will create a new process to monitor the instrument for new PDF files.
        Stopping the instrument will terminate the process.
        """
        try:
            if self.running:
                if self.process.is_alive():
                    self.process.terminate()
                self.running = 0
                print("Stopping " + self.name + "...")
                log(self.name + " Stopped")
            else:
                # generates a new process and stores it in the instrument object
                p = Process(target=process_instrument, args=(self.name, self.itype, self.path))
                p.start()
                self.process = p
                self.running = 1
                print("Running " + self.name + " with process " + str(self.process.pid) + "...")
                log(self.name + " Started: " + str(self.process.pid))
        except Exception as e:
            log("Error toggling instrument: " + str(e))

def load():
    """
    Loads instrument data from the instruments file into an array of Instrument objects. 
    If the instruments file does not exist, the user will be prompted to create new instrument(s).
    """
    instruments = []
    try:
        with open(os.path.join("instruments"), 'r') as f:
            inst_data = f.readlines()
            if inst_data == []:
                raise FileNotFoundError
            for i in range(len(inst_data)):
                inst_data[i] = inst_data[i].strip()
                # ex inst_data[i] = "name:type=0,path=C:\path\to\file", maxsplit used to prevent the path from being split
                inst_data[i] = re.split(':|,', inst_data[i], maxsplit=2)
                inst_name = inst_data[i][0]
                inst_type = inst_data[i][1]
                inst_path = inst_data[i][2]
                instruments.append(Instrument(inst_name, int(inst_type[inst_type.find('=') + 1:]), inst_path[inst_path.find('=') + 1:]))
    except FileNotFoundError:
        print("No instruments found. Please add instrument(s).")
        instruments += add_instrument()
    except Exception as e:
        print("Error loading instruments. Please check instruments file.")
        log("Error loading instruments: " + str(e))
        time.sleep(2)
        print("Exiting...")
        exit()

    return instruments

def save_instruments(instruments):
    """
    Overwrites the instruments file with an updated list of instruments after a remove command.
    """
    with open(os.path.join("instruments"), 'w') as f:
        for instrument in instruments:
            f.write(instrument.name + ":type=" + str(instrument.itype) + ",path=" + instrument.path + "\n")

def add_instrument():
    """
    Adds one or more instruments to the instruments file and returns a list of the new Instrument objects created.
    """
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
            # take as a string to avoid value error from bad input then cast to int
            inst_type = int(inst_type)
            inst_path = input("Enter the file path for " + inst_name + ": ")
            # validate that path exists before adding
            while not os.path.exists(inst_path):
                print("Invalid path. Please try again.")
                inst_path = input("Enter the file path for " + inst_name + ": ")
            instruments.append(Instrument(inst_name, inst_type, inst_path))
            cont = input("Add another instrument? (y/n): ")
        with open(os.path.join("instruments"), 'a') as f:
            for instrument in instruments:
                f.write(instrument.name + ":type=" + str(instrument.itype) + ",path=" + instrument.path + "\n")
        return instruments
    except Exception as e:
        print("Error adding instruments. Please try again.")
        log("Error adding instruments: " + str(e))
        time.sleep(2)
        return []

def print_menu(instruments):
    """
    Prints the main menu with a list of instruments and their running status.
    """
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
            # prints new line
            print()
    print("\n" + "-" * (32 + len(title)) + "\nX. Exit\nAdd. Add Instrument\nRm. Remove Instrument\n")

def main(instruments):
    print_menu(instruments)
    choice = input()
    while choice.lower() != 'x':
        if choice.lower() == 'add':
            os.system('cls')
            # append new instrument(s)
            instruments += add_instrument()
            os.system('cls')
            print_menu(instruments)
            choice = input()
            continue
        elif choice.lower() == 'rm':
            remove = input("Choose an instrument to remove: ")
            # pop selection and then overwrite instruments file
            try:
                remove = int(remove)
                if remove < 1 or remove > len(instruments):
                    raise ValueError
            except ValueError:
                print("Invalid choice. Press enter to continue.")
                input()
                os.system('cls')
                print_menu(instruments)
                choice = input()
                continue
            instruments.pop(remove - 1)
            save_instruments(instruments)
            os.system('cls')
            print_menu(instruments)
            choice = input()
            continue
        try:
            # handle invalid inputs
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
        # toggle selection on/off
        instrument.toggle()
        time.sleep(2)
        os.system('cls')
        print_menu(instruments)
        choice = input()
    # upon exit, terminate all running instrument processes
    for instrument in instruments:
        if instrument.running:
            if instrument.process.is_alive():
                instrument.process.terminate()

def log(string):
    """
    Performs logging to a log file.
    """
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