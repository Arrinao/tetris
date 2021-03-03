import random
import tkinter
import collections

game_speed = 300
square_size = 35
game_width = 10
game_height = 15
BLACK = "#000000"
BLUE = "#0029ff"
RED = "#ff1700"
GREEN = "#00ff00"
GREY = "#666666"
D_GREY = "#383838"
YELLOW = "#ffd343"
PURPLE = "#9900FF"
ORANGE = '#FF9900'
PINK = '#FF00FF'
TEAL = '#00FFFF'

shape_names = ["I", "L", "L_rev", "O", "E", "Z", "Z_rev"]


def run_gui():

    root = tkinter.Tk()
    root.resizable(False, False)

    tetris_canvas = tkinter.Canvas(
        root,
        width=square_size * game_width,
        height=square_size * game_height,
        highlightthickness=0,
    )
    tetris_canvas.grid()

    tetris_gui = TetrisGUI(game_speed, tetris_canvas)

    root.bind("<Left>", tetris_gui.left_mediator)
    root.bind("<Right>", tetris_gui.right_mediator)
    root.bind("<Up>", tetris_gui.rotate_mediator)

    tetris_gui.draw_board()
    tetris_gui.draw_block()
    tetris_gui.block_mediator()

    root.title("Tetris – by The Philgrim, Arrinao, and Master Akuli")
    # root.iconphoto(False, tkinter.PhotoImage(file=image_name.png")) TODO: INSERT LATER
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
                    x_gap + square_size,
                    y_gap + square_size,
                    fill=D_GREY,
                    outline=GREY,
                )
                y_gap += square_size

            x_gap += square_size

    def draw_block(self):
        """
        Draws the different shapes on the board
        """

        self.canvas.delete("block")
        for x, y in (
            self.tetris_game.get_current_block() + list(self.tetris_game.coord_extractor())
        ):
            self.canvas.create_rectangle(
                x * square_size,
                y * square_size,
                x * square_size + square_size,
                y * square_size + square_size,
                tags="block",
                fill=RED
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

    def rotate_mediator(self, event):
        self.tetris_game.block_rotator()
        self.draw_block()


class TetrisGame:
    def __init__(self):
        self.landed_blocks = {}
        self.upcoming_block_shape = None
        self.new_block()
        self.coords = []

    def new_block(self):
        """
        Chooses a random block from "blocks" and assigns it to
        self.current_block
        """
        if self.upcoming_block_shape is None:
            self.current_block_shape = random.choice(shape_names)
        else:
            self.current_block_shape = self.upcoming_block_shape
        self.current_block_center = (int(game_width / 2), -2)
        self.upcoming_block_shape = random.choice(shape_names)
        self.rotate_counter = 0
        self.current_block_active = True

    def get_current_block(self):
        (x, y) = self.current_block_center
        if self.current_block_shape == "I":
            I = [
                [(x - 2, y), (x - 1, y), (x, y), (x + 1, y)],
                [(x, y - 2), (x, y - 1), (x, y), (x, y + 1)],
            ]
            return I[self.rotate_counter % len(I)]
        if self.current_block_shape == "L":
            L = [
                [(x - 1, y + 1), (x, y + 1), (x + 1, y + 1), (x + 1, y)],
                [(x - 1, y - 1), (x - 1, y), (x - 1, y + 1), (x, y + 1)],
                [(x + 1, y - 1), (x, y - 1), (x - 1, y - 1), (x - 1, y)],
                [(x + 1, y + 1), (x + 1, y), (x + 1, y - 1), (x, y - 1)],
            ]
            return L[self.rotate_counter % len(L)]
        if self.current_block_shape == "L_rev":
            L_rev = [
                [(x - 1, y - 1), (x, y - 1), (x + 1, y - 1), (x + 1, y)],
                [(x + 1, y - 1), (x + 1, y), (x + 1, y + 1), (x, y + 1)],
                [(x + 1, y + 1), (x, y + 1), (x - 1, y + 1), (x - 1, y)],
                [(x - 1, y + 1), (x - 1, y), (x - 1, y - 1), (x, y - 1)],
            ]
            return L_rev[self.rotate_counter % len(L_rev)]
        if self.current_block_shape == "O":
            O = [[(x - 1, y), (x, y), (x, y - 1), (x - 1, y - 1)]]
            return O[0]
        if self.current_block_shape == "E":
            E = [
                [(x - 1, y), (x, y), (x + 1, y), (x, y - 1)],
                [(x, y - 1), (x, y), (x, y + 1), (x + 1, y)],
                [(x + 1, y), (x, y), (x - 1, y), (x, y + 1)],
                [(x, y + 1), (x, y), (x, y - 1), (x - 1, y)],
            ]
            return E[self.rotate_counter % len(E)]
        if self.current_block_shape == "Z":
            Z = [
                [(x - 1, y - 1), (x, y - 1), (x, y), (x + 1, y)],
                [(x + 1, y - 1), (x + 1, y), (x, y), (x, y + 1)],
            ]
            return Z[self.rotate_counter % len(Z)]
        if self.current_block_shape == "Z_rev":
            Z_rev = [
                [(x + 1, y - 1), (x, y - 1), (x, y), (x - 1, y)],
                [(x + 1, y + 1), (x + 1, y), (x, y), (x, y - 1)],
            ]
            return Z_rev[self.rotate_counter % len(Z_rev)]

    def block_mover(self):
        """
        Moves the current block downwards one square on the canvas
        """
        if any(
            (x, y + 1) in self.coords for (x, y) in self.get_current_block()
        ) or any(y + 1 == game_height for (x, y) in self.get_current_block()):
            if self.current_block_shape not in self.landed_blocks:
                self.landed_blocks[self.current_block_shape] = []
            for coord in self.get_current_block():
#               self.landed_blocks[self.current_block_shape]= coord   ##Doesn't work, only one coord is created :(
                self.landed_blocks[self.current_block_shape].append(coord)
            # self.full_line_clear()
            self.new_block()
        else:
            x, y = self.current_block_center
            self.current_block_center = (x, y + 1)

    def coord_extractor(self):
        for block in self.landed_blocks.values():
            for coord in block:
                self.coords.append(coord)
        return self.coords

    def user_input_left(self):
        """
        Moves the current block to the left on the canvas
        """
        if any(x == 0 for (x, y) in self.get_current_block()) or any(
            (x - 1, y) in self.landed_blocks.values() for x, y in self.get_current_block()
        ):
            return
        x, y = self.current_block_center
        self.current_block_center = (x - 1, y)

    def user_input_right(self):
        """
        Moves the current block to the right on the canvas
        """
        if any(x == game_width - 1 for x, y in self.get_current_block()) or any(
            (x + 1, y) in self.landed_blocks.values() for x, y in self.get_current_block()
        ):
            return
        x, y = self.current_block_center
        self.current_block_center = (x + 1, y)

    def block_rotator(self):
        """
        Rotates the current block
        """
        self.rotate_counter += 1
        # if any(x <= -1 or x >= game_width for (x, y) in self.get_current_block()) or any(
        #    (x, y) in self.landed_blocks for x, y in self.get_current_block()
        # ):
        if any(
            x not in range(game_width) or (x, y) in self.landed_blocks.values()
            for (x, y) in self.get_current_block()
        ):
            self.rotate_counter -= 1

    def full_line_clear(self):
        """
        Clears the line once it's fully populated with blocks
        """

    def block_color(self):
        color_list = [RED, BLUE, GREEN, YELLOW, PURPLE, ORANGE, PINK, TEAL]
        color_chart = {shape: color for shape, color in zip(shape_names, color_list)}
        return color_chart[self.current_block_shape]

#    def full_line_clear(self):
#        """
#        Clears the line once it's fully populated with blocks
#        """
#        y_coordinates = [y for (x, y) in self.landed_blocks.values()]
#        coordinates_counter = collections.Counter(y_coordinates)
#        for y_line in range(game_height):
#            count = coordinates_counter[y_line]
#            if count == game_width:
#                # TODO: root.after() here
#                self.landed_blocks = [
#                    (a, b + 1) for (a, b) in self.landed_blocks.values() if b < y_line
#                ] + [(a, b) for (a, b) in self.landed_blocks.values() if b > y_line]

run_gui()
