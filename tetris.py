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
    tetris_gui.tetris_game.new_block()

    root.bind("<Left>", lambda event: tetris_gui.tetris_game.user_input_left())
    root.bind("<Right>", lambda event: tetris_gui.tetris_game.user_input_right())

    tetris_gui.draw_board()
    tetris_gui.draw_block(tetris_gui.tetris_game.current_block)
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
        for x in range(10):
            y_gap = 0
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

    def draw_block(self, block_coords):
        """
        Draws the different shapes on the board
        """
        current_block_draw = block_coords
        print(current_block_draw)

        for x, y in current_block_draw:
            self.canvas.create_rectangle(
                x * rec_x, y * rec_y, x * rec_x + rec_x, y * rec_x + rec_x, fill=RED
            )

        # while current_block_draw not in landed_blocks:
        #self.canvas.after(2000, self.tetris_game.block_mover(current_block_draw))




x = int(width / 2)
y = 0


class TetrisGame:
    def __init__(self):
        self.landed_blocks = [(6, 10)]
        self.current_block = None
        self.upcoming_block = None

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
        if self.upcoming_block is None:
            self.current_block = random.choice(list(blocks.values()))
        else:
            self.current_block = self.upcoming_block
        self.upcoming_block = random.choice(list(blocks.values()))

    def user_input_left(self, event):
        left = []
        print("Going left!")
        for (x, y) in self.current_block:
            left.append((x + 1, y))
        return self.current_block, left

    def user_input_right(self, event):
        right = []
        print("Going right!")
        for (x, y) in self.current_block:
            right.append((x + 1, y))
        return self.current_block, right

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
