try:
    from tkinter import Tk, Label, Button, filedialog, Entry, Canvas, messagebox
    from PIL import ImageTk
    from threading import Thread
except ImportError as e:
    print("Could not import core libraries, exitting.")
    print(e)
    exit()

class MainScreen(Tk):
    """ Form on screen."""

    def __init__(self, anonymizer):
        """ Instantiates the form on screen with the controller provided. """
        Tk.__init__(self)
        self.controller = anonymizer
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
        self.btn_Folder['state'] = 'normal'
        self.btn_Folder.place(x=250, y=250)

        self.btn_identify = Button(self, text="Identify data", command=self._btn_identify)
        self.btn_identify['state'] = 'disabled'
        self.btn_identify.place(x=250, y=325)

        self.btn_anonymize = Button(self, text="Anonymize data", command=self._btn_anonymize)
        self.btn_anonymize['state'] = 'disabled'
        self.btn_anonymize.place(x=250, y=400)

        # Text field
        self.txt_study_name = Entry(self, bg="#668FA7", fg="white")
        self.txt_study_name.bind("<Key>")
        self.txt_study_name.place(x=250, y=175)

        # Labels
        self.lbl_directory = Label(self, bg="white", fg="#668FA7", font=("Courier", 14))
        self.lbl_directory.place(x=375, y=250)

        self.lbl_id = Label(self, bg="white", fg="#668FA7", font=("Courier", 14))
        self.lbl_id.place(x=375, y=325)

        self.lbl_anon = Label(self, bg="white", fg="#668FA7", font=("Courier", 14))
        self.lbl_anon.place(x=375, y=400)

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
        self.controller.folder_path = filedialog.askdirectory(initialdir='.')
        self.btn_Folder['state'] = 'normal'
        self.btn_identify['state'] = 'normal'
        self.btn_anonymize['state'] = 'disabled'
        self.lbl_directory.config(text=self.controller.folder_path)
    
    def _btn_identify(self):
        """ Executes when the identify button is pressed. """
        self.lbl_id.config(text="Identifying participants..")
        self.btn_Folder['state'] = 'disabled'
        self.btn_identify['state'] = 'disabled'
        identify_thread = Thread(target=self.controller._only_identify)
        identify_thread.start()

        identify_thread.join()

        self.lbl_id.config(text="Identifying participants..")
        self.btn_identify['state'] = 'normal'
        self.btn_anonymize['state'] = 'normal'
        self.btn_Folder['state'] = 'normal'
        self.lbl_id.config(text="Found {} patient folder(s).".format(len(self.controller.participant_folders)))
    
    def _btn_anonymize(self):
        """ Executes when the anonymize button is pressed. """
        if len(self.txt_study_name.get()) == 0:
            self.lbl_anon.config(text="Please enter a study name..")
        elif not self.txt_study_name.get().isalnum():
            self.lbl_anon.config(text="Please enter a valid study name..")
        else:
            self.lbl_anon.config(text="Anonymizing data..")
            self.btn_Folder['state'] = 'disabled'
            self.btn_identify['state'] = 'disabled'
            anonymize_thread = Thread(target=self.controller._only_anonymize)
            anonymize_thread.start()
            anonymize_thread.join()
            self.lbl_anon.config(text="Anonymization complete.")
            self.btn_anonymize['state'] = 'disabled'
            self.btn_identify['state'] = 'disabled'
            self.btn_Folder['state'] = 'normal'
