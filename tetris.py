import sys
import pathlib
import random
import time
import tkinter
from tkinter import ttk

game_speed = 0.
rec_x = rec_y = 25
width=10
height=20

def make_gui():
    root = tkinter.Tk()
    root.resizable(False, False)

    root = tkinter.Tk()
    root.resizable(False, False)

    tetris_canvas = tkinter.Canvas(root, width=400, height=800, background='black')
    tetris_canvas.grid()

    root.bind('<Left>', user_input_left)
    root.bind('<Right>', user_input_right)
    
    tetris_gui = TetrisGUI(game_speed, root)
    tetris_gui.draw_board()
    tetris_gui.root.mainloop()



# class TetrisGUI:
#     def __init__(self, speed, canvas):
#         self.speed = speed
#         self.canvas = canvas
#
#     def draw_board(self):
#         """
#         Draws the board of rectangles on top of the canvas
#         """
#         print("inside draw_board()")
#         for x in range(10):
#             for y in range(20):
#                 tetris_canvas.create_rectangle(20, 20, 200, 50, fill='red', outline='blue')
#
#     def draw_shape():
#
#         """
#         Draws the different shapes on the board
#         """
#
#
x = int(width/2)
y = 0

landed_shapes = [(6, 10)]

def shapes():
    shape_choice = random.choice(['L', 'O', 'L_rev', 'E', 'Z', 'Z_rev', 'I'])
    if shape_choice == 'L':
        shape_coords = [(x-1, y), (x,y), (x+1, y), (x+1, y+1)]
    elif shape_choice == 'L_rev':
        shape_coords = [(x-1, y+1), (x-1, y), (x, y), (x+1, y)]
    elif shape_choice == 'O':
        shape_coords = [(x-1, y), (x, y), (x-1, y+1), (x, y+1)]
    elif shape_choice == 'I':
        shape_coords = [(x-2, y), (x-1, y), (x, y), (x+1, y)]
    elif shape_choice == 'E':
        shape_coords = [(x, y), (x-1, y+1), (x, y+1), (x+1, y+1)]
    elif shape_choice == 'Z':
        shape_coords = [(x-1, y), (x, y), (x, y+1), (x-1, y+1)]
    elif shape_choice == 'Z_rev':
        shape_coords = [(x+1, y), (x, y), (x, y+1), (x-1, y+1)]
    for block_x, block_y in shape_coords:
             print(block_x, block_y)
    shape_mover(shape_coords)

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
            

    

shapes()
