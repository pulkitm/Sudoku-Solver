from imutils.perspective import four_point_transform
from skimage.segmentation import clear_border
import cv2
import imutils
import numpy as np

#Extracts out digits and returns its bounding rectangle 
def get_digit(cell):
    #Thresholding
    thresh = cv2.threshold(cell,0,255,cv2.THRESH_BINARY_INV|cv2.THRESH_OTSU)[1]
    thresh = clear_border(thresh)
    
    #finding digit contour
    cntrs = cv2.findContours(thresh.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cntrs = imutils.grab_contours(cntrs)
    if len(cntrs) ==0:
        return None
    
    #check for noise
    c = max(cntrs,key = cv2.contourArea)
    mask = np.zeros(thresh.shape,dtype = 'uint8')
    cv2.drawContours(mask,[c],-1,255,-1)      
    (h,w) = thresh.shape
    perfill = cv2.countNonZero(mask)/float(w*h)
    if perfill< 0.03:
        return None
        
    #bounding the digit
    x,y,w,h = cv2.boundingRect(c)
    imgCrop = thresh[y:(y+h),x:(x+w)]
    
    return imgCrop

#Crops and warps Image around sudoku grid
def get_board(img):
	#Blurring and Thresholding
	p1 = cv2.GaussianBlur(img.copy(),(9,9),0)
	p2 = cv2.adaptiveThreshold(p1,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)

	#Inverting and dilating for better boundary detection
	p3 = cv2.bitwise_not(p2,p2)
	kernel = np.array([[0., 1.,0.],[1., 1.,1.],[0.,1.,0.]],np.uint8)
	p4 = cv2.dilate(p3,kernel)
	
	#Finding largest contours and supposing it to be grid
	contours, h = cv2.findContours(p4.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	contours = sorted(contours, key=cv2.contourArea, reverse=True)
	
	#Approximating it to be 4 sided polygon
	pm = cv2.arcLength(contours[0],True)
	grid_cnt = cv2.approxPolyDP(contours[0],0.05*pm,True)
	
	if len(grid_cnt) != 4 :
		sys.exit("\nCan not detect the board! Please try with a better image.")
	    
	#Deskewing the image and warping the perspective
	grid = four_point_transform(img,grid_cnt.reshape(4, 2))
	
	return grid

	

