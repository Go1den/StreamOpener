from tkinter import Toplevel

from constants.fileConstants import FileConstants

class WindowHelper:

    @staticmethod
    def initializeWindow(window: Toplevel, parent, width: int, height: int, xoffset: int, yoffset: int, label: str):
        parent.window.attributes('-disabled', 1)
        window.iconbitmap(FileConstants.STREAMOPENER_ICON)
        if width == 0 or height == 0:
            window.geometry('+{x}+{y}'.format(x=parent.window.winfo_x() + xoffset, y=parent.window.winfo_y() + yoffset))
        else:
            window.geometry('{w}x{h}+{x}+{y}'.format(w=width, h=height, x=parent.window.winfo_x() + xoffset, y=parent.window.winfo_y() + yoffset))
        window.title(label)
        window.resizable(width=False, height=False)
        window.transient(parent.window)
        window.grab_set()

    @staticmethod
    def finalizeWindow(window: Toplevel, parent):
        window.deiconify()
        parent.window.wait_window(window)
        parent.window.attributes('-disabled', 0)
        parent.window.deiconify()
