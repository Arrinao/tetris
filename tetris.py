import sys
import pathlib
import random
import time
import tkinter
from tkinter import ttk

game_speed = 0.5
rec_x = rec_y = 25
width = 10
height = 20
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)


root = tkinter.Tk()
root.resizable(False, False)

tetris_canvas = tkinter.Canvas(root, width=400, height=800, background="black")
tetris_canvas.grid()


class TetrisGUI:
    def __init__(self, speed, canvas):
        self.speed = speed
        self.canvas = canvas
        self.rect_size = 25

    def draw_board(self):
        """
        Draws the board of rectangles on top of the canvas
        """
        x_gap = 25
        y_gap = 25
        for x in range(10):
            for y in range(20):
                y_gap += 25
                tetris_canvas.create_rectangle(
                    20, 20, 200, 50, fill="red", outline="blue"
                )
            x_gap += 25

    def draw_shape():
        """
        Draws the different shapes on the board
        """


tetris_gui = TetrisGUI(game_speed, root)

x = int(width / 2)
y = 0


class TetrisGame:
    def __init__(self, landed_points):
        self.landed_points = [(6, 10)]

    def blocks(self):
        blocks = {
            "L": [(x - 1, y), (x, y), (x + 1, y), (x + 1, y + 1)],
            "L_rev": [(x - 1, y + 1), (x - 1, y), (x, y), (x + 1, y)],
            "O": [(x - 1, y), (x, y), (x - 1, y + 1), (x, y + 1)],
            "E": [(x, y), (x - 1, y + 1), (x, y + 1), (x + 1, y + 1)],
            "Z": [(x - 1, y), (x, y), (x, y + 1), (x - 1, y + 1)],
            "Z_rev": [(x + 1, y), (x, y), (x, y + 1), (x - 1, y + 1)],
            "I": [(x - 2, y), (x - 1, y), (x, y), (x + 1, y)],
        }
        upcoming_block = random.choice(list(blocks.values()))
        if len(block_coords) > 1:
            block_coords = random.choice(list(blocks.values()))
        else:
            block_coords = upcoming_block

        print(block_coords)
        block_mover(block_coords)

    def block_mover(self, block_coords):
        time.sleep(0.5)
        for block in block_coords:
            print(f"Deleted at {block[0]}, {block[1]}.")
        if any((x, y + 1) in landed_points for (x, y) in block_coords) or any(
            y + 1 == height for (x, y) in block_coords
        ):
            for coord in block_coords:
                landed_points.append(coord)
            block_coords.pop(0)
            print(self.landed_points)
            blocks()
        else:
            block_coords = [(x, y + 1) for x, y in block_coords]
            for block in block_coords:
                print(block[0], block[1])
                block_mover(block_coords)

    def user_input_left(self, event):
        print("Going left!")
        for (x, y) in block_coords:
            return (x - 1, y)

    def user_input_right(self, event):
        print("Going right!")
        for (x, y) in block_coords:
            return (x + 1, y)


root.bind("<Left>", user_input_left)
root.bind("<Right>", user_input_right)


# tetris_gui.draw_board()
root.mainloop()
blocks()
