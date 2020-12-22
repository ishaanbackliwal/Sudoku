import sys, pygame as pg
from solver import solve, valid
import time

#########################################################################
# This is a Sudoku gui run by pygame                                    #
# Files Required:                                                       #
#       - gui.py                                                        #
#       - solver.py                                                     #
# Rules: unlimited incorrect guesses                                    #
# Instructions: Click on a square and enter a number to sketch it in.   #
#               To guess that value for that square, select the square  #
#               and press enter. If guess is incorrect, an X will be    #
#               added to the count. If the guess is correct, it will    #
#               become a permanent value on the baord. Enjoy!           #
#########################################################################


# init pygame
pg.init()

# fonts used throughout the program
font = pg.font.SysFont("timesnewroman", 40)
sketch_font = pg.font.SysFont("timesnewroman", 30)
btn_font = pg.font.SysFont("timesnewroman", 30)
game_over_font = pg.font.SysFont("timesnewroman", 60)
instruction_font = pg.font.SysFont("timesnewroman", 20)
win_time_font = pg.font.SysFont("timesnewroman", 30)

# screen settings
pg.display.set_caption("Sudoku")
screen_size = (640, 750)
screen = pg.display.set_mode(screen_size)
pg.display.flip()

# grid of values used to fill sudoku board
grid = [
    [0, 8, 0, 7, 0, 9, 0, 0, 2],
    [0, 3, 4, 0, 1, 0, 0, 9, 0],
    [0, 0, 0, 3, 0, 8, 0, 0, 0],
    [0, 0, 6, 4, 3, 0, 8, 0, 1],
    [0, 0, 1, 2, 7, 6, 0, 4, 0],
    [0, 0, 3, 0, 0, 1, 2, 5, 6],
    [0, 0, 0, 0, 9, 0, 0, 2, 7],
    [3, 4, 0, 8, 6, 7, 9, 0, 0],
    [0, 9, 0, 5, 0, 4, 0, 0, 3]
]

##################################################
# Grid class that defines the entire Sudoku grid #
##################################################
class Grid:

    # intitializes Grid object
    def __init__(self, rows, cols, width, height):
        self.rows = rows
        self.cols = cols
        self.squares = [[Square(grid[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)]
        self.width = width
        self.height = height
        self.model = None
        self.selected = None
    
    # draws lines of Sudoku grid
    # param: screen is the pygame screen
    def draw(self, screen):
        # fill background with white
        screen.fill(pg.Color("white"))
        pg.draw.rect(screen, pg.Color("black"), pg.Rect(5, 5, screen.get_width() - 10, screen.get_height() - 120), 3)
        # draw grid lines
        i = 1
        gap = self.width / 9
        xoffset = 5
        yoffset = 5
        while (i * gap) < self.width:
            # if row/column is multiple of 3, set thickness of line to greater than regular lines
            line_thickness = 3 if i % 3 == 0 else 1
            # horizontal lines
            pg.draw.line(screen, pg.Color("black"), pg.Vector2((i * gap) + xoffset, yoffset), ((i * gap) + xoffset, (self.width + yoffset)), line_thickness)
            # vertical lines
            pg.draw.line(screen, pg.Color("black"), pg.Vector2(xoffset, (i * gap) + yoffset), pg.Vector2((self.width + xoffset), (i * gap) + yoffset), line_thickness)
            i += 1
        
        # fill board with nums
        for i in range(self.rows):
            for j in range (self.cols):
                self.squares[i][j].draw(screen)


    # updates model to send to solver
    def update_model(self):
        self.model = [[self.squares[i][j].val for j in range(self.cols)] for i in range(self.rows)]
    
    # checks if val is valid for position selected
    # param: value to be checked
    # returns: true if valid num, false otherwise
    def valid_num(self, val):
        row, col = self.selected
        if self.squares[row][col].val == 0:
            self.squares[row][col].set_val(val)
            self.update_model()
            # check if val is a valid answer for the position
            if valid(self.model, val, (row, col)) and solve(self.model):
                return True
            else:
                self.squares[row][col].set_val(0)
                self.squares[row][col].set_temp(0)
                self.update_model()
                return False
    
    # pencils in number
    # param: value to be penciled in
    def pencil(self, val):
        row, col = self.selected
        self.squares[row][col].set_temp(val)

    # sets square to selected
    # param: 
    #   row num of square to be selected
    #   col num of square to be selected
    def select_square(self, row, col):
        # set all other squares to unselected
        for i in range(self.rows):
            for j in range(self.cols):
                self.squares[i][j].selected = False
        # set requested square to selected
        self.squares[row][col].selected = True
        self.selected = (row, col)
    
    # returns coordinate of mouse click
    # param: position of mouse click
    # returns: coordinate pair of mouse click if inside screen, otherwise returns None
    def mouse_click(self, position):
        if position[0] < self.width and position[1] < self.height:
            gap = self.width / 9
            x = position[0] / gap
            y = position[1] / gap
            return (int(y), int(x))
        else:
            return None

    # checks board to see if it is completed or not
    # returns: false if board is incomplete, true otherwise
    def finished_check(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.squares[i][j].val == 0:
                    return False
        return True

###################################################################
# Square class that defines each square object in the Sudoku grid #
###################################################################
class Square:
    rows = 9
    cols = 9

    # intitializes Square object
    def __init__(self, val, row, col, width ,height):
        self.val = val
        self.temp = 0
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False
    
    # draws this square onto grid
    # param: screen is the pygame screen
    def draw(self, screen):
        gap = self.width / 9  # width/height of each square
        x = self.col * gap  # x-coordinate of square
        y = self.row * gap  # y-coordinate of square

        # draws temp value
        if self.val == 0 and self.temp != 0:
            text = sketch_font.render(str(self.temp), 1, pg.Color("grey"))
            screen.blit(text, (x+10, y+5))
        # draws final value
        elif self.val != 0:
            num_text = font.render(str(self.val), True, pg.Color("black"))
            screen.blit(num_text, (x + 27, y + 20))
        # draws selection square
        if self.selected:
            pg.draw.rect(screen, pg.Color("lightgreen"), (x + 5, y + 5, gap, gap), 4)

    # sets value
    # param: val
    def set_val(self, val):
        self.val = val
   
    # sets temporary value
    # param: val
    def set_temp(self, val):
        self.temp = val


# formats the number of seconds to hr:min:sec format
# param: seconds is the num of seconds to be converted to format
# returns: time formatted in hr:min:sec form
def time_formatter(seconds):
    second = seconds % 60
    minute = seconds // 60
    hour = minute // 60
    formatted_time = "" + str(hour) + ":" + str(minute) + ":" + str(second)
    return formatted_time

# draws board with all componenets as requested
# params:
#   screen is the pygame screen
#   board is the sudoku board
#   wrong is the count of the number of incorrect user guesses
#   playing_time is the amount of time played
def redraw(screen, board, wrong, playing_time):
    # draw board
    board.draw(screen)
    
    # draw wrong answer Xs
    if wrong < 4:
        xs = font.render("X " * wrong, 1, (115, 0, 0))
    else:
        output_str = "X " * 3 + "+ " + str(wrong - 3)
        xs = font.render(output_str, 1, (115, 0, 0))
    screen.blit(xs, (20, 670))

    # draw time (WITHOUT solve button)
    time_txt = font.render("Time: " + time_formatter(playing_time), 1, pg.Color("black"))
    screen.blit(time_txt, ((screen.get_width() - 250), 670))
    
    # unused code for additional implementation - solving function to complete board for user
    '''
    # draw time WITH solve button
    time_txt = font.render("Time: " + time_formatter(playing_time), 1, pg.Color("black"))
    screen.blit(time_txt, ((screen.get_width() - 250), 650))
    # draw solve button
    pg.draw.rect(screen, pg.Color("DarkSlateBlue"), pg.Rect(screen.get_width() - 200, 700, 100, 40), 2)
    btn_txt = btn_font.render("Solve", 1, pg.Color("DarkSlateBlue"))
    screen.blit(btn_txt, ((screen.get_width() - 185), 705))
    '''

# displays winning message, called when board is completed
# param: win_time is the time it took for user to complete board
# returns: false to stop main function loop
def game_over(win_time):
    running = True
    # run loop until enter key is pressed
    while running:
        # draw rectangle to encapsulate message
        pg.draw.rect(screen, (112, 128, 144), pg.Rect(120, 210, 400, 150))
        # draw text
        game_over_txt = game_over_font.render("GAME OVER", 1, pg.Color("black"))
        time_txt = win_time_font.render("You won in " + time_formatter(win_time), 1, pg.Color("black"))
        instructions_txt = instruction_font.render("(Press 'Enter' to Exit)", 1, pg.Color("black"))
        screen.blit(game_over_txt, (140, 220))
        screen.blit(time_txt, (210, 280))
        screen.blit(instructions_txt, (230, 320))
        pg.display.flip()
        # wait for enter key to be pressed
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    running = False
    return False

# runs entire program
def main():
    # vars
    running = True  # set to false to end game loop
    key = None  # key press
    wrong = 0  # number of wrong guesses
    start_time = time.time()  # time when game was opened
    board = Grid(9, 9, 630, 630)  # create grid

    # game loop
    while running:
        # calc playing time
        playing_time = round(time.time() - start_time)
        # handle external events
        for event in pg.event.get():
            # to quit program
            if event.type == pg.QUIT:
                running = False
            # test for key press events
            if event.type == pg.KEYDOWN:
                # each number key
                if event.key == pg.K_1:
                    key = 1
                if event.key == pg.K_2:
                    key = 2
                if event.key == pg.K_3:
                    key = 3
                if event.key == pg.K_4:
                    key = 4
                if event.key == pg.K_5:
                    key = 5
                if event.key == pg.K_6:
                    key = 6
                if event.key == pg.K_7:
                    key = 7
                if event.key == pg.K_8:
                    key = 8
                if event.key == pg.K_9:
                    key = 9
                # operations when enter key is pressed
                if event.key == pg.K_RETURN:
                    i, j = board.selected
                    if board.squares[i][j].temp != 0:
                        # if guess is incorrect, add to wrong
                        if not board.valid_num(board.squares[i][j].temp):
                            wrong += 1
                        key = None
                        # check if board is complete after every entry
                        if board.finished_check():
                            running = game_over(playing_time)
            # test for mouse clicks
            if event.type == pg.MOUSEBUTTONDOWN:
                position = pg.mouse.get_pos()
                clicked = board.mouse_click(position)
                if clicked != None:
                    board.select_square(clicked[0], clicked[1])
                    key = None
        # pencil in the desired number
        if board.selected and key != None:
            board.pencil(key)
        # redraw board after changes
        redraw(screen, board, wrong, playing_time)
        pg.display.update()

# run the program
main()
pg.quit()