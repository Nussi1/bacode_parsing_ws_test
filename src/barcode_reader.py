import os

import cv2
import fitz
from PyPDF2 import PdfReader
from pyzbar.pyzbar import decode

from config import Properties


class BarcodeReader:
    def __init__(self, pdf_path, output_file_name):
        # Get the directory of the script
        script_dir = os.path.dirname(os.path.abspath(__file__))

        # Construct the absolute path to the PDF file
        self.pdf_path = os.path.join(script_dir, '..', pdf_path)
        self.output_file_name = output_file_name
        self.extracted_text = {}

    def extract_text_from_pdf(self):
        # Extract text from each page of the PDF
        with fitz.open(self.pdf_path) as pdf_document:
            number_of_pages = pdf_document.page_count

            for i in range(number_of_pages):
                page = pdf_document[i]
                page_text = page.get_text()
                print(f"Page {i + 1} content:")
                print(page_text)
                self.parse_text(page_text)

        print("Extracted Text after extraction:")
        print(self.extracted_text)

    def parse_text(self, text):
        # Parse text into key-value pairs
        lines = text.split('\n')
        print("Lines after splitting:")
        print(lines)

        for line in lines:
            key_value = line.split(':')
            if len(key_value) == 2:
                key = key_value[0].strip()
                value = key_value[1].strip()
                self.extracted_text[key] = value

        print("Extracted Text after parsing:")
        print(self.extracted_text)

    def detect_barcodes_in_pdf(self):
        # Detect barcodes in the first page of the PDF
        reader = PdfReader(self.pdf_path)
        page = reader.pages[0]

        for image_file_object in page.images:
            img = cv2.imread(image_file_object)
            detected_barcodes = decode(img)

            for barcode in detected_barcodes:
                if barcode.data != "":
                    print(barcode.data)

    def save_extracted_text_to_file(self):
        # Save extracted text to the specified file in the Properties
        output_full_path = Properties.EXTRACTED_TEXT_FILE
        with open(output_full_path, "w") as output_file:
            for key, value in self.extracted_text.items():
                output_file.write(f"{key}: {value}\n")


if __name__ == "__main__":
    # Create an instance of BarcodeReader with specified PDF and output file
    barcode_reader = BarcodeReader(Properties.TEST_TASK, Properties.EXTRACTED_TEXT_FILE)

    # Extract text, detect barcodes, and save the extracted text to a file
    barcode_reader.extract_text_from_pdf()
    print("Extracted Text as Dictionary:")
    print(barcode_reader.extracted_text)
    barcode_reader.detect_barcodes_in_pdf()
    barcode_reader.save_extracted_text_to_file()
    print(f"Extracted text saved to {Properties.EXTRACTED_TEXT_FILE} in {Properties.OUTPUT_FOLDER}")
