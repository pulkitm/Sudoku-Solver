from imutils.perspective import four_point_transform
from skimage.segmentation import clear_border
import cv2
import imutils
import numpy as np
from sudoku import Sudoku
from solver import solveSudoku
from get import get_board,get_digit
import sys
from os.path import isfile

#image print utility
def primg(img):
    cv2.imshow("Sudoku",img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

#program starts here...

path = input("\nEnter Path of the Sudoku image: ")

#Checking path validness
if not isfile(path):
	sys.exit("\nNo image found on the given path!")

img = cv2.imread(path,cv2.IMREAD_GRAYSCALE)


print("\n\nDetecting Sudoku board...")

#calling function from get.py file to get the processed Sudoku grid image
grid = get_board(img)


#Loading training data from train_data folder
with np.load('train_data/print_digit3.npz') as data:
    train = data['train']
    train_labels = data['train_labels']
    knn = cv2.ml.KNearest_create()
    knn.train(train,cv2.ml.ROW_SAMPLE,train_labels)

#Interpreting image as 9*9 grid
stepX = grid.shape[1] // 9
stepY = grid.shape[0] // 9
    
board = np.zeros((9, 9), dtype="int")
for y in range(0, 9):    
    for x in range(0, 9):        
        startX = x * stepX
        startY = y * stepY
        endX = (x + 1) * stepX
        endY = (y + 1) * stepY
        cell = grid[startY:endY+4,startX:endX+4]
        
        #Getting processed image of digit
        digi = get_digit(cell)        
        
        if(digi is not None):
            roi = cv2.resize(digi,(28,28))
            pred = 0
            test = roi.reshape(-1,784).astype(np.float32)
            #Predicting
            ret,result,neighbours,dist = knn.findNearest(test,k=7)
            pred = result[0]
            board[y,x] = pred

#Printing Detected board
print("\n\nDetected Sudoku board:")
puzzle = Sudoku(3, 3, board=board.tolist())
puzzle.show()

#Solving sudoku
sol = solveSudoku(board.tolist())
if sol == None :
    sys.exit("No solution exists for the detected board!")

print("\n\nSolved Sudoku board:")
puzzle = Sudoku(3, 3, sol)
puzzle.show_full()

#Printing the solution to image
col_grid = cv2.cvtColor(grid,cv2.COLOR_GRAY2RGB)

for y in range(0, 9):    
    for x in range(0, 9):        
        startX = x * stepX
        startY = y * stepY
        endX = (x + 1) * stepX
        endY = (y + 1) * stepY
        cell = grid[startY:endY+5,startX:endX+5]
        digi = get_digit(cell)        
        
        if(digi is None):
            textX = int((endX - startX) * 0.33)
            textY = int((endY - startY) * -0.2)
            textX += startX
            textY += endY
            cv2.putText(col_grid, str(sol[y][x]), (textX, textY),cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    
primg(col_grid)
