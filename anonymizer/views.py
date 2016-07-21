from tkinter import Tk, Button, Label, Entry, filedialog
from tkinter.ttk import Progressbar
from PIL import ImageTk
from controllers import Observer

class MainForm(Tk, Observer):
    """ Defines a form object based from Tk in tkinter. """

    def __init__(self, ctrl_obj):
        """ Initializes the control object and controls of the form. """
        self.ctrl_anon = ctrl_obj
        self.resizable(0, 0)
        self._center_window(800, 500)
        self._reset_controls()
    
    def _reset_controls(self):
        """ Resets the controls on the form. """
        image = ImageTk.PhotoImage("bg.png")
        
        # Initialize controls
        self.lbl_bg = Label(self, image=image)
        self.lbl_anon = Label(self, bg="white", fg="#668FA7", font=("Courier", 14))
        self.lbl_id = Label(self, bg="white", fg="#668FA7", font=("Courier", 14))
        self.btn_dir_select = Button(self, text="Select data folder", command=self._btn_dir_press)
        self.btn_id = Button(self, text="Identify data", command=self._btn_id_press)
        self.btn_anon = Button(self, text="Anonymize data", command=self._btn_anon_press)
        self.tb_study = Entry(self, bg="#668FA7", fg="white")
        self.prg_id = Progressbar(self, orient="horizontal", length=200, mode="determinate")
        self.prg_anon = Progressbar(self, orient="horizontal", length=200, mode="determinate")

        # Place controls
        self.lbl_bg.place(x=0, y=0, relwidth=1, relheight=1)
        self.lbl_anon.place(x=400, y=400)
        self.lbl_id.place(x=400, y=325)
        self.btn_dir_select.place(x=250, y=250)
        self.btn_id.place(x=250, y=325)
        self.btn_anon.place(x=250, y=400)
        self.tb_study.place(x=250, y=175)
        self.prg_id.place(x=410, y=290)
        self.prg_anon.place(x=410, y=370)

        # Other formatting
        self.lbl_bg.image = image
        self.btn_id['state'] = "disabled"
        self.btn_anon['state'] = "disabled"
        self.prg_id['maximum'] = 100
        self.prg_anon['maximum'] = 100
