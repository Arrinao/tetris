import random
import tkinter
import collections
import json
import time
import pathlib
import sys
from functools import partial
from enum import Enum
from tkinter import messagebox as mb
from tkinter import ttk

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

GameStatus = Enum("GameStatus", "in_progress, game_over, paused")

try:
    # When an end user is running the app or exe created with pyinstaller,
    # sys._MEIPASS is the path to where images are, as a string.
    image_dir = pathlib.Path(sys._MEIPASS)
except AttributeError:
    # When a developer runs this program without pyinstaller, there is no
    # sys._MEIPASS attribute, and we need to find the images based on where
    # this file is.
    image_dir = pathlib.Path(__file__).parent / "images"

try:
    with open(pathlib.Path(__file__).parent / "game_data.json", "r") as source:
        json_dict = json.load(source)
except FileNotFoundError:
    json_dict = {
        "game_speed": 300,
        "high_scores": [],
    }


def set_button_image(button_image, event):
    event.widget.config(image=button_image)


root = tkinter.Tk()
root.resizable(False, False)


def run_gui():
    game_frame = tkinter.Frame(
        root, width=square_size * game_width, height=square_size * game_height
    )
    game_frame.grid(row=1, sticky="nswe")
    game_frame.pack_propagate(0)

    global game_canvas
    game_canvas = tkinter.Canvas(
        game_frame,
        width=square_size * game_width,
        height=square_size * game_height,
        highlightthickness=1,
        highlightbackground="royal blue",
    )
    game_canvas.pack(fill="both", expand=True)

    topbar = tkinter.Frame(root, bg=D_GREY, relief="ridge")
    topbar.grid(row=0, columnspan=2, sticky="we")

    global topbar_time
    topbar_time = tkinter.Label(
        topbar, bg="black", text="00:00", font=("Digital-7 Mono", 20), fg="hot pink"
    )
    topbar_time.config(highlightbackground="red", highlightcolor="red")
    # For whatever reason, on Linux, Digital-7 font needs extra space inside the label (ipady)
    topbar_time.pack(side="left", padx=15, ipady=5)

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

    global topbar_canvas
    topbar_canvas = tkinter.Canvas(
        topbar_canvas_container,
        bg=D_GREY,
        width=square_size * 4,
        height=square_size * 2,
        highlightthickness=0,
    )
    topbar_canvas.pack(side="right", expand=True)

    global topbar_score
    topbar_score = tkinter.Label(
        topbar, bg="black", text="0", font=("Digital-7 Mono", 32), fg="lightblue", anchor="e"
    )
    topbar_score.pack(side="right", padx=20, ipady=5, fill="x", expand=True)

    sidebar = tkinter.Frame(root, bg=D_GREY)
    sidebar.grid(row=1, column=1, sticky="nsw")

    # image source https://cooltext.com/
    image_paths = {}
    button_images = [
        "start.png",
        "hstart.png",
        "return.png",
        "hreturn.png",
        "gamemode.png",
        "hgamemode.png",
        "clearlist.png",
        "hclearlist.png",
        "highscores.png",
        "hhighscores.png",
    ]
    for filename in button_images:
        transparent_image = tkinter.PhotoImage(file=(image_dir / filename))
        image_paths[filename] = tkinter.PhotoImage(file=image_dir / "button.png")
        image_paths[filename].tk.call(
            image_paths[filename], "copy", transparent_image, "-compositingrule", "overlay"
        )

    global tetris_control
    tetris_control = TetrisControl()

    style = ttk.Style(game_frame)
    style.theme_use("default")
    style.configure(
        "Treeview",
        rowheight=25,
        background=D_GREY,
        foreground="dark orange",
        fieldbackground=D_GREY,
        font=("Bahnschrift", 16),
    )
    style.map("Treeview", background=[("selected", "#BFBFBF")], foreground=[("selected", "black")])
    style.configure(
        "Treeview.Heading",
        background="gray4",
        foreground="orangered",
        font=("Arrr Matey BB", 22),
        padding=[5, 0],
    )
    global high_scores_treeview
    high_scores_treeview = ttk.Treeview(
        game_frame, columns=("Time Spent", "Game Speed", "Score"), height=10
    )
    # high_scores_treeview.tk.eval('''ttk::style theme use clam
    # ttk::style configure Treeview -fieldbackground gray7 -bordercolor red''')

    high_scores_treeview.column("#0", width=0, minwidth=0, stretch="NO")
    high_scores_treeview.column("Time Spent", width=100, minwidth=90, stretch="NO")
    high_scores_treeview.column("Game Speed", width=119, minwidth=130, stretch="NO")
    high_scores_treeview.column("Score", width=100, minwidth=90, stretch="NO")

    # Defining headings
    high_scores_treeview.heading("#0", text="", anchor="w")
    high_scores_treeview.heading("Time Spent", text="Time Spent", anchor="w")
    high_scores_treeview.heading("Game Speed", text="Game Speed", anchor="w")
    high_scores_treeview.heading("Score", text="Score", anchor="w")
    # game_frame = tkinter.Frame(root, width=square_size * game_width, height=square_size * game_height)
    lowbar = tkinter.Frame(high_scores_treeview, bg="black", height=72)
    lowbar.pack(side="bottom", fill="x")
    lowbar.pack_propagate(0)

    new_game_button = tkinter.Button(
        sidebar,
        image=image_paths["start.png"],
        borderwidth=0,
        highlightthickness=0,
        command=new_game_request,
    )
    new_game_button.grid(sticky="n")

    game_mode_button = tkinter.Button(
        sidebar, image=image_paths["gamemode.png"], borderwidth=0, highlightthickness=0
    )
    game_mode_button.grid(sticky="n")

    high_scores_button = tkinter.Button(
        sidebar,
        image=image_paths["highscores.png"],
        borderwidth=0,
        highlightthickness=0,
        command=display_high_scores,
    )
    high_scores_button.grid(sticky="n")

    return_button = tkinter.Button(
        lowbar,
        image=image_paths["return.png"],
        borderwidth=0,
        highlightthickness=0,
        command=display_high_scores,
    )
    return_button.pack(side="right", pady=(22, 0))

    clear_list_button = tkinter.Button(
        lowbar,
        image=image_paths["clearlist.png"],
        borderwidth=0,
        highlightthickness=0,
        command=clear_high_scores,
    )
    clear_list_button.pack(side="right", pady=(22, 0))

    root.bind("<Left>", tetris_control.move_block_left)
    root.bind("<Right>", tetris_control.move_block_right)
    root.bind("<Up>", tetris_control.rotate_block)
    root.bind("<p>", tetris_control.pause_game)
    root.bind("<Down>", tetris_control.move_block_down_press)
    root.bind("<KeyRelease-Down>", tetris_control.move_block_down_release)

    # Mouse wheel on top of game canvas moves the block sideways
    if sys.platform == "win32":

        def on_wheel(event):
            if event.delta > 0:  # Scrolled up
                tetris_control.move_block_left(event)
            else:
                tetris_control.move_block_right(event)

        game_canvas.bind("<MouseWheel>", on_wheel)
    elif sys.platform == "darwin":
        pass  # TODO: mouse wheel scrolling is smooth on macos, not sure what to do here
    else:
        game_canvas.bind("<Button-4>", tetris_control.move_block_left)
        game_canvas.bind("<Button-5>", tetris_control.move_block_right)

    new_game_button.bind("<Enter>", partial(set_button_image, image_paths["hstart.png"]))
    new_game_button.bind("<Leave>", partial(set_button_image, image_paths["start.png"]))
    game_mode_button.bind("<Enter>", partial(set_button_image, image_paths["hgamemode.png"]))
    game_mode_button.bind("<Leave>", partial(set_button_image, image_paths["gamemode.png"]))
    high_scores_button.bind("<Enter>", partial(set_button_image, image_paths["hhighscores.png"]))
    high_scores_button.bind("<Leave>", partial(set_button_image, image_paths["highscores.png"]))
    return_button.bind("<Enter>", partial(set_button_image, image_paths["hreturn.png"]))
    return_button.bind("<Leave>", partial(set_button_image, image_paths["return.png"]))
    clear_list_button.bind("<Enter>", partial(set_button_image, image_paths["hclearlist.png"]))
    clear_list_button.bind("<Leave>", partial(set_button_image, image_paths["clearlist.png"]))

    draw_board(game_canvas)

    root.title("Tetris – by The Philgrim, Arrinao, and Master Akuli")
    # root.iconphoto(False, tkinter.PhotoImage(file=image_name.png")) TODO: INSERT LATER


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


def get_high_scores_into_treeview():
    index = 0
    high_scores_treeview.delete(*high_scores_treeview.get_children())
    for index, high_score_dict in enumerate(json_dict["high_scores"]):
        if index % 2 == 0:
            tag = "odd_row"
        else:
            tag = "even_row"
        high_scores_treeview.insert(
            parent="",
            index="end",
            tags=tag,
            values=(
                tetris_control.game.time_formatter(high_score_dict["Time"]),
                high_score_dict["Game Speed"],
                high_score_dict["Score"],
            ),
        )
    high_scores_treeview.tag_configure("odd_row", background=D_GREY)
    high_scores_treeview.tag_configure("even_row", background="black")


def display_high_scores():
    get_high_scores_into_treeview()
    try:
        game_canvas.pack_info()  # Raises error if canvas isn't packed
    except tkinter.TclError:
        high_scores_treeview.pack_forget()
        game_canvas.pack(fill="both", expand=True)
    else:
        game_canvas.pack_forget()
        if tetris_control.game.status == GameStatus.in_progress:
            tetris_control.pause_game()
        high_scores_treeview.pack(side="top", fill="both", expand=True)


def clear_high_scores():
    if mb.askokcancel(
        "Clear high scores list?",
        "Are you sure you want to clear the high scores list?",
        parent=topbar_time,
    ):
        high_scores_treeview.delete(*high_scores_treeview.get_children())
        json_dict["high_scores"] = []
        with open("game_data.json", "w") as game_data:
            json.dump(json_dict, game_data)


def new_game():
    if tetris_control.game is not None:
        tetris_control.game.status = GameStatus.game_over
    high_scores_treeview.pack_forget()
    game_canvas.pack(fill="both", expand=True)
    small_board = Board(topbar_canvas, False)
    main_board = Board(game_canvas, True)
    game = Game(main_board, small_board, topbar_time)
    game.move_current_block_down()
    small_board.draw_block(game.get_upcoming_block_shape(), game.upcoming_block_letter)
    tetris_control.game = game


def new_game_request():
    if tetris_control.game.status != GameStatus.game_over:
        if tetris_control.game.status != GameStatus.paused:
            game_running = True
            tetris_control.pause_game()
        else:
            game_running = False

        if mb.askokcancel(
            "End current game?",
            "Do you wish to end the current game and start anew?",
            parent=topbar_time,
        ):
            new_game()
        else:
            if game_running:
                tetris_control.pause_game()
    else:
        new_game()


class Board:
    def __init__(self, canvas, is_main):
        self.canvas = canvas
        self.is_main = is_main

    def draw_rectangle(self, x, y, tags, fill):
        self.canvas.create_rectangle(
            x * square_size,
            y * square_size,
            x * square_size + square_size,
            y * square_size + square_size,
            tags=tags,
            fill=fill,
        )

    def draw_block(self, block, block_letter, landed_blocks=None):
        """
        Draws the different shapes on the board
        """
        color_dict = {
            "L": YELLOW,
            "I": RED,
            "E": GREEN,
            "L_rev": BLUE,
            "Z": PURPLE,
            "Z_rev": TEAL,
            "O": ORANGE,
        }
        self.canvas.delete("block")

        if self.is_main:
            for letter, coord_list in landed_blocks.items():
                for (x, y) in coord_list:
                    self.draw_rectangle(x, y, "block", color_dict[letter])
        else:
            self.resize_to_fit(block_letter)

        for x, y in block:
            self.draw_rectangle(x, y, "block", color_dict[block_letter])

    def resize_to_fit(self, block_letter):
        if block_letter == "L":
            self.canvas.config(width=square_size * 3, height=square_size * 2)
        if block_letter == "L_rev":
            self.canvas.config(width=square_size * 3, height=square_size * 2)
        if block_letter == "O":
            self.canvas.config(width=square_size * 2, height=square_size * 2)
        if block_letter == "E":
            self.canvas.config(width=square_size * 3, height=square_size * 2)
        if block_letter == "Z":
            self.canvas.config(width=square_size * 3, height=square_size * 2)
        if block_letter == "Z_rev":
            self.canvas.config(width=square_size * 3, height=square_size * 2)
        if block_letter == "I":
            self.canvas.config(width=square_size * 4, height=square_size * 1)

        if block_letter == "I":
            self.canvas.pack(pady=square_size / 2 + 10)
        else:
            self.canvas.pack(pady=10)


class Game:
    def __init__(self, main_board, small_board, topbar_time):
        self.landed_blocks = {}
        self.block_letter = random.choice(block_letters)
        self.upcoming_block_letter = random.choice(block_letters)
        self.current_block_center = (int(game_width / 2), -2)
        self.main_board = main_board
        self.small_board = small_board
        self.topbar_time = topbar_time
        self.fast_down = False
        self.start_time = time.time()
        self.rotate_counter = 0
        self.score = 0
        self.pause_start = 0
        self.paused_time = 0
        self.status = GameStatus.in_progress
        self.timer()
        topbar_score.config(text=self.score)

    def new_block(self):
        if self.status == GameStatus.in_progress:
            self.current_block_center = (int(game_width / 2), -2)
            self.block_letter = self.upcoming_block_letter
            self.upcoming_block_letter = random.choice(block_letters)
            self.small_board.draw_block(self.get_upcoming_block_shape(), self.upcoming_block_letter)
            self.rotate_counter = 0
            self.fast_down = False

    def get_block_shape(self):
        (x, y) = self.current_block_center
        coords = [self.get_coords_from_letter(self.block_letter, x, y)]

        if self.block_letter == "I" or self.block_letter == "Z" or self.block_letter == "Z_rev":
            coords.append([self.rotate_point(point) for point in coords[-1]])

        if self.block_letter == "L" or self.block_letter == "L_rev" or self.block_letter == "E":
            coords.append([self.rotate_point(point) for point in coords[-1]])
            coords.append([self.rotate_point(point) for point in coords[-1]])
            coords.append([self.rotate_point(point) for point in coords[-1]])

        return coords[self.rotate_counter % len(coords)]

    def get_upcoming_block_shape(self):
        if self.upcoming_block_letter == "I":
            return self.get_coords_from_letter(self.upcoming_block_letter, 2, 0)
        else:
            return self.get_coords_from_letter(self.upcoming_block_letter, 1, 1)

    def get_coords_from_letter(self, block_letter, x, y):
        if block_letter == "I":
            return [(x - 2, y), (x - 1, y), (x, y), (x + 1, y)]

        if block_letter == "L":
            return [(x - 1, y), (x, y), (x + 1, y), (x + 1, y - 1)]

        if block_letter == "L_rev":
            return [(x - 1, y - 1), (x - 1, y), (x, y), (x + 1, y)]

        if block_letter == "O":
            return [(x - 1, y), (x, y), (x, y - 1), (x - 1, y - 1)]

        if block_letter == "E":
            return [(x - 1, y), (x, y), (x + 1, y), (x, y - 1)]

        if block_letter == "Z":
            return [(x - 1, y - 1), (x, y - 1), (x, y), (x + 1, y)]

        if block_letter == "Z_rev":
            return [(x + 1, y - 1), (x, y - 1), (x, y), (x - 1, y)]

    def rotate_point(self, point):
        x, y = self.current_block_center
        point_x, point_y = point
        a = point_x - x
        b = point_y - y
        return (x - b, y + a)

    def block_hits_bottom_if_it_moves_down(self):
        return any(
            (x, y + 1) in self.coord_extractor() for (x, y) in self.get_block_shape()
        ) or any(y + 1 == game_height for (x, y) in self.get_block_shape())

    def move_current_block_down(self):
        """
        Moves the current block downwards one square on the canvas
        """
        if self.status == GameStatus.in_progress:
            if self.block_hits_bottom_if_it_moves_down():
                if self.block_letter not in self.landed_blocks:
                    self.landed_blocks[self.block_letter] = []
                self.landed_blocks[self.block_letter].extend(self.get_block_shape())
                self.full_line_clear()
                self.game_over()
                self.new_block()
            elif not self.fast_down:
                x, y = self.current_block_center
                self.current_block_center = (x, y + 1)
            self.main_board.draw_block(
                self.get_block_shape(), self.block_letter, self.landed_blocks
            )
        if self.status != GameStatus.game_over:
            self.main_board.canvas.after(game_speed, self.move_current_block_down)

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
        self.main_board.draw_block(self.get_block_shape(), self.block_letter, self.landed_blocks)

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
        self.main_board.draw_block(self.get_block_shape(), self.block_letter, self.landed_blocks)

    def user_input_down(self):
        if self.fast_down and not self.block_hits_bottom_if_it_moves_down():
            x, y = self.current_block_center
            self.current_block_center = (x, y + 1)
            self.main_board.draw_block(
                self.get_block_shape(), self.block_letter, self.landed_blocks
            )
            self.main_board.canvas.after(25, self.user_input_down)

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
        self.main_board.draw_block(self.get_block_shape(), self.block_letter, self.landed_blocks)

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
                self.main_board.canvas.update()
                time.sleep(0.1)
                self.flasher(full_lines, "black")
                self.main_board.canvas.update()
                time.sleep(0.1)
            self.main_board.canvas.delete("flash")

        for x_line in full_lines:
            for letter, coord_list in self.landed_blocks.items():
                self.landed_blocks[letter] = [(a, b) for (a, b) in coord_list if b > x_line] + [
                    (a, b + 1) for (a, b) in coord_list if b < x_line
                ]
        if len(full_lines) == 1:
            self.score += 10
        elif len(full_lines) == 2:
            self.score += 30
        elif len(full_lines) == 3:
            self.score += 60
        elif len(full_lines) == 4:
            self.score += 100
        topbar_score.config(text=self.score)

    def flasher(self, full_lines, fill):
        """
        Takes a list of full x lines and a color. Paints the blocks in the x_line with a given color.
        Used in conjuction with full_line clear for flashing purposes
        """
        for x in range(game_width):
            for x_line in full_lines:
                self.main_board.draw_rectangle(x, x_line, "flash", fill)

    def get_time(self):
        return time.time() - self.start_time - self.paused_time

    def time_formatter(self, get_time):
        return f"{int(get_time / 60):02d}:{int(get_time % 60):02d}"

    def timer(self):
        if self.status == GameStatus.in_progress:
            self.topbar_time.config(text=self.time_formatter(self.get_time()))
            self.topbar_time.after(1000, self.timer)

    def game_over(self):
        y_coordinates = [y for (x, y) in self.coord_extractor()]
        if any(y < 0 for y in y_coordinates):
            self.status = GameStatus.game_over
            json_dict["high_scores"].append(
                {"Time": int(self.get_time()), "Game Speed": game_speed, "Score": self.score}
            )
            with open("game_data.json", "w") as game_data:
                json.dump(json_dict, game_data)


class TetrisControl:
    def __init__(self):
        self.game = None

    def pause_game(self, event=None):
        if self.game.status == GameStatus.paused:
            self.game.status = GameStatus.in_progress
            self.game.paused_time += time.time() - self.game.pause_start
            self.game.timer()
        elif self.game.status == GameStatus.in_progress:
            self.game.status = GameStatus.paused
            self.game.pause_start = time.time()

    def move_block_left(self, event):
        if self.game.status == GameStatus.in_progress:
            self.game.user_input_left()

    def move_block_right(self, event):
        if self.game.status == GameStatus.in_progress:
            self.game.user_input_right()

    def move_block_down_press(self, event):
        if self.game.status == GameStatus.in_progress and not self.game.fast_down:
            self.game.fast_down = True
            self.game.user_input_down()

    def move_block_down_release(self, event):
        self.game.fast_down = False

    def rotate_block(self, event):
        if self.game.status == GameStatus.in_progress:
            self.game.block_rotator()


run_gui()
new_game()
root.mainloop()
