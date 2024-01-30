import os
import sys

import pytest

root_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, root_dir)

from config import Properties
from src.barcode_reader import BarcodeReader


def test_compare_extracted_text_with_file_content():
    # Expected result
    expected_extracted_text = {
        "PN": "tst",
        "SN": "123123",
        "DESCRIPTION": "PART",
        "LOCATION": "111",
        "CONDITION": "FN",
        "RECEIVER#": "9",
        "UOM": "EA",
        "EXP DATE": "13.04.2022",
        "PO": "P101",
        "CERT SOURCE": "wef",
        "REC.DATE": "18.04.2022",
        "MFG": "efwfe",
        "BATCH#": "1",
        "DOM": "13.04.2022",
        "REMARK": "",
        "LOT#": "1",
        "TAGGED BY": "",
        "Qty": "1",
        "NOTES": ""
    }

    # Create an instance of BarcodeReader
    barcode_reader = BarcodeReader(Properties.TEST_TASK, Properties.EXTRACTED_TEXT_FILE)
    barcode_reader.extract_text_from_pdf()

    print("File Path:", os.path.abspath(Properties.EXTRACTED_TEXT_FILE))
    # Extract text from the file
    with open(Properties.EXTRACTED_TEXT_FILE, "r", encoding="utf-8") as file:
        extracted_text_content = file.read()

    # Debugging prints
    print("Extracted text content:")
    print(extracted_text_content)
    print("\nExpected text content:")
    print("\n".join([f"{key}: {value}" for key, value in expected_extracted_text.items()]))

    # Compare the results
    assert barcode_reader.extracted_text == expected_extracted_text
