import cv2
import imutils
import numpy as np

def primg(img):
    cv2.imshow("Sudoku",img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
def get_digit(cell):
    #primg(cell)
    thresh = cv2.threshold(cell,0,255,cv2.THRESH_BINARY_INV|cv2.THRESH_OTSU)[1]
    #thresh = clear_border(thresh)
    #primg(thresh)
    cntrs = cv2.findContours(thresh.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cntrs = imutils.grab_contours(cntrs)
    
    c = max(cntrs,key = cv2.contourArea)
    x,y,w,h = cv2.boundingRect(c)
    imgCrop = thresh[y:(y+h),x:(x+w)]
    #primg(imgCrop)
    return imgCrop
    
grid = cv2.imread("dataset.png",cv2.IMREAD_GRAYSCALE )
stepX = grid.shape[1] // 9
stepY = grid.shape[0] // 6

for y in range(0, 6):    
    row = []
    for x in range(0, 9):        
        startX = x * stepX
        startY = y * stepY
        endX = (x + 1) * stepX
        endY = (y + 1) * stepY
        cell = grid[startY:endY+5,startX:endX+5]
        digi = get_digit(cell)
        cv2.imwrite(str(y)+str(x)+".png",digi)
