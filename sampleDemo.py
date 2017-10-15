from PIL import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = 'D:\\study_ghw\\Tesseract-OCR\\tesseract'

im = Image.open("bwsample.jpg")

text = pytesseract.image_to_string(im, lang = 'eng')

print(text)