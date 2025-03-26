import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from PyPDF2 import PdfReader

def log(string):
    with open("log.txt", 'a') as f:
        f.write(string + "\n")

# given a line with the filename in it, parse out only the filename
# the target PDF has a 4th line: 'Data File : {file_name}
def parse_filename(line: str, type: str):
  if type == 'cs':
    return 'PrintText' + line.split(':')[1].strip()
  else:
    text = line.split(':')[1].strip()
    file_no = text.split('.')[0]
    has_us = file_no.find('_')
    if has_us != -1:
      return file_no.split('_')[1]
    else:
      return ''.join([i for i in file_no if i.isdigit()])

# extract file title from PDF using PyPDF2
def extract_title(pdf_path, type: str):
  try:
    reader = PdfReader(pdf_path)
    if reader.pages:
      first_page = reader.pages[0]
      lines = first_page.extract_text().splitlines()
      for line in lines:
        if line.startswith("Data File"):
          return parse_filename(line.strip(), type)
      raise Exception("No 'Data File' line found")
  except Exception as e:
    log(f"Error reading {pdf_path}: {e}")
    return None
    
# process files as they are added to PDF folder only when the name of the PDF is 'printText'
def process_pdf(file_path: str, type: str):
  if type == 'cs' and not file_path.endswith("PrintText.pdf"):
    log(f"\tskipping {file_path}")
    return
  elif type == 'ps' and not file_path.endswith("PeakSimple.pdf"):
    log(f"\tskipping {file_path}")
    return

  max_retries = 5
  for attempt in range(max_retries):
    try:
      new_name = extract_title(file_path, type)
      log("\tnew pdf name: " + new_name)
      if new_name:
        stop = file_path.rfind(os.sep)
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
      log(f"Attempt {attempt + 1} failed for {file_path}: {e}")
      time.sleep(1)

# create a watchdog class that handles new PDF files
class CS_PDFHandler(FileSystemEventHandler):
  def on_created(self, event):
    if event.is_directory:
      return
    log("\tprocessing: " + event.src_path)
    process_pdf(event.src_path, 'cs')
  
class PS_PDFHandler(FileSystemEventHandler):
  def on_created(self, event):
    if event.is_directory:
      return
    log("\tprocessing: " + event.src_path)
    process_pdf(event.src_path, 'ps')

def process_instrument(instrument):
  # add logging to monitor performance
  log("Processing " + instrument.name)
  if instrument.type == instrument.CHEMSTATION:
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
