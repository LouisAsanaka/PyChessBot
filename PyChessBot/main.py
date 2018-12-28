from gui.gui import GUI
from board.scanner import Scanner


def main():
    interface = GUI()
    interface.create_window()

    scanner = Scanner(interface)
    scanner.capture_mouse()

    interface.window.mainloop()


main()

