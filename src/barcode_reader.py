import os
import cv2
import PyPDF2
from PyPDF2 import PdfReader
from pyzbar.pyzbar import decode
import fitz  # PyMuPDF

from config import properties

class BarcodeReader:
    def __init__(self, pdf_path, output_file_name):
        # Get the directory of the script
        script_dir = os.path.dirname(os.path.abspath(__file__))

        # Construct the absolute path to the PDF file
        self.pdf_path = os.path.join(script_dir, '..', pdf_path)
        self.output_file_name = output_file_name
        self.extracted_text = {}

    def extract_text_from_pdf(self):
        with fitz.open(self.pdf_path) as pdf_document:
            number_of_pages = pdf_document.page_count

            for i in range(number_of_pages):
                page = pdf_document[i]
                page_text = page.get_text()
                self.parse_text(page_text)

    def parse_text(self, text):
        lines = text.split('\n')
        for line in lines:
            if line.strip():
                key_value = line.split(':')
                if len(key_value) == 2:
                    key = key_value[0].strip()
                    value = key_value[1].strip()
                    self.extracted_text[key] = value

    def detect_barcodes_in_pdf(self):
        reader = PdfReader(self.pdf_path)
        page = reader.pages[0]

        for image_file_object in page.images:
            img = cv2.imread(image_file_object)
            detected_barcodes = decode(img)

            for barcode in detected_barcodes:
                if barcode.data != "":
                    print(barcode.data)

    def save_extracted_text_to_file(self):
        output_full_path = os.path.join(properties.OUTPUT_FOLDER, self.output_file_name)
        with open(output_full_path, "w") as output_file:
            for key, value in self.extracted_text.items():
                output_file.write(f"{key}: {value}\n")


if __name__ == "__main__":
    barcode_reader = BarcodeReader(properties.TEST_TASK, properties.EXTRACTED_TEXT_FILE)
    barcode_reader.extract_text_from_pdf()
    print("Extracted Text as Dictionary:")
    print(barcode_reader.extracted_text)
    barcode_reader.detect_barcodes_in_pdf()
    barcode_reader.save_extracted_text_to_file()
    print(f"Extracted text saved to {properties.EXTRACTED_TEXT_FILE} in {properties.OUTPUT_FOLDER}")
