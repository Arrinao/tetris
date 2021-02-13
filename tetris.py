import random
import time
import tkinter

game_speed = 0.5
rec_x = rec_y = 35
width = 10
height = 20
BLACK = "#000000"
BLUE = "#0029ff"
RED = "#ff1700"
GREEN = "#05ff00"
GREY = "#666666"
D_GREY = "#383838"


def run_gui():

    root = tkinter.Tk()
    root.resizable(False, False)

    tetris_canvas = tkinter.Canvas(root, width=rec_x * 10, height=rec_x * 20)
    tetris_canvas.grid()

    tetris_gui = TetrisGUI(game_speed, tetris_canvas)

    root.bind("<Left>", lambda event: tetris_gui.tetris_game.user_input_left())
    root.bind("<Right>", lambda event: tetris_gui.tetris_game.user_input_right())

    tetris_gui.draw_board()
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
        x_gap = 2
        for x in range(10):
            y_gap = 2
            for y in range(20):
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

    def draw_shape(self, coord_x, coord_y):
        """
        Draws the different shapes on the board
        """

x = int(width / 2)
y = 0


class TetrisGame:
    def __init__(self):
        self.landed_blocks = [(6, 10)]

    def new_block(self):
        blocks = {
            "L": [(x - 1, y), (x, y), (x + 1, y), (x + 1, y + 1)],
            "L_rev": [(x - 1, y + 1), (x - 1, y), (x, y), (x + 1, y)],
            "O": [(x - 1, y), (x, y), (x - 1, y + 1), (x, y + 1)],
            "E": [(x, y), (x - 1, y + 1), (x, y + 1), (x + 1, y + 1)],
            "Z": [(x - 1, y), (x, y), (x, y + 1), (x - 1, y + 1)],
            "Z_rev": [(x + 1, y), (x, y), (x, y + 1), (x - 1, y + 1)],
            "I": [(x - 2, y), (x - 1, y), (x, y), (x + 1, y)],
        }
        self.next_block = random.choice(list(blocks.values()))
        if len(self.landed_blocks) == 0:
            self.current_block = self.next_block
        else:
            self.current_block = self.upcoming_block
        self.upcoming_block = random.choice(list(blocks.values()))

        print(self.current_block)
        self.block_mover(self.current_block)

    def user_input_left(self, event):
        self.left = []
        print("Going left!")
        for (x, y) in self.current_block:
            self.left.append(x + 1, y)
        TetrisGUI.delete_shape(self.current_block)
        TetrisGUI.draw_shape(self.left)
        self.left = self.current_block

    def user_input_right(self, event):
        self.right = []
        print("Going right!")
        for (x, y) in self.current_block:
            self.right.append(x + 1, y)
        TetrisGUI.delete_shape(self.current_block)
        TetrisGUI.draw_shape(self.right)
        self.right = self.current_block

    def block_mover(self, current_block):
        if any((x, y + 1) in self.landed_blocks for (x, y) in current_block) or any(
            y + 1 == height for (x, y) in current_block
        ):
            for coord in current_block:
                self.landed_blocks.append(coord)
            print(self.landed_blocks)
            self.new_block()
        else:
            current_block = [(x, y + 1) for x, y in current_block]
            for block in current_block:
                print(block[0], block[1])


run_gui()
