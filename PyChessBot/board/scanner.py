import time
import pyautogui
import ctypes
from gui.gui import GUI


class Scanner:

    def __init__(self, interface):
        self.interface: GUI = interface
        self.first_pos = None
        self.second_pos = None

        # Button down = 0 or 1. Button up = -127 or -128
        self.state_left = self.button_state("left")

        # The epoch timestamp when the left mouse button was clicked
        self.last_click = None

    @staticmethod
    def button_state(side):
        if side == "left":
            return ctypes.windll.user32.GetKeyState(0x01) > 1
        else:
            return ctypes.windll.user32.GetKeyState(0x02) > 1

    # Tell the user to setup two points, the top-left corner and bottom-right corner of the chess board
    def retrieve_coordinates(self, callback):
        if not self.interface.running:
            self.interface.delay_task(1, self.retrieve_coordinates, callback)
            return
        pressed = self.button_state("left")

        if pressed is not self.state_left:  # Button state changed
            self.state_left = pressed
            if pressed:
                self.last_click = int(time.time())
                # logMessage('Left Button Pressed')
            else:
                # logMessage('Left Button Released')
                if self.last_click is not None and (time.time() - self.last_click) >= 1.5:
                    if self.first_pos is None:
                        self.interface.log('First position recorded')

                        # Fetch the position of the mouse
                        self.first_pos = pyautogui.position()
                        self.last_click = None
                    elif self.second_pos is None:
                        self.interface.log('Second position recorded')

                        # Fetch the position of the mouse
                        self.second_pos = pyautogui.position()

                        # Writing in the width and height of the chess board
                        width = self.second_pos[0] - self.first_pos[0]
                        height = self.second_pos[1] - self.first_pos[1]

                        # TODO: Start playing!
                        self.interface.log("Width: " + str(width))
                        self.interface.log("Height: " + str(height))

                        callback(width, height, self.first_pos)
                        return
        self.interface.delay_task(1, self.retrieve_coordinates, callback)
