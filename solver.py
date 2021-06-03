# Solves the sudoku given as list of list of integers.
# Returns None if solution does not exists.
# Uses Backtavking technique to solve.

#Infers box index from given indices
def gi(i,j):
    return int(i/3)*3 + int(j/3)

#Cheks if we can fill the val at i,j position
def chk(i,j,val):
    return (row[i][val] and col[j][val] and box[gi(i,j)][val])
    
#Recursive function that solves Sudoku using Backtracking     
def solve (i,j,A) : 
    if i==9:
        return True
        
    if j==9:
        return solve(i+1,0,A) 
        
    if A[i][j]!=0:
        return solve(i,j+1,A)
        
    for k in range(1,10):
    
        if chk(i,j,k):
        
            A[i][j] = k
            row[i][k] = False
            col[j][k] = False
            box[gi(i,j)][k] = False
            
            if solve(i,j+1,A):
                return True
            
            #Backtrack if current choice is not correct
            else :
                A[i][j] = 0
                row[i][k] = True
                col[j][k] = True
                box[gi(i,j)][k] = True
                
    return False

def solveSudoku(A):
    global row
    global col
    global box
    row = [[True for i in range(0,10)] for j in range(0,10)]
    col = [[True for i in range(0,10)] for j in range(0,10)]
    box = [[True for i in range(0,10)] for j in range(0,10)]
    
    for i in range(0,9):
        for j in range (0,9):
        	if A[i][j] != 0:
        		x = int(A[i][j])
        		row[i][x] = False
        		col[j][x] = False
        		box[gi(i,j)][x] = False
        		
    if solve(0,0,A):
    	return A
    else:
    	return None
