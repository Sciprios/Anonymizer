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

    @mock.patch('classes.forms.MainScreen.__init__')
    def test_click_btn_folder(self, ms_ini):
        """ Ensures correct actions are taken upon selecting to choose a folder. """
        ms_ini.return_value = None
        screen = MainScreen()

        screen._get_folder = mock.Mock()
        screen._get_folder.return_value = "TEST_666"
        screen.controller = mock.Mock()
        screen.btn_folder = {}
        screen.btn_identify = {}
        screen.btn_anonymize = {}
        screen.lbl_directory = mock.Mock()

        screen._btn_folder()

        assert screen.btn_folder['state'] == 'normal'
        assert screen.btn_identify['state'] == 'normal'
        assert screen.btn_anonymize['state'] == 'disabled'
        assert screen.controller.folder_path == "TEST_666"
        screen.lbl_directory.config.assert_called_with(text="TEST_666")

    @mock.patch('classes.forms.IdenThread')
    @mock.patch('classes.forms.MainScreen.__init__')
    def test_click_btn_identify(self, ms_ini, thread):
        """ Ensures correct actions are taken upon selecting to identify participants. """
        ms_ini.return_value = None
        screen = MainScreen()

        fake_thread = mock.Mock()
        screen.controller = mock.Mock()
        screen.controller._only_identify = mock.Mock()
        thread.return_value = fake_thread

        screen._btn_identify()

        assert fake_thread.start.call_count == 1

    @mock.patch('classes.forms.AnonThread')
    @mock.patch('classes.forms.MainScreen.__init__')
    def test_click_btn_anonymize(self, ms_ini, thread):
        """ Ensures correct actions are taken upon selecting to anonymize data set. """
        ms_ini.return_value = None
        screen = MainScreen()
        screen.lbl_anon = mock.Mock()

        # Invalid study name
        study_name = ""
        screen.txt_study_name = mock.Mock()

        screen.txt_study_name.get = mock.Mock(return_value=study_name)
        screen._btn_anonymize()
        screen.lbl_anon.config.assert_called_with(text="Please enter a study name..")

        study_name = "./This is not alpha numeric ././.8%$£"
        screen.txt_study_name.get = mock.Mock(return_value=study_name)
        screen._btn_anonymize()
        screen.lbl_anon.config.assert_called_with(text="Please enter a valid study name..")

        # Correct study name
        study_name = "test"
        screen.controller = mock.Mock()
        screen.controller._only_anonymize = mock.Mock()
        screen.txt_study_name.get = mock.Mock(return_value=study_name)
        fake_thread = mock.Mock()
        thread.return_value = fake_thread

        screen._btn_anonymize()

        assert thread.return_value.start.call_count == 1
