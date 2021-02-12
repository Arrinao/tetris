import sys
import pathlib
import random
import time
import tkinter
from tkinter import ttk

game_speed = 0.5
rec_x = rec_y = 35
width = 10
height = 20
BLACK = ("#000000")
BLUE = ("#0029ff")
RED = ("#ff1700")
GREEN = ("#05ff00")
GREY = ("#666666")
D_GREY = ("#383838")

root = tkinter.Tk()
root.resizable(False, False)

tetris_canvas = tkinter.Canvas(root, width=rec_x * 10, height=rec_x * 20)
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
        x_gap = 2
        for x in range(10):
            y_gap = 2
            for y in range(20):
                tetris_canvas.create_rectangle(
                x_gap, y_gap, x_gap + rec_x, y_gap + rec_y,
                fill=D_GREY, outline=GREY)
                y_gap += 35

            x_gap += 35

    def draw_shape(self, coord_x, coord_y):

        """
        Draws the different shapes on the board
        """



tetris_gui = TetrisGUI(game_speed, root)

x = int(width/2)
y = 0

landed_shapes = [(6, 10)]


def shapes():
    shapes = {
        'L': [(x-1, y), (x,y), (x+1, y), (x+1, y+1)],
        'L_rev': [(x-1, y+1), (x-1, y), (x, y), (x+1, y)],
        'O': [(x-1, y), (x, y), (x-1, y+1), (x, y+1)],
        'E': [(x, y), (x-1, y+1), (x, y+1), (x+1, y+1)],
        'Z': [(x-1, y), (x, y), (x, y+1), (x-1, y+1)],
        'Z_rev': [(x+1, y), (x, y), (x, y+1), (x-1, y+1)],
        'I': [(x-2, y), (x-1, y), (x, y), (x+1, y)]
    }
    shape_choice = random.choice(list(shapes.keys()))

    for block_x, block_y in shapes[shape_choice]:
        print(block_x, block_y)
    shape_mover(shapes[shape_choice])


def shape_mover(shape_coords):
    time.sleep(1.0)
    for shape in shape_coords:
        print (f'Deleted at {shape[0]}, {shape[1]}.')
    if any((x, y+1) in landed_shapes for (x, y) in shape_coords) or any(y+1 == height for (x, y) in shape_coords):
        for coord in shape_coords:
            landed_shapes.append(coord)
        print(landed_shapes)
        #shapes()
    else:
        shape_coords = [(x, y+1) for x, y in shape_coords]
        for shape in shape_coords:
            print(shape[0], shape[1])
        shape_mover(shape_coords)

def user_input_left(event):
    print('Going left!')
#    for (x, y) in shape_coords:
#        return (x-1, y)


def user_input_right(event):
    print('Going right!')
#    for (x, y) in shape_coords:
#        return (x+1, y)


root.bind('<Left>', user_input_left)
root.bind('<Right>', user_input_right)


# shapes()
tetris_gui.draw_board()
root.mainloop()
