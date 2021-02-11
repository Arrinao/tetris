# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 03:36:28 2021

@author: Martin
"""
import sys
import pathlib
import random
import time
import tkinter
from tkinter import ttk

game_speed = 0.5

class Board:
    height = 20
    width = 12
    black = (0, 0, 0)
    rectangle = 25, 25

    def __init__(self, speed):
        self.speed = speed

    root = tkinter.Tk()
    root.resizable(False, False)


tetris_board = Board(game_speed)

x = int(tetris_board.width/2)
y = 0

landed_shapes = [(6, 10)]

def shapes():
    shape_choice = random.choice(['L', 'O', 'L_rev', 'E', 'Z', 'Z_rev', 'I'])
    if shape_choice == 'L':
        shape_coords = [(x-1, y), (x,y), (x+1, y), (x+1, y+1)]
        for block_x, block_y in shape_coords:
             print(block_x, block_y)
        shape_mover(shape_coords)
    elif shape_choice == 'L_rev':
        shape_coords = [(x-1, y+1), (x-1, y), (x, y), (x+1, y)]
        for block_x, block_y in shape_coords:
             print(block_x, block_y)
        shape_mover(shape_coords)
    elif shape_choice == 'O':
        shape_coords = [(x-1, y), (x, y), (x-1, y+1), (x, y+1)]
        for block_x, block_y in shape_coords:
             print(block_x, block_y)
        shape_mover(shape_coords)
    elif shape_choice == 'I':
        shape_coords = [(x-2, y), (x-1, y), (x, y), (x+1, y)]
        for block_x, block_y in shape_coords:
             print(block_x, block_y)
        shape_mover(shape_coords)
    elif shape_choice == 'E':
        shape_coords = [(x, y), (x-1, y+1), (x, y+1), (x+1, y+1)]
        for block_x, block_y in shape_coords:
             print(block_x, block_y)
        shape_mover(shape_coords)
    elif shape_choice == 'Z':
        shape_coords = [(x-1, y), (x, y), (x, y+1), (x-1, y+1)]
        for block_x, block_y in shape_coords:
             print(block_x, block_y)
        shape_mover(shape_coords)
    elif shape_choice == 'Z_rev':
        shape_coords = [(x+1, y), (x, y), (x, y+1), (x-1, y+1)]
        for block_x, block_y in shape_coords:
             print(block_x, block_y)
        shape_mover(shape_coords)

def shape_mover(shape_coords):
    time.sleep(game_speed)
    for shape in shape_coords:
        print (f'Deleted at {shape[0]}, {shape[1]}.')
    if any((x, y-1) in shape_coords for (x, y) in landed_shapes):
        for coord in shape_coords:
            landed_shapes.append(coord)
        return shapes()
    else:
        shape_coords = [(x, y+1) for x, y in shape_coords]
        for shape in shape_coords:
            print(f'Spawned at {shape[0]}, {shape[1]}.')
        shape_mover(shape_coords)

#tetris_board.root.mainloop()
shapes()
