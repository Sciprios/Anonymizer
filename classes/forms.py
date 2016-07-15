try:
    from tkinter import Tk, Label
    from PIL import ImageTk
except ImportError as e:
    print("Could not import core libraries, exitting.")
    exit()

class MainScreen(Tk):
    """ Form on screen."""

    def __init__(self):
        Tk.__init__(self)
        self.resizable(0, 0)
        self.center_window(800, 500)
        self.set_background_image("static\\bg_800_500.png")

    def set_background_image(self, path):
        """ Sets the background image of this form. """
        image = ImageTk.PhotoImage(file = path)
        pnl_background = Label(self, image=image)
        pnl_background.pack(side='top', fill='both', expand='yes')
        pnl_background.image = image

    def center_window(self, new_width, new_height):
        """ Centers this form. """
        width = new_width
        height = new_height
        scr_width = self.winfo_screenwidth()
        scr_height = self.winfo_screenheight()

        # Calculate dimensions
        x = (scr_width/2) - (width/2)
        y = (scr_height/2) - (height/2)

        # Set window dimensions
        geo = str(width) + "x" + str(height) + "+" + str(x)[:-2] + "+" + str(y)[:-2]
        self.geometry(geo)