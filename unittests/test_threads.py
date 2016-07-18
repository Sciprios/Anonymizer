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
    from classes.threads import AnonThread, IdenThread

except Exception:
    print("Could not import all modules, exitting.")
    exit()


class TestAnonThread(TestCase):
    """ Class to test the AnonThread class. """

    def setUp(self):
        """ Sets instance variables. """
        pass

    def test_run(self):
        """ Tests the run method of the thread. """
        thread = AnonThread(gui=mock.Mock())
        thread.gui.lbl_anon = mock.Mock()
        thread.gui.controller = mock.Mock()
        thread.gui.btn_folder = {}
        thread.gui.btn_identify = {}
        thread.gui.btn_anonymize = {}

        thread.run()

        assert thread.gui.controller._only_anonymize.call_count == 1
        thread.gui.lbl_anon.config.assert_called_with(text="Anonymization complete.")
        assert thread.gui.btn_anonymize['state'] == 'disabled'
        assert thread.gui.btn_identify['state'] == 'disabled'
        assert thread.gui.btn_folder['state'] == 'normal'
