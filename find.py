import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import configparser
from sys import exit
import logging

config = configparser.ConfigParser()
config.read("config.cfg")
logging.basicConfig(
    filename="ocr.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
pytesseract.pytesseract.tesseract_cmd = r"{}".format(
    config.get("LibraryOptions", "location")
)


def adjust_coordinates_for_image(coordinates, image_width, page_width):
    # Unpack the original coordinates
    x1, y1, x2, y2 = coordinates

    # Calculate the scaling factor based on the ratio of the image width to the page width
    scaling = page_width / image_width

    # Adjust the coordinates based on the scaling factor
    adjusted_x1 = x1 * scaling
    adjusted_y1 = y1 * scaling
    adjusted_x2 = x2 * scaling
    adjusted_y2 = y2 * scaling

    return (adjusted_x1, adjusted_y1, adjusted_x2, adjusted_y2)


def is_subdocument(page, ocr_settings, image_width, page_width):
    for setting in ocr_settings:
        ocr_settings[setting] = adjust_coordinates_for_image(
            ocr_settings[setting], image_width, page_width
        )

    # print(ocr_settings)

    for setting in ocr_settings:
        doc_type = setting
        coordinates = ocr_settings[doc_type]
        img_rect = fitz.Rect(coordinates)
        img_pixmap = page.get_pixmap(clip=img_rect)
        try:
            pil_image = Image.frombytes(
                "RGB", [img_pixmap.width, img_pixmap.height], img_pixmap.samples
            )
        except Exception as e:
            logging.error(e)
            print("Error! Check coordinates")
            exit()
        try:
            extracted_text = pytesseract.image_to_string(pil_image)
        except Exception as e:
            logging.error(e)
            print(
                "Please specify location of Tesseract folder (Default: Tesseract-OCR/tesseract.exe)"
            )
            exit()

        extracted_text = extracted_text.strip().lower()

        if doc_type.lower() in extracted_text:
            return True, doc_type

    return False, None


def find_subdocuments(pdf_path, ocr_settings):
    subdocuments = []

    try:
        # Open the PDF file
        doc = fitz.open(pdf_path)

        for page_num, page in enumerate(doc, 1):
            page_width = page.rect.width

            image_list = page.get_images()

            if len(image_list) == 1:
                img = image_list[0]
                xref = img[0]  # get the XREF of the image
                pix = fitz.Pixmap(doc, xref)  # create a Pixmap
                image_width = pix.width

                status, doc_type = is_subdocument(
                    page, dict(ocr_settings), image_width, page_width
                )
                if status:
                    subdocuments.append((doc_type, page_num))

            else:
                print(f"Multiple Images Found in {pdf_path} at {page_num} page")

        # Close the PDF document
        doc.close()
    except Exception as e:
        print(f"Sorry, couldn't find subdocuments for {pdf_path}", e)
        logging.error(e)
        return []

    return subdocuments
