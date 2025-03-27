import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from PyPDF2 import PdfReader

def log(string):
    """
    Performs logging to a log file.
    """
    with open("log.txt", 'a') as f:
        f.write(string + "\n")

def parse_filename(line: str, itype: str) -> str:
  """
  Parses out the name of the file from the 'Data File' line in the PDF.
  Peaksimple files require further processing to extract the file number.
  """
  # ex CS line: 'Data File: P0QC2418.D' where 'P0QC2418.D' is the file name
  # ex PS line: 'Data file: GCTCD182089.CHR ({path})' where '182089' is the file name
  if itype == 'cs':
    return 'PrintText' + line.split(':')[1].strip()
  else:
    text = line.split(':')[1].strip()
    # usual format is either 'instrumentfileno.pdf' or 'instrument_fileno.pdf'
    file_no = text.split('.')[0]
    # check for underscore and split if found
    has_us = file_no.find('_')
    if has_us != -1:
      return file_no.split('_')[1]
    # else return all numbers in the file name
    else:
      return ''.join([i for i in file_no if i.isdigit()])

def extract_title(pdf_path: str, itype: str) -> str:
  """
  Extracts lines from the PDF file with PyPDF2 and searches for the 'Data File' line to extract the file name.
  """
  try:
    reader = PdfReader(pdf_path)
    if reader.pages:
      first_page = reader.pages[0]
      lines = first_page.extract_text().splitlines()
      for line in lines:
        line = line.strip()
        if line.lower().startswith("data file"):
          return parse_filename(line.strip(), itype)
      raise Exception("No 'Data File' line found")
  except Exception as e:
    log(f"Error reading {pdf_path}: {e}")
    return None
    
def process_pdf(file_path: str, itype: str):
  """
  Conditionally processes PDF files as they are created in the specified instrument computer directory.
  """
  # if ChemStation file, skip if not a PrintText.pdf file
  if itype == 'cs' and not file_path.endswith("PrintText.pdf"):
    log(f"\tskipping {file_path}")
    return
  # if PeakSimple file, skip if not a PeakSimple.pdf file
  elif itype == 'ps' and not file_path.endswith("PeakSimple.pdf"):
    log(f"\tskipping {file_path}")
    return
  # sleep to allow PDF file to finish printing
  time.sleep(1)
  # in case of failure, retry up to 5 times
  max_retries = 5
  for attempt in range(max_retries):
    try:
      new_name = extract_title(file_path, itype)
      log("\tnew pdf name: " + new_name)
      if new_name:
        stop = file_path.rfind(os.sep)
        # create new path for renaming with the new name
        new_path = os.path.join(file_path[:stop + 1], f"{new_name}.pdf")
        log("\tpath for new pdf: " + new_path)
        if not os.path.exists(new_path):
          os.rename(file_path, new_path)
          log(f"\tfile successfully renamed to {new_name}")
        else:
          log(f"\tfile with name {new_name} already exists")
        break
      else:
        log(f"\tcould not extract name from {file_path}")
    except Exception as e:
      log(f"\tAttempt {attempt + 1} failed for {file_path}: {e}")
      time.sleep(1)


class CS_PDFHandler(FileSystemEventHandler):
  """
  Handles the renaming of ChemStation PDF files.
  """
  def on_created(self, event):
    if event.is_directory:
      return
    log("\tprocessing: " + event.src_path)
    process_pdf(event.src_path, 'cs')
  
class PS_PDFHandler(FileSystemEventHandler):
  """
  Handles the renaming of PeakSimple PDF files.
  """
  def on_created(self, event):
    if event.is_directory:
      return
    log("\tprocessing: " + event.src_path)
    process_pdf(event.src_path, 'ps')

def process_instrument(instrument):
  """
  Creates a new observer for the given instrument to monitor for new PDF files.
  """
  # add logging to monitor performance
  log("Processing " + instrument.name)
  if instrument.itype == 0:
    event_handler = CS_PDFHandler()
  else:
    event_handler = PS_PDFHandler()
  observer = Observer()
  observer.schedule(event_handler, instrument.path, recursive=False)
  observer.start()

  # automatically run until process is terminated
  try:
    while True:
      time.sleep(1)
  except KeyboardInterrupt:
      observer.stop()

  observer.join()
