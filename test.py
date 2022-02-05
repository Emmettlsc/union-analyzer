import cv2
import pytesseract

img = cv2.imread('test5.png')

text = pytesseract.image_to_string(img)
print(text)
