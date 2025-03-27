# Automatic PDF Renamer

A simple program to automate file renaming for ChemStation and PeakSimple data files.

### Installation Instructions
- Download the code and extract to the desired location
- Ensure python is installed on the computer
- Use `pip install -r requirements.txt` in the program folder to install the required modules
- *(optional)* Send a shortcut of `main.py` to the desktop
- Run `main.py`

### Initial Setup
Upon startup, the program will try to load instrument data from the instruments file. If this is the first time running the program, the file will not exist yet and you will be prompted to enter one or more instrument.
- Enter the desired isntrument name
- Select the type of instrument software **(0 for ChemStation, 1 for PeakSimle)**
- Enter the path to the destination where you will be printing PDFs of data files

### How to Use
- Select an instrument to run, a new process will be created to handle PDF renaming for that computer
- Enter `X` to exit the program, all processes will be terminated prior to exiting
- Enter `Add` to add one or more instruments
- Enter `Rm` to remove an instrument
