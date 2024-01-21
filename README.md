# Barcode Reader Project

This project provides a simple barcode reader implemented in Python. It extracts information from a PDF file, detects barcodes in the images, and outputs the results.

## Project Structure

The project is organized as follows:

- **src**: Contains the source code of the barcode reader.
- **tests**: Contains unit tests for the barcode reader.
- **config**: Contains configuration files.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/Nussi1/bacode_parsing_ws_test.git
    cd barcode_reader_testing_project
    ```

2. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

To use the barcode reader, follow these steps:

1. Set the PDF file path in the `config.py` file:

    ```python
    TEST_TASK = "path/to/your/pdf/file.pdf"
    ```

2. Run the barcode reader:

    ```bash
    python barcode_reader.py
    ```

The results will be displayed in the console.

## Testing

To run the unit tests, use the following command:

```bash
pytest
