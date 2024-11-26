import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from PyPDF2 import PdfReader

pdf_folder = r'C:\Users\oilgas\Desktop\PDF'

# given a line with the filename in it, parse out only the filename
# the target PDF has a 4th line: 'Data File : {file_name}
def parse_filename(line):
  return 'PrintText' + line.split(':')[1].strip()

# extract file title from PDF using PyPDF2
def extract_title(pdf_path):
  try:
    reader = PdfReader(pdf_path)
    if reader.pages:
      first_page = reader.pages[0]
      lines = first_page.extract_text().splitlines()
      return parse_filename(lines[3].strip())
  except Exception as e:
    print(f"Error reading {pdf_path}: {e}")
  return None
    
# process files as they are added to PDF folder only when the name of the PDF is 'printText'
def process_pdf(file_path):
  if not file_path.endswith("PrintText.pdf"):
    return

  max_retries = 5
  for attempt in range(max_retries):
    try:
      new_name = extract_title(file_path)
      if new_name:
        new_path = os.path.join(pdf_folder, f"{new_name}.pdf")
        if not os.path.exists(new_path):
          os.rename(file_path, new_path)
          print(f"File successfully renamed to {new_name}.")
        else:
          print(f"File with name {new_name} already exists.")
        break
      else:
        print(f"Could not extract name from {file_path}")
    except Exception as e:
      print(f"Attempt {attempt + 1} failed for {file_path}: {e}")
      time.sleep(1)

# create a watchdog class that handles new PDF files
class PDFHandler(FileSystemEventHandler):
  def on_created(self, event):
    if event.is_directory:
      return
    process_pdf(event.src_path)

if __name__ == '__main__':
  # add logging to monitor performance
  event_handler = PDFHandler()
  observer = Observer()
  observer.schedule(event_handler, pdf_folder, recursive=False)
  observer.start()

  # automatically run until process is terminated
  try:
    while True:
      time.sleep(1)
  except KeyboardInterrupt:
      observer.stop()

  observer.join()
