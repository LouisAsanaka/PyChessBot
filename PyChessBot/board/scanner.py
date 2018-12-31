import time
import pyautogui
import ctypes
import os
from gui.gui import GUI

# Source: https://docs.microsoft.com/en-us/windows/desktop/inputdev/virtual-key-codes
VK_LBUTTON = 0x01
VK_RBUTTON = 0x02


class Scanner:

    def __init__(self, parent_dir, interface):
        self.parent_dir = parent_dir
        self.interface: GUI = interface
        self.first_pos = None
        self.second_pos = None

        # Button down = 0 or 1. Button up = -127 or -128
        self.state_left = self.button_state("left")

        # The epoch timestamp when the left mouse button was clicked
        self.last_click = None

        self.task_id = -1

    @staticmethod
    def button_state(side):
        if side == "left":
            return ctypes.windll.user32.GetKeyState(VK_LBUTTON) > 1
        else:
            return ctypes.windll.user32.GetKeyState(VK_RBUTTON) > 1

    # Tell the user to setup two points, the top-left corner and bottom-right corner of the chess board
    def retrieve_coordinates(self, callback):
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

                        with open(os.path.join(self.parent_dir, "board_pos.dat"), "w") as file:
                            file.write(str(self.first_pos[0]) + "," + str(self.first_pos[1]) + "\n")
                            file.write(str(width) + "," + str(height))

                        self.interface.log("Width: " + str(width), level="debug")
                        self.interface.log("Height: " + str(height), level="debug")

                        self.task_id = -1
                        callback(width, height, self.first_pos)
                        return
        self.task_id = self.interface.delay_task(10, self.retrieve_coordinates, callback)
