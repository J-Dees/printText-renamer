import os
import re
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from PyPDF2 import PdfReader

# Folder to monitor and output folder
pdf_folder = r"C:\path\to\pdfs"
output_folder = r"C:\path\to\output"

# Ensure the output folder exists
os.makedirs(output_folder, exist_ok=True)

def clean_filename(text):
    """Clean text to make it suitable as a filename."""
    return re.sub(r'[<>:"/\\|?*]', '_', text.strip())

def extract_title_from_pdf(pdf_path):
    """Extract the first line of text from the first page of a PDF."""
    try:
        reader = PdfReader(pdf_path)
        if reader.pages:
            first_page = reader.pages[0]
            text = first_page.extract_text()
            for line in text.splitlines():
                if line.strip():
                    return clean_filename(line)
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")
    return None

def process_pdf(file_path):
    """Rename and move a PDF file based on its content."""
    if not file_path.endswith(".pdf"):
        return

    print(f"Processing: {file_path}")
    new_name = extract_title_from_pdf(file_path)
    if new_name:
        new_path = os.path.join(output_folder, f"{new_name}.pdf")
        if not os.path.exists(new_path):
            os.rename(file_path, new_path)
            print(f"Renamed to: {new_name}.pdf")
        else:
            print(f"File with name {new_name}.pdf already exists. Skipping...")
    else:
        print(f"Could not extract a name for: {file_path}")

class PDFHandler(FileSystemEventHandler):
    """Handle file system events."""
    def on_created(self, event):
        if event.is_directory:
            return
        process_pdf(event.src_path)

if __name__ == "__main__":
    # Set up watchdog observer
    event_handler = PDFHandler()
    observer = Observer()
    observer.schedule(event_handler, pdf_folder, recursive=False)

    print(f"Watching folder: {pdf_folder}")
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping...")
        observer.stop()

    observer.join()
