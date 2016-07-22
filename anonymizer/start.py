from controllers import ControlAnonymizer
from views import MainForm

frm = MainForm()
controller = ControlAnonymizer(frm)
frm.add_controller(controller)
controller.start()