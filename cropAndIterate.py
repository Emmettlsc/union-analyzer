import cv2
import pytesseract
import numpy as np
import os
if os.name == 'nt':
    pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
drawing = False
colSelected = False

def crop_to_text(refPt):
    imgCrop = img[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]
    #add white border for OCR
    bordersize = 10
    imgCrop = cv2.copyMakeBorder(
        imgCrop,
        top=bordersize,
        bottom=bordersize,
        left=bordersize,
        right=bordersize,
        borderType=cv2.BORDER_CONSTANT,
        value=[255,255,255]
    )
    text = pytesseract.image_to_string(imgCrop)
    print(text)
    print('---------------')
    
def iterate_crop_to_text(lineRefPt):
    imgCopy = img.copy()
    cv2.rectangle(imgCopy, lineRefPt[0], lineRefPt[1], (100, 100, 255), 2)
    crop_to_text(lineRefPt)
    cv2.imshow('image', imgCopy)
    k = cv2.waitKey(0) & 0xFF
    if k == 27: #esc:
        cv2.destroyAllWindows()
        return
    elif k == ord('s'):
        lineRefPt[0] = (lineRefPt[0][0], lineRefPt[0][1]+1)
        lineRefPt[1] = (lineRefPt[1][0], lineRefPt[1][1]+1)
    elif k == ord('w'):
        lineRefPt[0] = (lineRefPt[0][0], lineRefPt[0][1]-1)
        lineRefPt[1] = (lineRefPt[1][0], lineRefPt[1][1]-1)
    elif k == 13: #enter
        height = lineRefPt[1][1] - lineRefPt[0][1]
        lineRefPt[0] = (lineRefPt[0][0], lineRefPt[0][1]+height)
        lineRefPt[1] = (lineRefPt[1][0], lineRefPt[1][1]+height)
    if(lineRefPt[1][1] < img.shape[0]):
        iterate_crop_to_text(lineRefPt)
    
def click_and_crop(event, x, y, flags, param):

    global refPt, drawing, img, imgCopy, colSelected
    if event == cv2.EVENT_LBUTTONDOWN:
        imgCopy = img.copy()
        drawing = True
        refPt = [(x, y)]
    
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True:
            imgCopy = img.copy()
            color = (100, 255, 100) if colSelected != True else (100, 100, 255)
            cv2.rectangle(imgCopy, refPt[0], (x,y),color,2)
    
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        refPt.append((x, y))
        if colSelected == True:
            iterate_crop_to_text(refPt)
        else:
            colSelected = True
            img = img[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]
            imgCopy = img.copy()
        
        
img = cv2.imread('testFull.jpg')
imgFull = img.copy();
imgCopy = img.copy()
cv2.namedWindow('image')
cv2.setMouseCallback('image',click_and_crop)

while(1):
    cv2.imshow('image',imgCopy)
    k = cv2.waitKey(1) & 0xFF
    if k == ord('s'):
        print('move box down, WIP')
    elif k == ord('r'):
        img = imgFull  
    elif k == 27: #esc
        break

cv2.destroyAllWindows()