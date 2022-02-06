import cv2
import pytesseract
import numpy as np
import os
import xlwings as xw
import pandas as pd

from spellchecker import SpellChecker #spell chack 


if os.name == 'nt':
    pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
drawing = False

wb = xw.Book('fill.xlsx')
sheet = wb.sheets['Sheet1']


def spellcheck (str):
    spell = SpellChecker()
    lines = str.split('\n')
    for j in range(len(lines)): 
        arr = lines[j].split()
        for i in range(len(arr)):
            arr[i]=arr[i].lower()
        misspelled = spell.unknown(arr)
        for word in misspelled: 
            if word != 'co.':
                fix = spell.correction(word)
                arr[arr.index(word)] = fix
        lines[j] = ' '.join(arr)
    df = pd.DataFrame(lines, columns=['Company Name'])
    sheet.range('A1').value = df
    print('\n'.join(lines))






def crop_to_text(refPt):
    imgCrop = img[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]
    text = pytesseract.image_to_string(imgCrop)
    spellcheck(text)
    print('---------------')
    
def click_and_crop(event, x, y, flags, param):

    global refPt, drawing, imgCopy
    
    if event == cv2.EVENT_LBUTTONDOWN:
        imgCopy = img.copy()
        drawing = True
        refPt = [(x, y)]
    
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True:
            imgCopy = img.copy()
            cv2.rectangle(imgCopy, refPt[0], (x,y),(0,255,0),2)
    
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        refPt.append((x, y))
        cv2.rectangle(imgCopy, refPt[0], refPt[1], (0, 255, 0), 2)
        crop_to_text(refPt)
        
        
img = cv2.imread('testFull.jpg', cv2.IMREAD_GRAYSCALE)
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