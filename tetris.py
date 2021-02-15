import tkinter

game_speed = 800
rec_x = rec_y = 35
width = 10
height = 20
BLACK = "#000000"
BLUE = "#0029ff"
RED = "#ff1700"
GREEN = "#05ff00"
GREY = "#666666"
D_GREY = "#383838"


def run_gui():

    root = tkinter.Tk()
    root.resizable(False, False)

    tetris_canvas = tkinter.Canvas(root, width=rec_x * 10, height=rec_x * 20)
    tetris_canvas.grid()

    tetris_gui = TetrisGUI(game_speed, tetris_canvas)
    tetris_gui.tetris_game.new_block()

    root.bind("<Left>", lambda event: tetris_gui.tetris_game.user_input_left())
    root.bind("<Right>", lambda event: tetris_gui.tetris_game.user_input_right())

    tetris_gui.draw_board()
    tetris_gui.draw_block()
    tetris_gui.block_mediator()
    root.mainloop()

    tetris_gui.tetris_game.block_rotator()


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
        for x in range(10):
            y_gap = 0
            for y in range(20):
                self.canvas.create_rectangle(
                    x_gap,
                    y_gap,
                    x_gap + rec_x,
                    y_gap + rec_y,
                    fill=D_GREY,
                    outline=GREY,
                )
                y_gap += 35

            x_gap += 35

    def draw_block(self):
        """
        Draws the different shapes on the board
        """
        previous_block_clear = self.tetris_game.previous_block

        current_block_draw = self.tetris_game.current_block

        if (
            previous_block_clear is not None
            and previous_block_clear not in self.tetris_game.landed_blocks
        ):
            for coord in previous_block_clear:
                self.canvas.delete()

        for x, y in current_block_draw:
            self.canvas.create_rectangle(
                x * rec_x, y * rec_y, x * rec_x + rec_x, y * rec_x + rec_x, fill=RED
            )  # TODO: Find way to assign whole block to a variable so it
            # can be deleted

    def block_mediator(self):
        """
        Has the responsibility to call block_mover() and draw_block() to
        simulate the blocks moving downwards on the canvas
        """
        self.tetris_game.block_mover()
        self.draw_block()
        self.canvas.after(game_speed, self.block_mediator)


class TetrisGame:
    def __init__(self):
        self.landed_blocks = [(6, 10)]
        self.previous_block = None
        self.current_block = None
        self.upcoming_block = None

    def new_block(self):
        """
        Chooses a random block from "blocks" and assigns it to
        self.current_block
        """
        x = int(width / 2)
        y = 0
        test_block = [(x, y)]
        blocks = {
            "L": [(x - 1, y), (x, y), (x + 1, y), (x + 1, y + 1)],
            "L_rev": [(x - 1, y + 1), (x - 1, y), (x, y), (x + 1, y)],
            "O": [(x - 1, y), (x, y), (x - 1, y + 1), (x, y + 1)],
            "E": [(x, y), (x - 1, y + 1), (x, y + 1), (x + 1, y + 1)],
            "Z": [(x - 1, y), (x, y), (x, y + 1), (x - 1, y + 1)],
            "Z_rev": [(x + 1, y), (x, y), (x, y + 1), (x - 1, y + 1)],
            "I": [(x - 2, y), (x - 1, y), (x, y), (x + 1, y)],
        }
        if self.upcoming_block is None:
            # self.current_block = random.choice(list(blocks.values()))
            self.current_block = test_block  # Remove when code is working
        else:
            self.current_block = self.upcoming_block
        self.previous_block = self.current_block
        # self.upcoming_block = random.choice(list(blocks.values()))
        self.upcoming_block = test_block  # Remove when code is working

    def user_input_left(self, event):
        """
        Moves the current block to the left on the canvas
        """
        left = []
        print("Going left!")
        for (x, y) in self.current_block:
            left.append((x + 1, y))
        self.current_block = left

    def user_input_right(self, event):
        """
        Moves the current block to the right on the canvas
        """
        right = []
        print("Going right!")
        for (x, y) in self.current_block:
            right.append((x + 1, y))
        self.current_block = right

    def block_mover(self):
        """
        Moves the current block downwards one square on the canvas
        """
        if any(
            (x, y + 1) in self.landed_blocks for (x, y) in self.current_block
        ) or any(y + 1 == height for (x, y) in self.current_block):
            for coord in self.current_block:
                self.landed_blocks.append(coord)
            # print(self.landed_blocks)
            self.new_block()
        else:
            self.current_block = [(x, y + 1) for x, y in self.current_block]
            return self.current_block
            for block in self.current_block:  # TODO: Remove this for loop when
                print(block[0], block[1])  # everything works

    def block_rotator(self, event):
        rotate = []
        for (x, y) in self.current_block:
            rotate.append((y, x))
        self.current_block = rotate


run_gui()
