import cv2
import numpy as np
from PIL import Image
import sys
import pytesseract


pytesseract.pytesseract.tesseract_cmd = 'D:\\study_ghw\\Tesseract-OCR\\tesseract'

def change_contrast(img, level):
    factor = (259 * (level + 255)) / (255 * (259 - level))
    def contrast(c):
        return 128 + factor * (c - 128)
    return img.point(contrast)


bookName=sys.argv[1]
large = cv2.imread(bookName)
im = Image.open(bookName)
print("image height is "+str(im.size[1])+"width  is "+str(im.size[0]))
'''if(im.size[1]<900 and im.size[0]<900):
	im=im.resize([900,900])'''
change_contrast(im, 100)
#change_contrast(large,100)

rgb = cv2.pyrDown(large)
small = cv2.cvtColor(rgb, cv2.COLOR_BGR2GRAY)

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
grad = cv2.morphologyEx(small, cv2.MORPH_GRADIENT, kernel)

_, bw = cv2.threshold(grad, 0.0, 255.0, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 1))
connected = cv2.morphologyEx(bw, cv2.MORPH_CLOSE, kernel)
# using RETR_EXTERNAL instead of RETR_CCOMP
_,contours, hierarchy = cv2.findContours(connected.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

mask = np.zeros(bw.shape, dtype=np.uint8)
ymax=im.size[1]

for idx in range(len(contours)):
    x, y, w, h = cv2.boundingRect(contours[idx])
    mask[y:y+h, x:x+w] = 0
    cv2.drawContours(mask, contours, idx, (255, 255, 255), -1)
    r = float(cv2.countNonZero(mask[y:y+h, x:x+w])) / (w * h)

    if r > 0.45 :
        cv2.rectangle(rgb, (x, y), (x+w-1, y+h-1), (0, 255, 0), 2)
        cropped=small[y:y+h,x:x+w]
        cv2.imwrite("imgTempSave.jpg",cropped)
        img_cropped = Image.open("imgTempSave.jpg")
        text = pytesseract.image_to_string(img_cropped, lang = 'eng')
        print("the text is "+text)
'''


        print("x is "+str(x)+" y is "+str(y)+" x+w-1 is "+str(x+w-1)+" y+h-1 is "+str(y+h-1))
        tempVar=im
        imgTempSave=im.crop((x,y,x+w-1,y+h-1))
        imgTempSave.save("imgTempSave"+str(idx)+".jpg")
        
        im=tempVar


'''
cv2.imshow('rects', rgb)
cv2.waitKey(0)