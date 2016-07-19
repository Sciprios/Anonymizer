try:
    from threading import Thread
except ImportError as e:
    print("Could not import core libraries, exitting.")
    print(e)
    exit()


class CustomGuiThread(Thread):
    """ Thread to update the gui in someway. """

    def __init__(self, gui=None, target=None, other_args=None):
        """ Initializes instance variables."""
        Thread.__init__(self, target=target, args=other_args)
        self.gui = gui
        self.tgt = target


class IdenThread(CustomGuiThread):
    """ Thread to identify the files."""

    def run(self):
        """ Start the naonimization process. """
        self.gui.lbl_id.config(text="Identifying data..")
        self.gui.btn_folder['state'] = 'disabled'
        self.gui.btn_identify['state'] = 'disabled'
        self.gui.btn_anonymize['state'] = 'disabled'
        self.gui.controller._only_identify()
        self.gui.lbl_id.config(text="Identification complete.")
        self.gui.btn_anonymize['state'] = 'normal'
        self.gui.btn_identify['state'] = 'disabled'
        self.gui.btn_folder['state'] = 'disabled'


class AnonThread(CustomGuiThread):
    """ Thread to anonimize the data."""

    def run(self):
        """ Start the naonimization process. """
        self.gui.lbl_anon.config(text="Anonymizing data..")
        self.gui.btn_folder['state'] = 'disabled'
        self.gui.btn_identify['state'] = 'disabled'
        self.gui.controller._only_anonymize()
        self.gui.lbl_anon.config(text="Anonymization complete.")
        self.gui.lbl_csv_dir.config(fg="#668FA7")
        self.gui.btn_anonymize['state'] = 'disabled'
        self.gui.btn_identify['state'] = 'disabled'
        self.gui.btn_folder['state'] = 'normal'

