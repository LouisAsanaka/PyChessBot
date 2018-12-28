import tkinter


class GUI:

    def __init__(self):
        self.window = None
        self.outbox = None

        self.time_slider = None
        self.node_count_slider = None

        self.start = False
        self.button = None

    def toggle_start(self):
        self.start = not self.start
        if self.start:
            self.button.config(text="Pause", background="red")
        else:
            self.button.config(text="Start", background="green")

    def create_window(self):
        # Initialize the Tkinter window
        self.window = tkinter.Tk()

        # Make the window always on top
        self.window.wm_attributes("-topmost", True)
        self.window.resizable(width=False, height=False)

        # The width and the height of the Tkinter window
        width = 300
        height = 450

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
        self.outbox = tkinter.Text(self.window, state='disabled', height=10, width=30, bg='#d3d3d3')
        self.outbox.pack()

        self.time_slider = tkinter.Scale(
            self.window, label="Thinking Time (ms)", from_=500, to=10000, resolution=500,
            orient=tkinter.HORIZONTAL, length=250
        )
        self.time_slider.set(2000)
        self.time_slider.pack()

        self.node_count_slider = tkinter.Scale(
            self.window, label="# of Nodes", from_=100000, to=1000000, resolution=10000,
            orient=tkinter.HORIZONTAL, length=250
        )
        self.node_count_slider.set(100000)
        self.node_count_slider.pack()

        frame = tkinter.Frame(self.window, height=100, width=200)
        frame.pack_propagate(0)  # don't shrink
        frame.pack()

        self.button = tkinter.Button(frame, text="Start", background='green', command=self.toggle_start)
        self.button.pack(fill=tkinter.BOTH, expand=1)

    # Log a message in the outbox
    def log(self, message):
        self.outbox.configure(state='normal')
        self.outbox.insert(tkinter.END, message + "\n")  # Add the text to the textbox widget
        self.outbox.see(tkinter.END)
        self.outbox.configure(state='disabled')

    def delay_task(self, ms, func=None, *arg):
        self.window.after(ms, func, *arg)
