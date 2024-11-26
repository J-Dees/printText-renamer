# printText-renamer

A simple program to automate file renaming for ChemStation printText files on GCSCD3.

Uses watchdog to handle and create sys alarms that monitor folder changes. See example pdf for file format. This script will open a pdf that is default named to 'PrintText.pdf" and placed in the target path, look at the fourth line of text that contains the data file name, parse out the data file name, and rename the pdf to 'PrintText{data_file}.pdf'.

The required modules are listed in requirements.txt. Use `pip install {module}` to install the necessary modules.

target path: `C:\Users\oilgas\Desktop\PDF`

### To Expand On:
- PyPDF2 allows for merging of files, this means that the corresponding quant file can be merged with the PrintText to consolidate the number of files being created
- It would be good practice to set up a testbench for this program
- Set up logging
