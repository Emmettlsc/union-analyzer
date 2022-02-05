import cv2
import pytesseract
import numpy as np
import os
if os.name == 'nt':
    pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
drawing = False

def crop_to_text(refPt):
    imgCrop = img[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]
    text = pytesseract.image_to_string(imgCrop)
    print(text)
    print('---------------')
    
def click_and_crop(event, x, y, flags, param):

    global refPt, drawing, imgCopy
    imgCopy = img.copy()
    
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        refPt = [(x, y)]
    
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True:
            cv2.rectangle(imgCopy, refPt[0], (x,y),(0,255,0),2)
    
    
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        refPt.append((x, y))
    
        cv2.rectangle(imgCopy, refPt[0], refPt[1], (0, 255, 0), 2)
        crop_to_text(refPt)
        
img = cv2.imread('testFull.jpg', cv2.IMREAD_GRAYSCALE)
imgCopy = img.copy()
cv2.namedWindow('image')
cv2.setMouseCallback('image',click_and_crop)

while(1):
    cv2.imshow('image',imgCopy)
    k = cv2.waitKey(1) & 0xFF
    if k == ord('m'):
        print('m key pressed')
    elif k == 27: #esc
        break

cv2.destroyAllWindows()