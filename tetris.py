import random
import time
import tkinter
import collections

game_speed = 300
rec_x = rec_y = 35
game_width = 10
game_height = 15
BLACK = "#000000"
BLUE = "#0029ff"
RED = "#ff1700"
GREEN = "#05ff00"
GREY = "#666666"
D_GREY = "#383838"



def run_gui():

    root = tkinter.Tk()
    root.resizable(False, False)

    tetris_canvas = tkinter.Canvas(root, width=rec_x * game_width, height=rec_x * game_height, highlightthickness=0)
    tetris_canvas.grid()

    tetris_gui = TetrisGUI(game_speed, tetris_canvas)
    tetris_gui.tetris_game.new_block()
    tetris_gui.tetris_game.full_line_clear()

    root.bind("<Left>", tetris_gui.left_mediator)
    root.bind("<Right>", tetris_gui.right_mediator)
    root.bind("<Up>", tetris_gui.tetris_game.block_rotator)

    tetris_gui.draw_board()
    tetris_gui.draw_block()
    tetris_gui.block_mediator()

    root.title("Tetris – by The Philgrim, Arrinao, and Master Akuli")
    # root.iconphoto(False, tkinter.PhotoImage(file=image_name.png")) INSERT LATER
    root.mainloop()



class TetrisGUI:
    def __init__(self, speed, canvas):
        self.speed = speed
        self.canvas = canvas
        self.rect_size = 25
        self.tetris_game = TetrisGame()

    def draw_board(self):
        """
        Draws the board of rectangles on top of the canvas
        """
        x_gap = 0
        for x in range(game_width):
            y_gap = 0
            for y in range(game_height):
                self.canvas.create_rectangle(
                    x_gap,
                    y_gap,
                    x_gap + rec_x,
                    y_gap + rec_y,
                    fill=D_GREY,
                    outline=GREY,
                )
                y_gap += 35

            x_gap += 35

    def draw_block(self):
        """
        Draws the different shapes on the board
        """

        current_block_draw = self.tetris_game.current_block

        self.canvas.delete("block")

        for x, y in current_block_draw:
            self.canvas.create_rectangle(
                x * rec_x,
                y * rec_y,
                x * rec_x + rec_x,
                y * rec_x + rec_x,
                tags="block",
                fill=RED,
            )  # TODO: Find way to assign whole block to a variable so it
            # can be deleted

        for x, y in self.tetris_game.landed_blocks:
            self.canvas.create_rectangle(
                x * rec_x,
                y * rec_y,
                x * rec_x + rec_x,
                y * rec_x + rec_x,
                tags="block",
                fill=BLUE,
            )

    def block_mediator(self):
        """
        Has the responsibility to call block_mover() and draw_block() to
        simulate the blocks moving downwards on the canvas
        """
        self.tetris_game.block_mover()

        self.draw_block()

        self.canvas.after(game_speed, self.block_mediator)

    def left_mediator(self, event):
        self.tetris_game.user_input_left()
        self.draw_block()

    def right_mediator(self, event):
        self.tetris_game.user_input_right()
        self.draw_block()



class TetrisGame:
    def __init__(self):
        self.landed_blocks = []
        self.previous_block = None
        self.current_block = None
        self.upcoming_block = None

    def new_block(self):
        x = int(game_width / 2)
        y = 0
        """
        Chooses a random block from "blocks" and assigns it to
        self.current_block
        """
        test_block = [(x, y)]
        blocks = {
            "L": [(x - 1, y), (x, y), (x + 1, y), (x + 1, y + 1)],
            "L_rev": [(x - 1, y + 1), (x - 1, y), (x, y), (x + 1, y)],
            "O": [(x - 1, y), (x, y), (x - 1, y + 1), (x, y + 1)],
            "E": [(x, y), (x - 1, y + 1), (x, y + 1), (x + 1, y + 1)],
            "Z": [(x - 1, y), (x, y), (x, y + 1), (x - 1, y + 1)],
            "Z_rev": [(x + 1, y), (x, y), (x, y + 1), (x - 1, y + 1)],
            "I": [(x - 2, y), (x - 1, y), (x, y), (x + 1, y)],
        }
        if self.upcoming_block is None:
            self.current_block = random.choice(list(blocks.values()))
            # self.current_block = test_block  # Remove when code is working
        else:
            self.current_block = self.upcoming_block
        self.previous_block = self.current_block
        self.upcoming_block = random.choice(list(blocks.values()))
        # self.upcoming_block = test_block  # Remove when code is working

    def user_input_left(self):
        """
        Moves the current block to the left on the canvas
        """
        left = []
        for (x, y) in self.current_block:
            if x == 0:
                return
            left.append((x - 1, y))
        self.current_block = left

    def user_input_right(self):
        """
        Moves the current block to the right on the canvas
        """
        right = []
        for (x, y) in self.current_block:
            if x == 9:
                return
            right.append((x + 1, y))
        self.current_block = right

    def block_mover(self):
        """
        Moves the current block downwards one square on the canvas
        """
        if any(
            (x, y + 1) in self.landed_blocks for (x, y) in self.current_block
        ) or any(y + 1 == game_height for (x, y) in self.current_block):
            for coord in self.current_block:
                self.landed_blocks.append(coord)
            print(self.landed_blocks)
            self.full_line_clear()
            self.new_block()
        else:
            self.current_block = [(x, y + 1) for x, y in self.current_block]

    def block_rotator(self, event):
        rotate = []
        for (x, y) in self.current_block:
            rotate.append((y, x))
        self.current_block = rotate

    def full_line_clear(self):
        y_coordinates = [y for (x, y) in self.landed_blocks]
        coordinates_counter = collections.Counter(y_coordinates)
        print(coordinates_counter)
        for y_line, count in coordinates_counter.items():
            if count == game_width:
                self.landed_blocks = [(a, b) for (a, b) in self.landed_blocks if b != y_line]
                time.sleep(0.5)
                self.landed_blocks = [(a, b+1) for (a, b) in self.landed_blocks if b < y_line] + [(a, b) for (a, b) in self.landed_blocks if b > y_line]
            

run_gui()

