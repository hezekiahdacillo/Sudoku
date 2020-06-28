"""
This is a simple program that solves a Sudoku board.
Created by Hezekiah Dacillo

pseudocode:
1. pick an empty location
2. try any valid number
3. repeat
4. backtract
"""

def solve(board):
    """Solves a Sudoku board using backtracking algorithm."""
    empty = find_empty_location(board)
    if not empty:
        return True
    else:
        row, column = empty

    for i in range(1, 10):
        if valid_solution(board, (row, column), i):
            board[row][column] = i

            if solve(board):
                return True

            board[row][column] = 0
    return False

def valid_solution(board, position, number):
    """Return true if the number value of the attempt is valid."""
    # Checks the row of the board
    for i in range(len(board[0])):
        if board[position[0]][i] == number and position[1] != i:
            return False

    # Checks the column of the board
    for j in range(len(board)):
        if board[j][position[1]] == number and position[0] != j:
            return False

    # Check section of the board that the number attempt is in
    column = position[1] // 3
    row = position[0] // 3
    for k in range(row * 3, (row * 3) + 3):
        for l in range(column * 3, (column * 3) + 3):
            if board[k][l] == number and (k, l) != position:
                return False

    return True

def find_empty_location(board):
    """Finds an empty space in the board."""
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                return (i, j)

    return None

# -----------------------------------------------------------------

def solved_board(board):
    """Solves the board and returns the solved Sudoku board"""
    solve(board)
    return board

def print_board(board):
    """Prints the Sudoku board."""
    for i in range(len(board)):
        if (i % 3) == 0 and i != 0:
            print('- - - + - - - + - - -')
        for j in range(len(board[i])):
            if (j % 3) == 0 and j != 0:
                print("| ", end='')
            if j == 8:
                print(board[i][j], end='\n')
            else:
                print(str(board[i][j]) + ' ', end='')