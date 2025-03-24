import os

instruments = {}
paths = {}

def load():
    '''Load file paths and instrument/software data. If none exists for either, the user will be prompted to create them.'''
    global instruments
    global paths
    try:
        with open(os.path.join("instruments"), 'r') as f:
            lines = f.readlines()
            if lines == []:
                raise FileNotFoundError
            for line in lines:
                line.strip().split('=')
                instruments[line[0]] = line[1]
    except FileNotFoundError:
        print("No instruments found. Please add instrument(s).")
        add_instrument()
        load()
    except:
        print("Error loading instruments. Please check instruments file.")
        exit()
    try:
        with open(os.path.join("paths"), 'r') as f:
            lines = f.readlines()
            if lines == []:
                raise FileNotFoundError
            for line in lines:
                line.strip().split('=')
                paths[line[0]] = line[1]
    except FileNotFoundError:
        print("No file paths found. Please add path(s).")
        for instrument in instruments:
            add_path(instrument)
        load()
    except:
        print("Error loading file paths. Please check file paths file.")
        exit()

    # verify that each instrument has a path
    for instrument in instruments:
        if instrument not in paths:
            print("No file path found for " + instrument + ". Please add the file path.")
            add_path(instrument)

def add_instrument():
    instruments = {}
    cont = ''
    while cont.lower() != 'n':
        instrument = input("Enter an instrument name to add: ")
        type = input("Enter the software type for " + instrument + ": ")
        instruments[instrument] = type
        cont = input("Add another instrument? (y/n): ")
    with open(os.path.join("instruments"), 'a') as f:
        for instrument in instruments:
            f.write(instrument + "=" + instruments[instrument] + "\n")
    return

def main():
    title = "Auto File Renamer"
    print("=" * (32 + len(title)))
    print("\t\t" + title)
    print("=" * (32 + len(title)))
    print("\nChoose Instrument:")

if __name__ == "__main__":
    load()
    main()