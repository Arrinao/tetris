# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 03:36:28 2021

@author: Martin
"""
import sys
import pathlib
import random
import time

height=20
width=12

x = int(width/2)
y = 0

       
def shapes():
    shape_choice = random.choice(['L', 'O', 'L_rev', 'E', 'Z', 'Z_rev', 'I'])
    shape_active = True
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
    if shape_active == True:
        time.sleep(0.5)
        for shape in shape_coords:
            print (f'Delete {shape[0]} and {shape[1]}.')
        shape_coords = [(x, y+1) for x, y in shape_coords]
        for shape in shape_coords:
            print(shape[0], shape[1])
        shape_mover(shape_coords)

shapes()

       
root.mainloop()

