import cv2
import pytesseract
import numpy as np
import os
if os.name == 'nt':
    pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

img = cv2.imread('test14.png')
text = pytesseract.image_to_string(img)
print(text)
height, width, channels = img.shape
n = 28

for i in range(n):
    imgCrop = img[int(i*height/n):int((i+1)*height/n),]
    textCrop = pytesseract.image_to_string(imgCrop)
    x = -10
    while(len(textCrop) < 12 and x < 10 and int(i*height/n+x) > 0 and int((i+1)*height/n+x) < height):
        imgCrop = img[int(i*height/n+x):int((i+1)*height/n+x)]
        textCrop = pytesseract.image_to_string(imgCrop)
        x+=1
    print('x: '+str(x))
    print(textCrop)
    cv2.imshow(textCrop, imgCrop)
    cv2.waitKey(0)

'''
h, w, c = img.shape
boxes = pytesseract.image_to_boxes(img) 
for b in boxes.splitlines():
    b = b.split(' ')
    img = cv2.rectangle(img, (int(b[1]), h - int(b[2])), (int(b[3]), h - int(b[4])), (0, 255, 0), 2)
cv2.imshow('img', img)
cv2.waitKey(0)
'''
