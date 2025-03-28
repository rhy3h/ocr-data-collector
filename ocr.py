import easyocr

class Ocr:
    def __init__(self):
        self.easyocr_reader = easyocr.Reader(['en'])

    def predictByEasyOcr(self, file_path: str):
        return self.easyocr_reader.readtext(file_path, detail = 0)
