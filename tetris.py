import random
import tkinter
import collections
import time
import pathlib
import sys
from functools import partial
from enum import Enum

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

block_letters = ["I", "L", "L_rev", "O", "E", "Z", "Z_rev"]

GameStatus = Enum("GameStatus", "in_progress, game_lost, paused")

try:
    # When an end user is running the app or exe created with pyinstaller,
    # sys._MEIPASS is the path to where images are, as a string.
    image_dir = pathlib.Path(sys._MEIPASS)
except AttributeError:
    # When a developer runs this program without pyinstaller, there is no
    # sys._MEIPASS attribute, and we need to find the images based on where
    # this file is.
    image_dir = pathlib.Path(__file__).parent / "images"


def set_button_image(button_image, event):
    event.widget.config(image=button_image)


def run_gui():

    root = tkinter.Tk()
    root.resizable(False, False)

    game_canvas = tkinter.Canvas(
        root,
        width=square_size * game_width,
        height=square_size * game_height,
        highlightthickness=1,
        highlightbackground="royal blue",
    )
    game_canvas.grid(row=1, sticky="nswe")

    topbar = tkinter.Frame(root, bg=D_GREY, relief="ridge")
    topbar.grid(row=0, columnspan=2, sticky="we")

    topbar_time = tkinter.Label(
        topbar, bg=D_GREY, text="00:00", font="digital-7", fg="orange", borderwidth=1
    )
    topbar_time.pack(side="left", padx=15)

    # This forces fixed size of topbar_canvas but allows it to resize constantly inside.
    topbar_canvas_container = tkinter.Frame(
        topbar,
        bg=D_GREY,
        relief="ridge",
        height=square_size * 3,
        width=square_size * 5,
    )
    topbar_canvas_container.pack(side="right")
    topbar_canvas_container.pack_propagate(0)  # don't overlook width and height

    topbar_canvas = tkinter.Canvas(
        topbar_canvas_container,
        bg=D_GREY,
        width=square_size * 4,
        height=square_size * 2,
        highlightthickness=0,
    )
    topbar_canvas.pack(side="right", expand=True)

    topbar_score = tkinter.Label(
        topbar, bg=D_GREY, text="0", font="digital-7", fg="orange", anchor="e"
    )
    topbar_score.pack(side="right", padx=20, fill="x", expand=True)

    sidebar = tkinter.Frame(root, bg=D_GREY)
    sidebar.grid(row=1, column=1, sticky="nsw")

    # image source https://cooltext.com/
    button_images = {}
    for filename in [
        "start.png",
        "hstart.png",
        "gamemode.png",
        "hgamemode.png",
        "highscores.png",
        "hhighscores.png",
    ]:
        transparent_image = tkinter.PhotoImage(file=(image_dir / filename))
        button_images[filename] = tkinter.PhotoImage(file=image_dir / "button.png")
        button_images[filename].tk.call(
            button_images[filename], "copy", transparent_image, "-compositingrule", "overlay"
        )

    tetris_gui = TetrisGUI(topbar_time, game_canvas, topbar_score, topbar_canvas)
    tetris_gui.move_block_down()
    tetris_gui.timer()

    new_game_button = tkinter.Button(
        sidebar,
        image=button_images["start.png"],
        borderwidth=0,
        highlightthickness=0,
        command=tetris_gui.new_game,
    )
    new_game_button.grid(sticky="n")

    game_mode_button = tkinter.Button(
        sidebar, image=button_images["gamemode.png"], borderwidth=0, highlightthickness=0
    )
    game_mode_button.grid(sticky="n")

    high_scores_button = tkinter.Button(
        sidebar, image=button_images["highscores.png"], borderwidth=0, highlightthickness=0
    )
    high_scores_button.grid(sticky="n")

    draw_board(game_canvas)

    root.bind("<Left>", tetris_gui.move_block_left)
    root.bind("<Right>", tetris_gui.move_block_right)
    root.bind("<Up>", tetris_gui.rotate_block)
    root.bind("<p>", tetris_gui.pause_game)
    root.bind("<Down>", tetris_gui.move_block_down_press)
    root.bind("<KeyRelease-Down>", tetris_gui.move_block_down_release)

    new_game_button.bind("<Enter>", partial(set_button_image, button_images["hstart.png"]))
    new_game_button.bind("<Leave>", partial(set_button_image, button_images["start.png"]))
    game_mode_button.bind("<Enter>", partial(set_button_image, button_images["hgamemode.png"]))
    game_mode_button.bind("<Leave>", partial(set_button_image, button_images["gamemode.png"]))
    high_scores_button.bind("<Enter>", partial(set_button_image, button_images["hhighscores.png"]))
    high_scores_button.bind("<Leave>", partial(set_button_image, button_images["highscores.png"]))

    root.title("Tetris – by The Philgrim, Arrinao, and Master Akuli")
    # root.iconphoto(False, tkinter.PhotoImage(file=image_name.png")) TODO: INSERT LATER

    root.mainloop()


def draw_board(canvas):
    """
    Draws the board consisting of 15x10 rectangles on top of the canvas before the game starts
    """
    x_gap = 0
    for x in range(game_width):
        y_gap = 0
        for y in range(game_height):
            canvas.create_rectangle(
                x_gap,
                y_gap,
                x_gap + square_size,
                y_gap + square_size,
                fill=D_GREY,
                outline=GREY,
            )
            y_gap += square_size

        x_gap += square_size


def rotate_point(point, center):
    x, y = center
    point_x, point_y = point
    a = point_x - x
    b = point_y - y
    return (x - b, y + a)


class Board:
    def __init__(self, canvas, current_block_center, small_board, topbar_score):
        self.canvas = canvas
        self.landed_blocks = {}
        self.current_block_center = current_block_center
        self.block_letter = random.choice(block_letters)
        self.rotate_counter = 0
        self.small_board = small_board
        self.topbar_score = topbar_score
        self.game_score = 0
        self.fast_down = False

    def draw_rectangle(self, x, y, tags, fill):
        self.canvas.create_rectangle(
            x * square_size,
            y * square_size,
            x * square_size + square_size,
            y * square_size + square_size,
            tags=tags,
            fill=fill,
        )

    def draw_block(self):
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

        for x, y in self.get_block_shape():
            self.draw_rectangle(x, y, "block", self.color_dict[self.block_letter])

        for letter, coord_list in self.landed_blocks.items():
            for (x, y) in coord_list:
                self.draw_rectangle(x, y, "block", self.color_dict[letter])

    def new_block(self):
        self.current_block_center = (int(game_width / 2), -2)
        self.block_letter = self.small_board.block_letter
        self.small_board.block_letter = random.choice(block_letters)
        self.small_board.resize_to_fit()
        self.small_board.draw_block()
        self.rotate_counter = 0
        self.fast_down = False

    def resize_to_fit(self):
        if self.block_letter == "L":
            self.canvas.config(width=square_size * 3, height=square_size * 2)
        if self.block_letter == "L_rev":
            self.canvas.config(width=square_size * 3, height=square_size * 2)
        if self.block_letter == "O":
            self.canvas.config(width=square_size * 2, height=square_size * 2)
        if self.block_letter == "E":
            self.canvas.config(width=square_size * 3, height=square_size * 2)
        if self.block_letter == "Z":
            self.canvas.config(width=square_size * 3, height=square_size * 2)
        if self.block_letter == "Z_rev":
            self.canvas.config(width=square_size * 3, height=square_size * 2)
        if self.block_letter == "I":
            self.canvas.config(width=square_size * 4, height=square_size * 1)

        if self.block_letter == "I":
            self.canvas.pack(pady=square_size / 2 + 10)
            self.current_block_center = (2, 0)
        else:
            self.canvas.pack(pady=10)
            self.current_block_center = (1, 1)

    def get_block_shape(self):
        (x, y) = self.current_block_center
        if self.block_letter == "I":
            coords = [[(x - 2, y), (x - 1, y), (x, y), (x + 1, y)]]
            coords.append([rotate_point(point, self.current_block_center) for point in coords[-1]])

        if self.block_letter == "L":
            coords = [[(x - 1, y), (x, y), (x + 1, y), (x + 1, y - 1)]]
            coords.append([rotate_point(point, self.current_block_center) for point in coords[-1]])
            coords.append([rotate_point(point, self.current_block_center) for point in coords[-1]])
            coords.append([rotate_point(point, self.current_block_center) for point in coords[-1]])

        if self.block_letter == "L_rev":
            coords = [[(x - 1, y - 1), (x - 1, y), (x, y), (x + 1, y)]]
            coords.append([rotate_point(point, self.current_block_center) for point in coords[-1]])
            coords.append([rotate_point(point, self.current_block_center) for point in coords[-1]])
            coords.append([rotate_point(point, self.current_block_center) for point in coords[-1]])

        if self.block_letter == "O":
            coords = [[(x - 1, y), (x, y), (x, y - 1), (x - 1, y - 1)]]

        if self.block_letter == "E":
            coords = [[(x - 1, y), (x, y), (x + 1, y), (x, y - 1)]]
            coords.append([rotate_point(point, self.current_block_center) for point in coords[-1]])
            coords.append([rotate_point(point, self.current_block_center) for point in coords[-1]])
            coords.append([rotate_point(point, self.current_block_center) for point in coords[-1]])

        if self.block_letter == "Z":
            coords = [[(x - 1, y - 1), (x, y - 1), (x, y), (x + 1, y)]]
            coords.append([rotate_point(point, self.current_block_center) for point in coords[-1]])

        if self.block_letter == "Z_rev":
            coords = [[(x + 1, y - 1), (x, y - 1), (x, y), (x - 1, y)]]
            coords.append([rotate_point(point, self.current_block_center) for point in coords[-1]])

        return coords[self.rotate_counter % len(coords)]

    def block_hits_bottom_if_it_moves_down(self):
        return any(
            (x, y + 1) in self.coord_extractor() for (x, y) in self.get_block_shape()
        ) or any(y + 1 == game_height for (x, y) in self.get_block_shape())

    def move_current_block_down(self):
        """
        Moves the current block downwards one square on the canvas
        """
        if self.block_hits_bottom_if_it_moves_down():
            if self.block_letter not in self.landed_blocks:
                self.landed_blocks[self.block_letter] = []
            self.landed_blocks[self.block_letter].extend(self.get_block_shape())
            self.full_line_clear()
            self.new_block()
        elif not self.fast_down:
            x, y = self.current_block_center
            self.current_block_center = (x, y + 1)

    def user_input_left(self):
        """
        Moves the current block to the left on the canvas
        """
        if any(x == 0 for (x, y) in self.get_block_shape()) or any(
            (x - 1, y) in self.coord_extractor() for x, y in self.get_block_shape()
        ):
            return
        x, y = self.current_block_center
        self.current_block_center = (x - 1, y)

    def user_input_right(self):
        """
        Moves the current block to the right on the canvas
        """
        if any(x == game_width - 1 for x, y in self.get_block_shape()) or any(
            (x + 1, y) in self.coord_extractor() for x, y in self.get_block_shape()
        ):
            return
        x, y = self.current_block_center
        self.current_block_center = (x + 1, y)

    def user_input_down(self):
        if self.fast_down and not self.block_hits_bottom_if_it_moves_down():
            x, y = self.current_block_center
            self.current_block_center = (x, y + 1)
            self.draw_block()
            self.canvas.after(25, self.user_input_down)

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
        if any(
            x not in range(game_width) or y >= game_height or (x, y) in self.coord_extractor()
            for (x, y) in self.get_block_shape()
        ):
            self.rotate_counter -= 1

    def full_line_clear(self):
        """
        Flashes the line once it's fully populated with blocks and clears it afterwards
        """
        full_lines = []
        y_coordinates = [y for (x, y) in self.coord_extractor()]
        coordinates_counter = collections.Counter(y_coordinates)
        for x_line in range(game_height):
            count = coordinates_counter[x_line]
            if count == game_width:
                full_lines.append(x_line)

        if full_lines:
            for flash in range(2):
                self.flasher(full_lines, "pink")
                self.canvas.update()
                time.sleep(0.1)
                self.flasher(full_lines, "black")
                self.canvas.update()
                time.sleep(0.1)
            self.canvas.delete("flash")

        for x_line in full_lines:
            for letter, coord_list in self.landed_blocks.items():
                self.landed_blocks[letter] = [(a, b) for (a, b) in coord_list if b > x_line] + [
                    (a, b + 1) for (a, b) in coord_list if b < x_line
                ]

        if len(full_lines) == 1:
            self.game_score += 10
        elif len(full_lines) == 2:
            self.game_score += 30
        elif len(full_lines) == 3:
            self.game_score += 60
        elif len(full_lines) == 4:
            self.game_score += 100
        self.topbar_score.config(text=self.game_score)

    def flasher(self, full_lines, fill):
        """
        Takes a list of full x lines and a color. Paints the blocks in the x_line with a given color.
        Used in conjuction with full_line clear for flashing purposes
        """
        for x in range(game_width):
            for x_line in full_lines:
                self.draw_rectangle(x, x_line, "flash", fill)


class TetrisGUI:
    def __init__(self, topbar_time, game_canvas, topbar_score, topbar_canvas):
        self.topbar_time = topbar_time
        self.topbar_canvas = topbar_canvas
        self.game_canvas = game_canvas
        self.topbar_score = topbar_score
        self.new_game()

    def game_over_check(self):
        y_coordinates = [y for (x, y) in self.main_board.coord_extractor()]
        if any(y < 0 for y in y_coordinates):
            self.game_status = GameStatus.game_lost

    def pause_game(self, event):
        if self.game_status == GameStatus.paused:
            self.game_status = GameStatus.in_progress
            self.paused_time += time.time() - self.pause_start
            self.timer()
        elif self.game_status == GameStatus.in_progress:
            self.game_status = GameStatus.paused
            self.pause_start = time.time()

    def move_block_left(self, event):
        if self.game_status == GameStatus.in_progress:
            self.main_board.user_input_left()
            self.main_board.draw_block()

    def move_block_right(self, event):
        if self.game_status == GameStatus.in_progress:
            self.main_board.user_input_right()
            self.main_board.draw_block()

    def move_block_down(self):
        if self.game_status == GameStatus.in_progress:
            self.main_board.move_current_block_down()
            self.game_over_check()
            self.main_board.draw_block()
        self.main_board.canvas.after(game_speed, self.move_block_down)

    def move_block_down_press(self, event):
        if not self.main_board.fast_down:
            self.main_board.fast_down = True
            self.main_board.user_input_down()

    def move_block_down_release(self, event):
        self.main_board.fast_down = False

    def rotate_block(self, event):
        if self.game_status == GameStatus.in_progress:
            self.main_board.block_rotator()
            self.main_board.draw_block()

    def timer(self):
        if self.game_status == GameStatus.in_progress:
            game_time = time.time() - self.start_time - self.paused_time
            self.topbar_time.config(text=f"{int(game_time / 60):02d}:{int(game_time % 60):02d}")
            self.topbar_time.after(1000, self.timer)

    def new_game(self):
        self.small_board = Board(
            self.topbar_canvas,
            (1, 1),
            None,
            None,
        )
        self.small_board.resize_to_fit()
        self.small_board.draw_block()

        self.main_board = Board(
            self.game_canvas,
            (int(game_width / 2), -2),
            self.small_board,
            self.topbar_score,
        )
        self.start_time = time.time()
        self.pause_start = 0
        self.paused_time = 0
        self.game_status = GameStatus.in_progress
        self.main_board.game_score = 0
        self.main_board.topbar_score.config(text=self.main_board.game_score)


run_gui()
