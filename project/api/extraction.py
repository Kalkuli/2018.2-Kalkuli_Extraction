import pytesseract
from pdf2image import convert_from_bytes


class Extraction:
    def __init__(self, file):
        self.file = file

    def extract_text_from_image(self, img):
        text_obj = {}
        text_obj['raw_text'] = ""
        for page in img:
            text_obj['raw_text'] += pytesseract.image_to_string(page, lang='por')
        return text_obj


    def convert_pdf_to_image(self):
        return convert_from_bytes(self.file)
    
    def extract(self):
        converted_pdf = self.convert_pdf_to_image()
        extracted_text = self.extract_text_from_image(converted_pdf)
        return extracted_text
    
