import chess
import tkinter
import tkinter.font as font
import os
import numpy as np

DEBUG = True


class GUI:

    def __init__(self, color_callback, set_coordinates_callback):
        self.window = None
        self.outbox = None

        self.custom_font = None
        self.text_bg_color = "#a1dbcd"

        self.time_slider = None
        self.node_count_slider = None

        self.running = False
        self.start_button = None

        self.color = chess.WHITE
        self.color_button = None
        self.color_callback = color_callback

        self.loaded = False
        self.load_button = None
        self.set_coordinates_callback = set_coordinates_callback

    def toggle_running(self):
        self.running = not self.running
        if self.running:
            self.log("Starting...")
            self.start_button.config(text="Pause", background="red")
        else:
            self.log("Pausing...")
            self.start_button.config(text="Start", background="green")

    def toggle_color(self):
        self.color_callback()
        self.color = not self.color
        if self.color:
            self.log("Playing as WHITE")
            self.color_button.config(text="Play as BLACK", background="red")
        else:
            self.log("Playing as BLACK")
            self.color_button.config(text="Play as WHITE", background="green")

    def load_board_pos(self):
        if self.loaded:
            self.log("Cannot load position again.")
            return
        if not os.path.isfile("../board_pos.dat"):
            self.log("No position saved!")
        else:
            data = np.genfromtxt(r"../board_pos.dat", delimiter=",", dtype=int)
            if len(data) != 2:
                self.log("Corrupt position file.", level="error")
            else:
                (x, y), (width, height) = data

                self.log("Width: " + str(width), level="debug")
                self.log("Height: " + str(height), level="debug")

                self.log("Loaded board position.")
                self.loaded = True
                self.set_coordinates_callback(int(width), int(height), (int(x), int(y)))

    def create_window(self):
        # Initialize the Tkinter window
        self.window = tkinter.Tk()
        self.window.config(background=self.text_bg_color)
        self.window.title("PyChessBot")
        self.window.iconbitmap("../data/favicon.ico")
        self.custom_font = font.Font(family="Segoe UI Semibold", size=10)

        # Make the window always on top
        self.window.wm_attributes("-topmost", True)
        self.window.resizable(width=False, height=False)

        # The width and the height of the Tkinter window
        width = 300
        height = 550

        # Get screen width and height
        ws = self.window.winfo_screenwidth()  # width of the screen
        hs = self.window.winfo_screenheight()  # height of the screen

        # calculate x and y coordinates for the Tkinter window
        x = ((4 * ws) / 5) - (width / 2)
        y = (hs / 3) - (height / 2)

        # Set the dimensions of the screen 
        # and where it is placed
        self.window.geometry('%dx%d+%d+%d' % (width, height, x, y))

        # Add the textbox widget
        self.outbox = tkinter.Text(self.window, state='disabled', height=8, width=30,
                                   bg='#d3d3d3', font=self.custom_font)
        self.outbox.pack(pady=10)

        self.time_slider = tkinter.Scale(
            self.window, label="Thinking Time (ms)", from_=500, to=10000, resolution=500,
            orient=tkinter.HORIZONTAL, length=250, font=self.custom_font, bg=self.text_bg_color,
            highlightthickness=0
        )
        self.time_slider.set(2000)
        self.time_slider.pack(pady=2)

        self.node_count_slider = tkinter.Scale(
            self.window, label="# of Nodes", from_=100000, to=1000000, resolution=10000,
            orient=tkinter.HORIZONTAL, length=250, font=self.custom_font, bg=self.text_bg_color,
            highlightthickness=0
        )
        self.node_count_slider.set(100000)
        self.node_count_slider.pack(pady=10)

        frame = tkinter.Frame(self.window, height=150, width=200)
        frame.pack_propagate(0)  # don't shrink
        frame.pack()

        self.start_button = tkinter.Button(frame, text="Start", background='green',
                                           command=self.toggle_running, font=self.custom_font)
        self.start_button.pack(fill=tkinter.BOTH, expand=1)

        self.color_button = tkinter.Button(frame, text="Play as BLACK", background='red',
                                           command=self.toggle_color, font=self.custom_font)
        self.color_button.pack(fill=tkinter.BOTH, expand=1)

        self.load_button = tkinter.Button(frame, text="Load board position", background='orange',
                                          command=self.load_board_pos, font=self.custom_font)
        self.load_button.pack(fill=tkinter.BOTH, expand=1)

    # Log a message in the outbox
    def log(self, message, level="normal"):
        self.outbox.configure(state='normal')
        if level == "normal":
            message = "" + message
        elif level == "debug" and DEBUG:
            message = "> " + message
        elif level == "error":
            message = "ERROR " + message
        self.outbox.insert(tkinter.END, message + "\n")  # Add the text to the textbox widget
        self.outbox.see(tkinter.END)
        self.outbox.configure(state='disabled')

    def cancel_task(self, task_id):
        self.window.after_cancel(task_id)

    def delay_task(self, ms, func=None, *arg):
        return self.window.after(ms, func, *arg)
