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
		# Open the PDF file for reading in binary mode
		with open(self.pdf_path, "rb") as pdf_file:
			# Create a PdfFileReader object
			read_pdf = PyPDF2.PdfFileReader(pdf_file)
			# Get the number of pages in the PDF
			number_of_pages = read_pdf.getNumPages()

			# Iterate through each page in the PDF
			for i in range(number_of_pages):
				# Get the page object
				page = read_pdf.pages[i]
				# Extract text content from the page
				page_content = page.extractText()
				print(page_content)
				# Parse text in page_content and convert to dictionary
				self.parse_text(page_content)

	def parse_text(self, text):
		# Split the text into lines
		lines = text.split('\n')
		# Iterate through each line
		for line in lines:
			# Split each line into key and value using ':'
			key_value = line.split(':')
			if len(key_value) == 2:
				# Extract key and value, strip extra spaces, and store in dictionary
				key = key_value[0].strip()
				value = key_value[1].strip()
				self.extracted_text[key] = value

	def detect_barcodes_in_pdf(self):
		# Create a PdfReader object
		reader = PdfReader(self.pdf_path)
		# Get the first page
		page = reader.pages[0]

		# Iterate through each image in the page
		for image_file_object in page.images:
			# Read the image using cv2
			img = cv2.imread(image_file_object)
			# Detect barcodes in the image
			detected_barcodes = decode(img)

			# Traverse through all the detected barcodes in the image
			for barcode in detected_barcodes:
				if barcode.data != "":
					# Print the barcode data
					print(barcode.data)

	def save_extracted_text_to_file(self):
		# Create the full output path by joining OUTPUT_FOLDER and output_file_name
		output_full_path = os.path.join(properties.OUTPUT_FOLDER, self.output_file_name)

		# Open the output file for writing
		with open(output_full_path, "w") as output_file:
			# Write each key-value pair to the file
			for key, value in self.extracted_text.items():
				output_file.write(f"{key}: {value}\n")


if __name__ == "__main__":
	# Create an instance of BarcodeReader with specified input and output files
	barcode_reader = BarcodeReader(properties.TEST_TASK, properties.EXTRACTED_TEXT_FILE)
	# Extract text from the PDF
	barcode_reader.extract_text_from_pdf()
	print("Extracted Text as Dictionary:")
	print(barcode_reader.extracted_text)
	# Detect barcodes in the PDF
	barcode_reader.detect_barcodes_in_pdf()
	# Save the extracted text to a file
	barcode_reader.save_extracted_text_to_file()
	print(f"Extracted text saved to {properties.EXTRACTED_TEXT_FILE} in {properties.OUTPUT_FOLDER}")
