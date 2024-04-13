# To Do - Install these packages on the first run or if no downloads are allowed, bundle these packages
import configparser
import os
import PyPDF2
from PyPDF2 import PdfReader, PdfWriter

# Function to split the pdfs
def split_into_pdfs(file, output_directory, value):
    # Read pdf
    inputpdf = PdfReader(open(file, "rb"))
    page_no = 1
    output = PdfWriter()
    for i in range(len(inputpdf.pages)):
        page_no += 1
        output.add_page(inputpdf.pages[i])
        # If page number is lesser than the next given page no (to-do) then keep building the pdf
        if page_no < value:
            continue
        # Create pdf with file name (to-do)
        with open(output_directory + "/" + "document-page%s.pdf" % i, "wb") as outputStream:
            output.write(outputStream)
            output = PdfWriter()

# Read config
config = configparser.ConfigParser()
config.read('config.cfg')
input_directory = config['Files']['input']
output_directory = config['Files']['output']
value = 4

# Iterate through every pdf file
for file in os.listdir(input_directory):
    if file.endswith(".pdf"):
        # OCR function here
        split_into_pdfs(input_directory + "/" + file, output_directory, value)
