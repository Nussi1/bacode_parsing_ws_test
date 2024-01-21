import os

import pytest

from config import properties
from src.barcode_reader import BarcodeReader


def test_compare_extracted_text_with_file_content():
    # Expected result
    expected_extracted_text = {
        "PN": "tst",
        "DESCRIPTION": "PART LOCATION: 111 RECEIVER#: 9",
        "EXP DATE": "13.04.2022",
        "CERT SOURCE": "wef",
        "REC.DATE": "18.04.2022",
        "BATCH#": "1",
        "REMARK": "",
        "TAGGED BY": "",
        "Qty": "1",
        "SN": "123123",
        "CONDITION": "FN UOM: EA",
        "PO": "P101",
        "MFG": "efwfe",
        "DOM": "13.04.2022",
        "LOT#": "1",
        "NOTES": "inspection notes"
    }

    # Create an instance of BarcodeReader
    barcode_reader = BarcodeReader(properties.TEST_TASK)

    # Check the existence of the file
    assert os.path.exists(properties.EXTRACTED_TEXT_FILE)

    # Extract text from the file
    with open(properties.EXTRACTED_TEXT_FILE, "r", encoding="utf-8") as file:
        extracted_text_content = file.read()

    # Compare the results
    assert barcode_reader.extracted_text == expected_extracted_text
    assert extracted_text_content.strip() == str(expected_extracted_text).strip()
