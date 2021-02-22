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
GREEN = "#05ff00"
GREY = "#666666"
D_GREY = "#383838"
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
    tetris_gui.tetris_game.new_block()

    root.bind("<Left>", tetris_gui.left_mediator)
    root.bind("<Right>", tetris_gui.right_mediator)
    root.bind("<Up>", tetris_gui.tetris_game.block_rotator)

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
            self.tetris_game.get_current_block() + self.tetris_game.landed_blocks
        ):
            self.canvas.create_rectangle(
                x * square_size,
                y * square_size,
                x * square_size + square_size,
                y * square_size + square_size,
                tags="block",
                fill=RED,
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
        self.upcoming_block_shape = None
        self.current_block_shape = None
        self.current_block_center = None

    def new_block(self):
        """
        Chooses a random block from "blocks" and assigns it to
        self.current_block
        """
        x = int(game_width / 2)
        y = 0
        if self.upcoming_block_shape is None:
            self.current_block_shape = random.choice(shape_names)
        else:
            self.current_block_shape = self.upcoming_block_shape
        self.current_block_center = (x, y)
        self.upcoming_block_shape = random.choice(shape_names)

    def get_current_block(self):
        (x, y) = self.current_block_center
        if self.current_block_shape == "I":
            return [(x - 2, y), (x - 1, y), (x, y), (x + 1, y)]
        if self.current_block_shape == "L":
            return [(x - 1, y - 1), (x - 1, y), (x, y), (x + 1, y)]
        if self.current_block_shape == "L_rev":
            return [(x - 1, y), (x, y), (x + 1, y), (x + 1, y + 1)]
        if self.current_block_shape == "O":
            return [(x - 1, y), (x, y), (x + 1, y), (x + 1, y + 1)]
        if self.current_block_shape == "E":
            return [(x - 1, y), (x, y), (x + 1, y), (x + 1, y + 1)]
        if self.current_block_shape == "Z":
            return [(x - 1, y), (x, y), (x + 1, y), (x + 1, y + 1)]
        if self.current_block_shape == "Z_rev":
            return [(x - 1, y), (x, y), (x + 1, y), (x + 1, y + 1)]

    def user_input_left(self):
        """
        Moves the current block to the left on the canvas
        """
        if any(x == 0 for x, y in self.get_current_block()):
            return
        x, y = self.current_block_center
        self.current_block_center = (x - 1, y)

    def user_input_right(self):
        """
        Moves the current block to the right on the canvas
        """
        if any(x == game_width - 1 for x, y in self.get_current_block()):
            return
        x, y = self.current_block_center
        self.current_block_center = (x + 1, y)

    def block_mover(self):
        """
        Moves the current block downwards one square on the canvas
        """
        if any(
            (x, y + 1) in self.landed_blocks for (x, y) in self.get_current_block()
        ) or any(y + 1 == game_height for (x, y) in self.get_current_block()):
            for coord in self.get_current_block():
                self.landed_blocks.append(coord)
            print(self.landed_blocks)
            self.full_line_clear()
            self.new_block()
        else:
            x, y = self.current_block_center
            self.current_block_center = (x, y + 1)

    def block_rotator(self, event):
        print("TODO: should rotate")

    def full_line_clear(self):
        y_coordinates = [y for (x, y) in self.landed_blocks]
        coordinates_counter = collections.Counter(y_coordinates)
        print(coordinates_counter)
        for y_line in range(game_height):
            count = coordinates_counter[y_line]
            if count == game_width:
                # TODO: root.after() here
                self.landed_blocks = [
                    (a, b + 1) for (a, b) in self.landed_blocks if b < y_line
                ] + [(a, b) for (a, b) in self.landed_blocks if b > y_line]


run_gui()
