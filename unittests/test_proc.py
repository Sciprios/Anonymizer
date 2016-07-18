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

except Exception:
    print("Could not import all modules, exitting.")
    exit()


class TestAnonymizer(TestCase):
    """ Class to test the Anonymizer class. """

    def setUp(self):
        """ Sets instance variables. """
        self.study_name = "TEST_STUDY"

    @mock.patch('classes.processor.printer')
    def test_anonymize_data(self, print_mck):
        """ Tests the anonymize_data method. """
        anon = Anonymizer(self.study_name)

        anon._identify_patient_folders = mock.Mock()
        anon._identify_files = mock.Mock()
        anon._patch_folder_names = mock.Mock()
        anon._patch_file_names = mock.Mock()
        anon._patch_file_content = mock.Mock()
        anon._output_hash = mock.Mock()

        anon.anonymize_data()

        assert anon._identify_patient_folders.call_count == 1
        assert anon._identify_files.call_count == 1
        assert anon._patch_folder_names.call_count == 1
        assert anon._patch_file_names.call_count == 1
        assert anon._patch_file_content.call_count == 1
        assert anon._output_hash.call_count == 1

    def test_only_anonymize(self):
        """ Tests the only_anonymize method. """
        anon = Anonymizer(self.study_name)

        anon._patch_folder_names = mock.Mock()
        anon._patch_file_names = mock.Mock()
        anon._patch_file_content = mock.Mock()

        anon._only_anonymize()

        assert anon._patch_folder_names.call_count == 1
        assert anon._patch_file_names.call_count == 1
        assert anon._patch_file_content.call_count == 1

    def test_only_identify(self):
        """ Tests the only_identify method. """
        anon = Anonymizer(self.study_name)

        anon._identify_patient_folders = mock.Mock()
        anon._identify_files = mock.Mock()

        anon._only_identify()

        assert anon._identify_patient_folders.call_count == 1
        assert anon._identify_files.call_count == 1

    def test_identify_patient_folders(self):
        """ Tests the identify_patient_folders method. """
        pass

    def test_identify_files(self):
        """ Tests the identify_files method. """
        anon = Anonymizer(self.study_name)

        fld_one = mock.Mock()
        fld_two = mock.Mock()
        fld_three = mock.Mock()
        anon.participant_folders = [fld_one, fld_two, fld_three]

        anon._identify_files()

        assert fld_one._extract_self.call_count == 1
        assert fld_two._extract_self.call_count == 1
        assert fld_three._extract_self.call_count == 1

    @mock.patch('classes.processor.random')
    def test_patch_folder_names(self, rnd_mck):
        """ Tests the patch_folder_names method. """
        anon = Anonymizer(self.study_name)

        rnd_mck.randint = mock.Mock(return_value=666)
        fld_one = mock.Mock()
        fld_two = mock.Mock()
        fld_three = mock.Mock()
        anon.participant_folders = [fld_one, fld_two, fld_three]

        anon._patch_folder_names()

        assert len(anon.participant_hash) == 3
        assert fld_one.anonymize_folder.call_count == 1
        assert fld_two.anonymize_folder.call_count == 1
        assert fld_three.anonymize_folder.call_count == 1

    @mock.patch('classes.processor.random')
    def test_patch_file_names(self, rnd_mck):
        """ Tests the patch_file_names method. """
        anon = Anonymizer(self.study_name)

        rnd_mck.randint = mock.Mock(return_value=666)
        fld_one = mock.Mock()
        fld_two = mock.Mock()
        fld_three = mock.Mock()
        anon.participant_folders = [fld_one, fld_two, fld_three]

        anon._patch_file_names()

        fld_one._anonymize_file_names.assert_called_with(666)
        fld_two._anonymize_file_names.assert_called_with(666)
        fld_three._anonymize_file_names.assert_called_with(666)

    def test_patch_file_content(self):
        """ Tests the patch_file_content method. """
        anon = Anonymizer(self.study_name)

        fld_one = mock.Mock()
        fld_two = mock.Mock()
        fld_three = mock.Mock()
        anon.participant_folders = [fld_one, fld_two, fld_three]

        anon._patch_file_content()

        assert fld_one._anonymize_file_contents.call_count == 1
        assert fld_two._anonymize_file_contents.call_count == 1
        assert fld_three._anonymize_file_contents.call_count == 1

    @mock.patch('classes.processor.printer')
    @mock.patch('classes.processor.os')
    def test_output_hash(self, os_mck, prnt_mck):
        """ Tests the output_hash method. """
        anon = Anonymizer(self.study_name)

        # os error
        os_mck.remove = mock.Mock(side_effect=OSError)
        anon._output_hash()
        assert prnt_mck.print_yellow.call_count == 2

