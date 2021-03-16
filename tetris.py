import random
import tkinter
import collections
import time

game_speed = 300
square_size = 32
game_width = 10
game_height = 15
sidebar_width = 100
BLACK = "#000000"
BLUE = "Blue2"
RED = "red2"
GREEN = "green2"
GREY = "Gray24"
D_GREY = "gray7"
YELLOW = "gold"
PURPLE = "#9900FF"
ORANGE = "Orangered2"
PINK = "#FF00FF"
TEAL = "paleturquoise3"

shape_names = ["I", "L", "L_rev", "O", "E", "Z", "Z_rev"]


def run_gui():

    root = tkinter.Tk()
    root.resizable(False, False)

    game_board = tkinter.Canvas(
        root,
        width=square_size * game_width,
        height=square_size * game_height,
    )
    game_board.grid(row=1, sticky='nswe')

    topbar = tkinter.Frame(root, bg=D_GREY, relief = 'ridge')
    topbar.grid(row=0, columnspan=2, sticky='we')

    topbar_time = tkinter.Label(topbar, bg=D_GREY, text='00:00', font = 'digital-7', fg='orange', borderwidth=1)
    topbar_time.pack(side='left', padx=10)

    topbar_score = tkinter.Label(topbar, bg=D_GREY, text='foo', font = 'digital-7', fg='orange', borderwidth=1)
    topbar_score.pack(side='left', fill='x', expand=True)

    topbar_board = tkinter.Canvas(topbar, bg=D_GREY, width = square_size*4, height = square_size*2, highlightthickness=0)
    topbar_board.pack(side='right', expand=True)

    sidebar = tkinter.Frame(root, bg=D_GREY)
    sidebar.grid(row=1, column=1, sticky='nsw')

    new_game_button = tkinter.Button(sidebar, text = 'start')
    new_game_button.grid(sticky='n')

    new_game_button2 = tkinter.Button(sidebar, text = 'start')
    new_game_button2.grid(sticky='n')

    new_game_button3 = tkinter.Button(sidebar, text = 'start')
    new_game_button3.grid(sticky='n')

    tetris_gui = TetrisGUI(game_speed, game_board)

    main_board = Board(game_board, GREY, game_width, game_height, random.choice(shape_names), (int(game_width / 2), -2), 0)
    small_board = Board(topbar_board, D_GREY, square_size*4, square_size*2, random.choice(shape_names), (2, 1), 0)

    root.bind("<Left>", tetris_gui.move_block_left)
    root.bind("<Right>", tetris_gui.move_block_right)
    root.bind("<Up>", tetris_gui.rotate_block)

    main_board.draw_board()
    small_board.draw_board()
    main_board.draw_block()
    main_board.move_block()

    root.title("Tetris – by The Philgrim, Arrinao, and Master Akuli")
    # root.iconphoto(False, tkinter.PhotoImage(file=image_name.png")) TODO: INSERT LATER
    root.mainloop()


class TetrisGUI:
    def __init__(self, speed, canvas):
        self.speed = speed
        self.canvas = canvas
        self.rect_size = 25
        self.tetris_game = TetrisGame()
        self.start_time = time.time()

    #def draw_board(self, canvas, width, height, outline_color):
    #    """
    #    Draws the board of rectangles on top of the canvas
    #    """
    #    x_gap = 0
    #    for x in range(width):
    #        y_gap = 0
    #        for y in range(height):
    #            canvas.create_rectangle(
    #                x_gap,
    #                y_gap,
    #                x_gap + square_size,
    #                y_gap + square_size,
    #                fill=D_GREY,
    #                outline=outline_color,
    #            )
    #            y_gap += square_size
    #
    #        x_gap += square_size

    #def draw_block(self):
    #    """
    #    Draws the different shapes on the board
    #    """
    #    self.color_dict = {
    #        "L": YELLOW,
    #        "I": RED,
    #        "E": GREEN,
    #        "L_rev": BLUE,
    #        "Z": PURPLE,
    #        "Z_rev": TEAL,
    #        "O": ORANGE,
    #    }
    #    self.canvas.delete("block")
    #    self.canvas_small.delete('block')
    #    for x, y in self.tetris_game.get_block_shape(self.tetris_game.current_block_shape, self.tetris_game.current_block_center, self.tetris_game.rotate_counter):
    #        self.canvas.create_rectangle(
    #            x * square_size,
    #            y * square_size,
    #            x * square_size + square_size,
    #            y * square_size + square_size,
    #            tags="block",
    #            fill=self.color_dict[self.tetris_game.current_block_shape],
    #        )
    #
    #    for letter, coord_list in self.tetris_game.landed_blocks.items():
    #        for (x, y) in coord_list:
    #            self.canvas.create_rectangle(
    #                x * square_size,
    #                y * square_size,
    #                x * square_size + square_size,
    #                y * square_size + square_size,
    #                tags="block",
    #                fill=self.color_dict[letter],
    #            )
    #
    #    for x, y in self.tetris_game.get_block_shape(self.tetris_game.upcoming_block_shape, self.tetris_game.upcoming_block_center, 0):
    #        self.canvas_small.create_rectangle(
    #                x * square_size,
    #                y * square_size,
    #                x * square_size + square_size,
    #                y * square_size + square_size,
    #                tags="block",
    #                fill=self.color_dict[self.tetris_game.upcoming_block_shape],
    #        )

    def move_block(self):
        """
        Has the responsibility to call current_block_mover() and draw_block() to
        simulate the blocks moving downwards on the canvas
        """
        self.tetris_game.current_block_mover()
        self.draw_block()
        self.canvas.after(game_speed, self.move_block)

    def move_block_left(self, event):
        self.tetris_game.user_input_left()
        self.draw_block()

    def move_block_right(self, event):
        self.tetris_game.user_input_right()
        self.draw_block()

    def rotate_block(self, event):
        self.tetris_game.block_rotator()
        self.draw_block()

    def timer(self):
        game_time = time.time() - self.start_time
        return f"{int(game_time / 60):02d}:{int(game_time % 60):02d}"


class TetrisGame:
    def __init__(self):
        self.landed_blocks = {}  # e.g. {'L': [(1, 2), (3, 4)]}
        self.upcoming_block_shape = None
        self.new_block()

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
        self.upcoming_block_center = (2, 1)
        self.rotate_counter = 0

    #def get_block_shape(self, block_shape, block_center, rotate_counter):
    #    (x, y) = block_center
    #    if block_shape == "I":
    #        coords = [
    #            [(x - 2, y), (x - 1, y), (x, y), (x + 1, y)],
    #            [(x, y - 2), (x, y - 1), (x, y), (x, y + 1)],
    #        ]
    #    if block_shape == "L":
    #        coords = [
    #            [(x - 1, y + 1), (x, y + 1), (x + 1, y + 1), (x + 1, y)],
    #            [(x - 1, y - 1), (x - 1, y), (x - 1, y + 1), (x, y + 1)],
    #            [(x + 1, y - 1), (x, y - 1), (x - 1, y - 1), (x - 1, y)],
    #            [(x + 1, y + 1), (x + 1, y), (x + 1, y - 1), (x, y - 1)],
    #        ]
    #    if block_shape == "L_rev":
    #        coords = [
    #            [(x - 1, y - 1), (x, y - 1), (x + 1, y - 1), (x + 1, y)],
    #            [(x + 1, y - 1), (x + 1, y), (x + 1, y + 1), (x, y + 1)],
    #            [(x + 1, y + 1), (x, y + 1), (x - 1, y + 1), (x - 1, y)],
    #            [(x - 1, y + 1), (x - 1, y), (x - 1, y - 1), (x, y - 1)],
    #        ]
    #    if block_shape == "O":
    #        coords = [[(x - 1, y), (x, y), (x, y - 1), (x - 1, y - 1)]]
    #    if block_shape == "E":
    #        coords = [
    #            [(x - 1, y), (x, y), (x + 1, y), (x, y - 1)],
    #            [(x, y - 1), (x, y), (x, y + 1), (x + 1, y)],
    #            [(x + 1, y), (x, y), (x - 1, y), (x, y + 1)],
    #            [(x, y + 1), (x, y), (x, y - 1), (x - 1, y)],
    #        ]
    #    if block_shape == "Z":
    #        coords = [
    #            [(x - 1, y - 1), (x, y - 1), (x, y), (x + 1, y)],
    #            [(x + 1, y - 1), (x + 1, y), (x, y), (x, y + 1)],
    #        ]
    #    if block_shape == "Z_rev":
    #        coords = [
    #            [(x + 1, y - 1), (x, y - 1), (x, y), (x - 1, y)],
    #            [(x + 1, y + 1), (x + 1, y), (x, y), (x, y - 1)],
    #        ]
    #
    #    return coords[rotate_counter % len(coords)]

    def get_landed_coords(self):
        return [coords for shape, coords in self.landed_blocks]

    def current_block_mover(self):
        """
        Moves the current block downwards one square on the canvas
        """
        if any((x, y + 1) in self.coord_extractor() for (x, y) in self.get_block_shape(self.current_block_shape, self.current_block_center, self.rotate_counter)) or any(y + 1 == game_height for (x, y) in self.get_block_shape(self.current_block_shape, self.current_block_center, self.rotate_counter)):
            if self.current_block_shape not in self.landed_blocks:
                self.landed_blocks[self.current_block_shape] = []
            self.landed_blocks[self.current_block_shape].extend(
                self.get_block_shape(self.current_block_shape, self.current_block_center, self.rotate_counter)
            )
            self.full_line_clear()
            self.new_block()
        else:
            x, y = self.current_block_center
            self.current_block_center = (x, y + 1)

    def user_input_left(self):
        """
        Moves the current block to the left on the canvas
        """
        if any(x == 0 for (x, y) in self.get_block_shape(self.current_block_shape, self.current_block_center, self.rotate_counter)) or any(
            (x - 1, y) in self.coord_extractor() for x, y in self.get_block_shape(self.current_block_shape, self.current_block_center, self.rotate_counter)
        ):
            return
        x, y = self.current_block_center
        self.current_block_center = (x - 1, y)

    def user_input_right(self):
        """
        Moves the current block to the right on the canvas
        """
        if any(x == game_width - 1 for x, y in self.get_block_shape(self.current_block_shape, self.current_block_center, self.rotate_counter)) or any(
            (x + 1, y) in self.coord_extractor() for x, y in self.get_block_shape(self.current_block_shape, self.current_block_center, self.rotate_counter)
        ):
            return
        x, y = self.current_block_center
        self.current_block_center = (x + 1, y)

    def coord_extractor(self):
        coords = []
        for coord in self.landed_blocks.values():
            for (x, y) in coord:
                coords.append((x, y))
        return coords

    def block_rotator(self):
        """
        Rotates the current block
        """
        self.rotate_counter += 1
        # if any(x <= -1 or x >= game_width for (x, y) in self.get_block_shape(self.current_block_shape, self.current_block_center, self.rotate_counter)) or any(
        #    (x, y) in self.landed_blocks for x, y in self.get_block_shape(self.current_block_shape, self.current_block_center, self.rotate_counter)
        # ):
        if any(
            x not in range(game_width)
            or y >= game_height
            or (x, y) in self.coord_extractor()
            for (x, y) in self.get_block_shape(self.current_block_shape, self.current_block_center, self.rotate_counter)
        ):
            self.rotate_counter -= 1

    def full_line_clear(self):
        """
        Clears the line once it's fully populated with blocks
        """
        y_coordinates = [y for (x, y) in self.coord_extractor()]
        coordinates_counter = collections.Counter(y_coordinates)
        for x_line in range(game_height):
            count = coordinates_counter[x_line]
            if count == game_width:
                # TODO: root.after() here
                for letter, coord_list in self.landed_blocks.items():
                    # self.landed_blocks = {letter: [(a, b) for (a, b) in coord_list if b > x_line] + [(a, b+1) for (a, b) in coord_list if b < x_line]} #Why this doesn't work?
                    self.landed_blocks[letter] = [
                        (a, b) for (a, b) in coord_list if b > x_line
                    ] + [(a, b + 1) for (a, b) in coord_list if b < x_line]


class Board:
    def __init__(self, canvas, outline_color, width, height, block_shape, block_center, rotate_counter):
        self.canvas = canvas
        self.outline_color = outline_color
        self.width = width
        self.height = height
        self.block_shape = block_shape
        self.block_center = block_center
        self.rotate_counter = rotate_counter

    def draw_board(self):
        """
        Draws the board of rectangles on top of the canvas
        """
        x_gap = 0
        for x in range(self.width):
            y_gap = 0
            for y in range(self.height):
                self.canvas.create_rectangle(
                    x_gap,
                    y_gap,
                    x_gap + square_size,
                    y_gap + square_size,
                    fill=D_GREY,
                    outline=self.outline_color,
                )
                y_gap += square_size

            x_gap += square_size

    def draw_block(self, landed_blocks):
        """
        Draws the different shapes on the board
        """
        self.color_dict = {
            "L": YELLOW,
            "I": RED,
            "E": GREEN,
            "L_rev": BLUE,
            "Z": PURPLE,
            "Z_rev": TEAL,
            "O": ORANGE,
        }
        self.canvas.delete("block")
        self.canvas_small.delete('block')

        for x, y in self.get_block_shape(self.tetris_game.current_block_shape, self.tetris_game.current_block_center, self.tetris_game.rotate_counter):
            self.canvas.create_rectangle(
                x * square_size,
                y * square_size,
                x * square_size + square_size,
                y * square_size + square_size,
                tags="block",
                fill=self.color_dict[self.tetris_game.current_block_shape],
            )

        for letter, coord_list in self.tetris_game.landed_blocks.items():
            for (x, y) in coord_list:
                self.canvas.create_rectangle(
                    x * square_size,
                    y * square_size,
                    x * square_size + square_size,
                    y * square_size + square_size,
                    tags="block",
                    fill=self.color_dict[letter],
                )

        for x, y in self.get_block_shape(self.tetris_game.upcoming_block_shape, self.tetris_game.upcoming_block_center, 0):
            self.canvas_small.create_rectangle(
                    x * square_size,
                    y * square_size,
                    x * square_size + square_size,
                    y * square_size + square_size,
                    tags="block",
                    fill=self.color_dict[self.tetris_game.upcoming_block_shape],
            )

    def get_block_shape(self, block_shape, block_center, rotate_counter):
        (x, y) = block_center
        if block_shape == "I":
            coords = [
                [(x - 2, y), (x - 1, y), (x, y), (x + 1, y)],
                [(x, y - 2), (x, y - 1), (x, y), (x, y + 1)],
            ]
        if block_shape == "L":
            coords = [
                [(x - 1, y + 1), (x, y + 1), (x + 1, y + 1), (x + 1, y)],
                [(x - 1, y - 1), (x - 1, y), (x - 1, y + 1), (x, y + 1)],
                [(x + 1, y - 1), (x, y - 1), (x - 1, y - 1), (x - 1, y)],
                [(x + 1, y + 1), (x + 1, y), (x + 1, y - 1), (x, y - 1)],
            ]
        if block_shape == "L_rev":
            coords = [
                [(x - 1, y - 1), (x, y - 1), (x + 1, y - 1), (x + 1, y)],
                [(x + 1, y - 1), (x + 1, y), (x + 1, y + 1), (x, y + 1)],
                [(x + 1, y + 1), (x, y + 1), (x - 1, y + 1), (x - 1, y)],
                [(x - 1, y + 1), (x - 1, y), (x - 1, y - 1), (x, y - 1)],
            ]
        if block_shape == "O":
            coords = [[(x - 1, y), (x, y), (x, y - 1), (x - 1, y - 1)]]
        if block_shape == "E":
            coords = [
                [(x - 1, y), (x, y), (x + 1, y), (x, y - 1)],
                [(x, y - 1), (x, y), (x, y + 1), (x + 1, y)],
                [(x + 1, y), (x, y), (x - 1, y), (x, y + 1)],
                [(x, y + 1), (x, y), (x, y - 1), (x - 1, y)],
            ]
        if block_shape == "Z":
            coords = [
                [(x - 1, y - 1), (x, y - 1), (x, y), (x + 1, y)],
                [(x + 1, y - 1), (x + 1, y), (x, y), (x, y + 1)],
            ]
        if block_shape == "Z_rev":
            coords = [
                [(x + 1, y - 1), (x, y - 1), (x, y), (x - 1, y)],
                [(x + 1, y + 1), (x + 1, y), (x, y), (x, y - 1)],
            ]

        return coords[rotate_counter % len(coords)]



run_gui()
