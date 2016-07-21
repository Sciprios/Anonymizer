from tkinter import Tk, Button, Label, Entry, filedialog
from tkinter.ttk import Progressbar
from PIL import ImageTk
from controllers import Observer

class MainForm(Tk, Observer):
    """ Defines a form object based from Tk in tkinter. """

    def __init__(self):
        """ Initializes the control object and controls of the form. """
        Tk.__init__(self)
        Observer.__init__(self)
        self.ctrl_anon = None
        self.resizable(0, 0)
        self._center_window(800, 500)
        self._reset_controls()
    
    def _reset_controls(self):
        """ Resets the controls on the form. """
        image = ImageTk.PhotoImage("bg.png")
        
        # Initialize controls
        self.lbl_bg = Label(self, image=image)
        self.lbl_dir = Label(self, bg="white", fg="#668FA7", font=("Courier", 14))
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

    def _btn_dir_press(self):
        """ Allows user to select their data folder. """
        self.ctrl_anon.reset()
        dir = filedialog.askdirectory(initialdir='.')
        if len(dir) > 0:
            self.lbl_dir.config(text=dir)
            self.btn_id['state'] = "enabled"
            self.btn_anon['state'] = "disabled"
        else:
            self.btn_id['state'] = "disabled"
            self.btn_anon['state'] = "disabled"
    
    def _btn_id_press(self):
        """ Calls the controller to identify data set. """
        self.ctrl_anon.identify(self.lbl_dir['text'])
        self.btn_anon['state'] = "enabled"
    
    def _btn_anon_press(self):
        """ Calls the controller to anonymize the data set. """
        if len(self.self.tb_study.get().get()) == 0:
            self.lbl_anon.config(text="Please enter a study name..")
        elif not self.self.tb_study.get().get().isalnum():
            self.lbl_anon.config(text="Please enter a valid study name..")
        else:
            self.ctrl_anon.anonymize(self.tb_study.get(), self.lbl_dir['text'])
    
    def notify(self):
        """ Updates the progress of the anonymization and identification processes. """
        self.prg_id['value'] = self.ctrl_anon.id_progress
        if self.prg_id['value'] == 100:
            self.lbl_id.config(text="Identification compelete")
        else:
            self.lbl_id.config(text="Identification in progress..")
        
        self.prg_anon['value'] = self.ctrl_anon.anon_progress
        if self.prg_anon['value'] == 100:
            self.lbl_id.config(text="Anonymization compelete")
        else:
            self.lbl_anon.config(text="Anonymization in progress..")

    def add_controller(self, control_anon):
        """ Adds a control anonymizer object to this gui. """
        self.ctrl_anon = control_anon
        self.ctrl_anon.subscribe(self)