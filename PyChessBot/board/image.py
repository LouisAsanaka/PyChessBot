from mss import mss
from PIL import Image
from math import isclose


class BoardImage:

    def __init__(self, coord, width, height):
        self.region = {
            "top": coord[1],
            "left": coord[0],
            "width": width,
            "height": height
        }
        self.sct = mss()

    def snap(self):
        return self.sct.grab(self.region)

    @staticmethod
    def save(screenshot, filename):
        img = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")
        img.save(f"{filename}.png")

    @staticmethod
    def is_close(p1, p2):
        return isclose(p1[0], p2[0], abs_tol=8) and \
            isclose(p1[1], p2[1], abs_tol=8) and \
            isclose(p1[2], p2[2], abs_tol=8)
