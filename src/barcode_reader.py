import os

import cv2
import PyPDF2
from PyPDF2 import PdfReader
from pyzbar.pyzbar import decode

from config import properties


class BarcodeReader:
    def __init__(self, pdf_path, output_file_name):
        self.pdf_path = pdf_path
        self.output_file_name = output_file_name
        self.extracted_text = {}

    def extract_text_from_pdf(self):
        with open(self.pdf_path, "rb") as pdf_file:
            read_pdf = PyPDF2.PdfFileReader(pdf_file)
            number_of_pages = read_pdf.getNumPages()

            for i in range(number_of_pages):
                page = read_pdf.pages[i]
                page_content = page.extractText()
                print(page_content)
                # Parse text in page_content and convert to dictionary
                self.parse_text(page_content)

    def parse_text(self, text):

        lines = text.split('\n')
        for line in lines:
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
    if __name__ == "__main__":
        barcode_reader = BarcodeReader(properties.TEST_TASK, properties.EXTRACTED_TEXT_FILE)
        barcode_reader.extract_text_from_pdf()
        print("Extracted Text as Dictionary:")
        print(barcode_reader.extracted_text)
        barcode_reader.detect_barcodes_in_pdf()

        barcode_reader.save_extracted_text_to_file()
        print(f"Extracted text saved to {properties.EXTRACTED_TEXT_FILE} in {properties.OUTPUT_FOLDER}")
