try:
    from tkinter import Tk, Label, Button, filedialog
    from PIL import ImageTk
except ImportError as e:
    print("Could not import core libraries, exitting.")
    print(e)
    exit()

class MainScreen(Tk):
    """ Form on screen."""

    def __init__(self):
        Tk.__init__(self)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.resizable(0, 0)
        self.center_window(800, 500)
        self.add_controls()
    
    def add_controls(self):
        """ Sets up controls on the window. """
        # Background Image
        self.pnl_background = self.create_background_image("static\\bg_800_500_txt.png")

        # Create buttons
        self.btn_Folder = Button(self, text="Select a directory", command=self._btn_folder)
        self.btn_Folder.place(x=250, y=250)

        self.btn_identify = Button(self, text="Identify data", command=self._btn_identify)
        self.btn_identify.place(x=250, y=325)

        self.btn_anonymize = Button(self, text="Anonymize data", command=self._btn_anonymize)
        self.btn_anonymize.place(x=250, y=400)

    def create_background_image(self, path):
        """ Sets the background image of this form. """
        image = ImageTk.PhotoImage(file = path)
        pnl_background = Label(self, image=image)
        pnl_background.image = image
        pnl_background.place(x=0, y=0, relwidth=1, relheight=1)

        return pnl_background
        

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
    
    def _btn_folder(self):
        """ Executes when btn_Folder is pressed. """
        filedialog.askdirectory(initialdir='.')
    
    def _btn_identify(self):
        """ Executes when the identify button is pressed. """
        pass
    
    def _btn_anonymize(self):
        """ Executes when the anonymize button is pressed. """
        pass