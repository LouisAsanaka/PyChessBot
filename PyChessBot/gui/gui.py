import chess
import tkinter
import tkinter.font as font


class GUI:

    def __init__(self, color_callback):
        self.window = None
        self.outbox = None

        self.custom_font = None

        self.time_slider = None
        self.node_count_slider = None

        self.running = False
        self.start_button = None

        self.color = chess.WHITE
        self.color_button = None
        self.color_callback = color_callback

    def toggle_running(self):
        self.running = not self.running
        if self.running:
            self.start_button.config(text="Pause", background="red")
        else:
            self.start_button.config(text="Start", background="green")

    def toggle_color(self):
        self.color_callback()
        self.color = not self.color
        if self.color:
            self.color_button.config(text="Play as BLACK", background="red")
        else:
            self.color_button.config(text="Play as WHITE", background="green")

    def create_window(self):
        # Initialize the Tkinter window
        self.window = tkinter.Tk()
        self.custom_font = font.Font(family="Consolas", size=10)

        # Make the window always on top
        self.window.wm_attributes("-topmost", True)
        self.window.resizable(width=False, height=False)

        # The width and the height of the Tkinter window
        width = 300
        height = 500

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
        self.outbox = tkinter.Text(self.window, state='disabled', height=10, width=30,
                                   bg='#d3d3d3', font=self.custom_font)
        self.outbox.pack()

        self.time_slider = tkinter.Scale(
            self.window, label="Thinking Time (ms)", from_=500, to=10000, resolution=500,
            orient=tkinter.HORIZONTAL, length=250, font=self.custom_font
        )
        self.time_slider.set(2000)
        self.time_slider.pack()

        self.node_count_slider = tkinter.Scale(
            self.window, label="# of Nodes", from_=100000, to=1000000, resolution=10000,
            orient=tkinter.HORIZONTAL, length=250, font=self.custom_font
        )
        self.node_count_slider.set(100000)
        self.node_count_slider.pack()

        frame = tkinter.Frame(self.window, height=150, width=200)
        frame.pack_propagate(0)  # don't shrink
        frame.pack()

        self.start_button = tkinter.Button(frame, text="Start", background='green',
                                           command=self.toggle_running, font=self.custom_font)
        self.start_button.pack(fill=tkinter.BOTH, expand=1)

        self.color_button = tkinter.Button(frame, text="Play as BLACK", background='red',
                                           command=self.toggle_color, font=self.custom_font)
        self.color_button.pack(fill=tkinter.BOTH, expand=1)

    # Log a message in the outbox
    def log(self, message):
        self.outbox.configure(state='normal')
        self.outbox.insert(tkinter.END, message + "\n")  # Add the text to the textbox widget
        self.outbox.see(tkinter.END)
        self.outbox.configure(state='disabled')

    def delay_task(self, ms, func=None, *arg):
        return self.window.after(ms, func, *arg)
