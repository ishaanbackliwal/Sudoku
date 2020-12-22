#########################################################################
# This is a Sudoku board solver that finds the correct answers          #
# to any sudoku board it is presented with using a BACKTRACKING         #
# algorithm.                                                            #
#                                                                       #
# Algorithm:                                                            #
#       1. Find first empty square in the Sudoku board                  #
#       2. Try and fill found empty square with digits 1 through 9      #
#       3. Check for each digits validity in the board and stop at      #
#          the first valid number based on current the boards layout    #
#          If the board is...                                           #
#               Valid: continue to fill out board using steps 1         #
#                      through 3 recursivley                            #
#               Invalid: undo step three and return to step 2           #
#       4. If entire board as been filled, a solution has been found    #
#########################################################################

# solves entire Sudoku board using backtracking algorithm
# param: board is the Sudoku board to be solved
def solve(board):
    find = find_empty(board)
    # base case
    if not find:
        return True
    else:
        row, col = find
    
    # recursive case
    for i in range(1, 10):
        if valid(board, i, (row, col)):
            board[row][col] = i

            if solve(board):
                return True
                
            board[row][col] = 0

    return False

# checks if number in a specific board and position is valid
# params:
#   board is the board to be checked against
#   num is the number to be validated
#   pos is the position in the board to be checked for the num
# returns: true if num in pos is valid, false otherwise
def valid(board, num, pos):
    # check row
    for i in range(len(board[0])):
        if board[pos[0]][i] == num and pos[1] != i:
            return False
    
    # check col
    for i in range(len(board)):
        if board[i][pos[1]] == num and pos[0] != i:
            return False
    
    # check box
    box_x = pos[1] // 3
    box_y = pos[0] // 3
    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if board[i][j] == num and (i, j) != pos:
                return False

    # if none of the checks result in an invalidity, return true
    return True

# prints board to console
# param: board to be printed
def print_board(board):
    for i in range(len(board)):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - - ")
        for j in range(len(board[0])):
            if j % 3 == 0 and j != 0:
                print(" | ", end="")
            if j == 8:
                print(board[i][j])
            else:
                print(str(board[i][j]) + " ", end="")

# finds next empty location in the board
# returns: (row, col) of empty position, or None if 
#          no empty positions exist
def find_empty(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                return (i, j)
    return None