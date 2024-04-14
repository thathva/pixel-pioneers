## Overview

Some legal firms deal with combined PDF documents containing multiple sub-documents like Complaint, Summons, Appearance, etc. These combined PDFs need to be separated into individual PDFs for submission to the courts. This tool automates the process using OCR (Optical Character Recognition) to identify sub-document types based on text in specific regions of each page.

## Project Details

### Problem Statement

Legal firms often receive combined PDF documents with multiple sub-documents. These need to be split into individual PDFs, each containing a single sub-document. The first page of each sub-document contains identifying text (e.g., "COMPLAINT"), while subsequent pages do not.

### Solution

Developed a standalone executable tool that uses a configuration file to determine how to split the combined PDFs. The configuration file includes settings for input/output directories and OCR settings.
The configuration file MUST contain all the sections and parameters in the following format.

#### Configuration File (Sample.cfg)

```cfg
[Files]
INPUT=D:\Firm1\Cases\
OUTPUT=D:\Firm1\Out\

[OCR]
Text1="COMPLAINT"
Loc1=200,100,500,400

Text2="SUMMONS"
Loc2=200,100,500,400

Text3="APPEARANCE"
Loc3=200,100,500,400

[LibraryOptions]
Location=Tesseract-OCR\tesseract.exe
```

#### Dependencies
Since there is OCR involved, the program depends on `PyTesseract`. Other dependencies include `configparser`, `PyMuPDF` and `PyPDF`. In development mode, these packages needs to be `pip` installed, and depending on the platform, an `.exe` file of the `Tesseract` library (https://github.com/UB-Mannheim/tesseract/wiki).

#### Development Mode
1. Clone the repository
2. Pip install the additional libraries as mentioned in the Dependencies section.
3. Run the program using `py index.py`

#### Standalone mode
To bundle it in standalone mode, install `pyinstaller` using `pip install pyinstaller`. Once installed, run `pyinstaller -F index.py`. This will generate the `.exe` file into the `dist` folder. Ensure `config.cfg` file is in the same directory and the `Location` key in config file points to the installed location of `Tesseract`. 