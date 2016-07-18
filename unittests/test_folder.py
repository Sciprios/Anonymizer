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
    from classes.folder import Folder

except Exception:
    print("Could not import all modules, exitting.")
    exit()


class TestFolder(TestCase):
    """ Class to test the Folder class. """

    def setUp(self):
        """ Sets instance variables. """
        self.path = "blah/TEST_PATH"

    @mock.patch('classes.folder.printer')
    def test_extract_self(self, prnt_mck):
        """ Tests the extract_self method. """
        fld = Folder(self.path)
        fld._identify_files = mock.Mock()

        fld._extract_self()

        prnt_mck.print_yellow.assert_called_with("Identifying files in: " + fld.name)
        assert fld._identify_files.call_count == 1

    @mock.patch('classes.folder.printer')
    @mock.patch('classes.folder.os')
    def test_anonymize_folder(self, os_mck, prnt_mck):
        """ Tests the anonymize_folder method. """
        fld = Folder(self.path)
        identifier = "666"
        old_path = self.path
        new_path = old_path[:-len(fld.name)] + identifier

        # No error
        os_mck.rename = mock.Mock()

        fld.anonymize_folder(identifier)

        os_mck.rename.assert_called_with(old_path, new_path)
        assert fld.absolute_path == new_path
        assert fld.name == "666"

        # OSError
        os_mck.rename = mock.Mock(side_effect=OSError)
        fld.anonymize_folder(identifier)
        prnt_mck.print_red.assert_called_with("ERROR: Could not rename directory - " + fld.name)

    @mock.patch('classes.folder.printer')
    @mock.patch('classes.folder.os')
    def test_anonymize_file_names(self, os_mck, prnt_mck):
        """ Tests the anonymize_file_names method. """
        fld = Folder(self.path)
        seed = 666
        fld.files = ["TEST_FILE_666"]

        # No error
        os_mck.rename = mock.Mock()
        fld._anonymize_file_names(seed)
        assert os_mck.rename.call_count == 2

        # Error
        os_mck.rename = mock.Mock(side_effect=OSError)
        fld._anonymize_file_names(seed)
        prnt_mck.print_red.call_count == 1

    def test_anonymize_file_contents(self):
        """ Tests the anonymize_file_contents method. """
        fld = Folder(self.path)
        fld.xml_files = ["TEST_XML"]
        fld._anonymize_file = mock.Mock()
        fld._anonymize_file_contents()
        fld._anonymize_file.assert_called_with(fld.xml_files[0])
