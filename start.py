from anonymizer.controllers import ControlAnonymizer
from anonymizer.views import MainForm

frm = MainForm()
controller = ControlAnonymizer()
frm.add_controller(controller)
controller.start()