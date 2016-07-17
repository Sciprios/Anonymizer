try:
    import os
    import sys
    # Find the application folder path
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    # Insert path if not found
    if path not in sys.path:
        sys.path.insert(1, path)
    del path

    from unittest import mock, TestCase
    from classes.processor import Anonymizer
    from classes.forms import MainScreen

except Exception:
    print("Could not import all modules, exitting.")
    exit()

class TestMainScreen(TestCase):
    """ Class to test the main screen """

    def test_center_window(self):
        """ Tests the centering of a window. """
        anon = Anonymizer("FAKE_STUDY")
        screen = MainScreen(anon)

        # Mock out a bunch of methods required.
        screen.winfo_screenwidth = mock.Mock(return_value=600)
        screen.winfo_screenheight = mock.Mock(return_value=600)
        screen.geometry = mock.Mock()

        screen._center_window(600, 600)

        screen.geometry.assert_called_with("600x600+0+0")

    @mock.patch('classes.forms.MainScreen.__init__')
    @mock.patch('classes.forms.Label.place')
    @mock.patch('classes.forms.Label.__init__')
    @mock.patch('classes.forms.ImageTk.PhotoImage')
    def test_set_bg_image(self, pht_img, lbl_init, lbl_plc, ms_init):
        """ Tests the method to set the background image. """
        # Mock out some stuff
        ms_init.return_value = None
        lbl_init.return_value = None
        
        screen = MainScreen()

        screen._create_background_image("TEST_PATH")

        # Check
        pht_img.assert_called_with(file="TEST_PATH")
        lbl_plc.assert_called_with(x=0, y=0, relwidth=1, relheight=1)

    def test_click_btn_folder(self):
        """ Ensures correct actions are taken upon selecting to choose a folder. """
        pass
    
    def test_click_btn_identify(self):
        """ Ensures correct actions are taken upon selecting to identify participants. """
        pass
    
    def test_click_btn_anonymize(self):
        """ Ensures correct actions are taken upon selecting to anonymize data set. """
        pass