import pytesseract
import cv2

pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

def imageReader(image):

    text = pytesseract.image_to_string(image, lang="amh")

    return text




if __name__ == '__main__':
    image = cv2.imread("img/paper8.jpg")
    text = imageReader(image)
    print(text)

