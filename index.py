# To Do - Install these packages on the first run or if no downloads are allowed, bundle these packages
import configparser
import os
import PyPDF2
from PyPDF2 import PdfReader, PdfWriter
from find import find_subdocuments


def parse_settings(settings):
    ocr_settings = {}

    for i in range(1, len(settings), 2):
        text_key = settings[i - 1][1].strip('"')
        loc_values = tuple(map(int, settings[i][1].split(",")))
        ocr_settings[text_key] = loc_values

    return ocr_settings


# Function to split the pdfs
def split_into_pdfs(input_directory, file, output_directory, text_and_pages):
    try:
        print('Processing ' + file)
        inputpdf = PdfReader(open(input_directory + "/" + file, "rb"))
        for index, (label, page_number) in enumerate(text_and_pages):
            output = PdfWriter()
            start_page = page_number - 1  # Adjust to 0-based index
            end_page = text_and_pages[index + 1][1] - 1 if index < len(text_and_pages) - 1 else len(inputpdf.pages)
            for i in range(start_page, end_page):
                output.add_page(inputpdf.pages[i])
            with open(f"{output_directory}/{file}_{label}.pdf", "wb") as outputStream:
                output.write(outputStream)
        print('Saved to ' + output_directory)
    except Exception as e:
        print("Something went wrong! Double check the pdf file:", e)
        return

def main():
    # Read config
    config = configparser.ConfigParser()
    config.read("config.cfg")
    try:
        input_directory = config['Files']['input']
        output_directory = config['Files']['output']
    except:
            print("Something went wrong! Ensure the configuration file has a 'Files' section and 'input' and 'output' field under it")
            return

    ocr_settings = parse_settings(config.items("OCR"))

    # Iterate through every pdf file
    for file in os.listdir(input_directory):
        if file.endswith(".pdf"):
            text_and_pages = find_subdocuments(file, ocr_settings)
            split_into_pdfs(input_directory, file, output_directory, text_and_pages)


if __name__ == '__main__':
    main()
