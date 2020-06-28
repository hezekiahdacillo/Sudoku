from tkinter import *
from tkinter.ttk import *
import copy
from sudoku_solver import solved_board, print_board

# global variables
MARGIN = 20  # pixels around the board
SIDE = 50  # width of every board cell.
WIDTH = HEIGHT = MARGIN * 2 + SIDE * 9  # width and height of the whole board


class SudokuError(Exception):
    """Throws a specific Sudoku error when called."""
    pass


class SudokuBoard(object):
    """Creates Sudoku game board."""

    def __init__(self, board_file):
        self.board = self.create_board(board_file)

    def create_board(self, board_file):
        board = []
        for line in board_file:
            line = line.strip().split()

            # throws an error if the row does not contain 9 numbers
            if len(line) != 9:
                raise SudokuError('Each line in the sudoku puzzle must be 9 chars long.')

            # converts each number string to int
            temp_list = []
            for number in line:

                # throws an error if the row contains invalid characters
                if not number.isdigit():
                    raise SudokuError('Valid characters for a sudoku puzzle must be in 0-9')

                number = int(number)
                temp_list.append(number)

            board += [temp_list]

        # throws an error if the board does not contain 9 rows
        if len(board) != 9:
            raise SudokuError('Each sudoku puzzle must be 9 lines long')

        # for CLI
        print('This is the Sudoku board puzzle.')
        print_board(board)

        return board


class SudokuGame(object):
    """A Sudoku game logic that is responsible for the state of the board."""

    def __init__(self, board_file):
        self.board_file = board_file
        self.start_puzzle = SudokuBoard(board_file).board

    def start(self):
        self.game_over = False
        self.puzzle = copy.deepcopy(
            self.start_puzzle)  # creates a copy of the puzzle for the user to clear their answers

    def check_answer(self):
        solved_puzzle = solved_board(copy.deepcopy(self.start_puzzle))
        if self.puzzle == solved_puzzle:
            self.game_over = True
            return True

        # for CLI
        print('\nThis is your Sudoku board')
        print_board(self.puzzle)
        print('\nThis is the solved Sudoku board.')
        print_board(solved_puzzle)

        return False


class SudokuGameUI(Frame):
    """A Sudoku game user interface that is responsible for drawing the board and processing user inputs."""

    def __init__(self, parent, game):
        self.game = game
        Frame.__init__(self, parent)
        self.parent = parent

        self.row = -1
        self.column = -1

        self.ui()

    def ui(self):
        self.parent.title('Sudoku')
        self.pack(fill=BOTH)
        self.canvas = Canvas(self, width=WIDTH, height=HEIGHT)
        self.canvas.pack(fill=BOTH, side=TOP)
        clear_button = Button(self, text='Clear answers', command=self.clear_answers)
        clear_button.pack(fill=BOTH, side=RIGHT, expand=YES)
        solve_button = Button(self, text='Show answers', command=self.show_answers)
        solve_button.pack(fill=BOTH, side=LEFT, expand=YES)

        self.draw_grid()
        self.draw_puzzle()

        self.canvas.bind('<Button-1>', self.cell_clicked)
        self.canvas.bind('<Key>', self.key_pressed)

    def draw_grid(self):
        for i in range(10):
            colour = 'blue' if i % 3 == 0 else 'gray'

            x0 = MARGIN + i * SIDE
            y0 = MARGIN
            x1 = MARGIN + i * SIDE
            y1 = HEIGHT - MARGIN
            self.canvas.create_line(x0, y0, x1, y1, fill=colour)

            x0 = MARGIN
            y0 = MARGIN + i * SIDE
            x1 = WIDTH - MARGIN
            y1 = MARGIN + i * SIDE
            self.canvas.create_line(x0, y0, x1, y1, fill=colour)

    def draw_puzzle(self):
        self.canvas.delete('numbers')
        for i in range(9):
            for j in range(9):
                answer = self.game.puzzle[i][j]
                if answer != 0:
                    x = MARGIN + j * SIDE + SIDE // 2
                    y = MARGIN + i * SIDE + SIDE // 2
                    original = self.game.start_puzzle[i][j]
                    colour = 'black' if answer == original else 'sea green'
                    self.canvas.create_text(x, y, text=answer, tags='numbers', fill=colour)

    def cell_clicked(self, event):
        if self.game.game_over:
            return
        x = event.x
        y = event.y
        if (MARGIN < x < WIDTH - MARGIN and MARGIN < y < HEIGHT - MARGIN):
            self.canvas.focus_set()

            # get row and column numbers from x,y coordinates
            row = (y - MARGIN) // SIDE
            column = (x - MARGIN) // SIDE

            # if cell was selected already - deselect it
            if (row, column) == (self.row, self.column):
                self.row = -1
                self.column = -1
            elif self.game.start_puzzle[row][column] == 0:
                self.row = row
                self.column = column
        else:
            self.row = -1
            self.column = -1

        self.draw_cursor()

    def draw_cursor(self):
        self.canvas.delete('cursor')
        if self.row >= 0 and self.column >= 0:
            x0 = MARGIN + self.column * SIDE + 1
            y0 = MARGIN + self.row * SIDE + 1
            x1 = MARGIN + (self.column + 1) * SIDE - 1
            y1 = MARGIN + (self.row + 1) * SIDE - 1
            self.canvas.create_rectangle(x0, y0, x1, y1, outline='red', tags='cursor')

    def key_pressed(self, event):
        if self.game.game_over:
            return
        if self.row >= 0 and self.column >= 0 and event.char in '1234567890':
            self.game.puzzle[self.row][self.column] = int(event.char)
            self.column = -1
            self.row = -1
            self.draw_puzzle()
            self.draw_cursor()
            if self.game.check_answer():
                self.draw_victory()

    def draw_victory(self):
        # create a oval (which will be a circle)
        x0 = y0 = MARGIN + SIDE * 2
        x1 = y1 = MARGIN + SIDE * 7
        self.canvas.create_oval(x0, y0, x1, y1, tags='victory', fill='dark orange', outline='orange')

        # create text
        x = y = MARGIN + 4 * SIDE + SIDE // 2
        self.canvas.create_text(x, y, text='You win!', tags='victory', fill='white', font=('Arial', 32))

    def clear_answers(self):
        self.game.start()
        self.canvas.delete('victory')
        self.draw_puzzle()

    def show_answers(self):
        self.game.game_over = True
        self.game.puzzle = solved_board(copy.deepcopy(self.game.start_puzzle))
        self.game.start_puzzle = solved_board(copy.deepcopy(self.game.start_puzzle))
        self.draw_puzzle()


class DifficultyPicker(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent

        self.ui()

    def ui(self):
        self.parent.title('Sudoku')
        self.pack(fill=BOTH)
        self.canvas = Canvas(self, width=WIDTH, height=HEIGHT)
        self.canvas.pack(fill=BOTH, side=TOP)
        self.image = PhotoImage(file='sudoku.png')
        self.background = Label(self, image=self.image).place(relwidth=1, relheight=1)

        self.difficulties = ['Easy', 'Medium', 'Hard', 'Expert']
        self.picker = Combobox(self, values=self.difficulties, width=7)
        self.picker.set(self.difficulties[0])
        self.picker.pack()
        self.picker.place(width=WIDTH, relx=0.5, rely=0.77, anchor=S)
        self.play_button = Button(self, text='Play', command=self.game_on)
        self.play_button.pack()
        self.play_button.place(width=WIDTH, relx=0.5, rely=0.77, anchor=N)

    def game_on(self):
        self.sudoku_difficulty = self.picker.get()
        self.parent.destroy()
        self.set_difficulty()

    def set_difficulty(self):
        if self.sudoku_difficulty == 'Easy':
            board_difficulty = 'easy_board.txt'
        elif self.sudoku_difficulty == 'Medium':
            board_difficulty = 'medium_board.txt'
        elif self.sudoku_difficulty == 'Hard':
            board_difficulty = 'hard_board.txt'
        elif self.sudoku_difficulty == 'Expert':
            board_difficulty = 'expert_board.txt'
        else:
            raise SudokuError('Puzzle difficulty is not set.')

        file = open(board_difficulty)
        boards_file = file.readlines()
        file.close()

        window = Tk()
        window.geometry('%dx%d' % (WIDTH, HEIGHT + 40))

        game = SudokuGame(boards_file)

        game.start()

        SudokuGameUI(window, game)

if __name__ == '__main__':
    window = Tk()
    window.geometry('%dx%d' % (WIDTH, HEIGHT + 40))

    difficulty = DifficultyPicker(window)

    window.mainloop()