""" Module containing the Anonymizer class. """
try:
    from classes.colours import ColourPrint
    from classes.folder import Folder
    printer = ColourPrint()
except Exception:
    print("ERROR: Missing parts of classes library, exiting.")
    exit()

try:
    import os
except Exception:
    printer.print_red("Error loading core modules.. Exiting..")
    exit()

class Anonymizer(object):
    """ Anonymizer object anonymizes any patient folders in the Data folder. """

    def __init__(self, study_name, data_folder_path):
        """ Initializes an anonymizer object for the given study. """
        self.study = study_name
        self.participant_folders = []
        self.folder_path = data_folder_path
    
    def anonymize_data(self):
        """ Anonymize the data in the Data folder. """
        printer.print_green("=== Anonymizing Data ===")
        self._identify_patient_folders()
        self._identify_files()

    def _identify_patient_folders(self):
        """ Identifies patient folders within the Data folder. """
        try:
            printer.print_blue("Identifying participant folders")
            for folder_name in next(os.walk(self.folder_path))[1]:
                self.participant_folders.append(Folder(self.folder_path + "\\{}".format(folder_name)))
        except StopIteration:
            printer.print_yellow("No participant folders found.")
        finally:
            printer.print_blue("Identified {} participant folder(s).".format(len(self.participant_folders)))

    def _identify_files(self):
        """ Calls Folders to identify their files. """
        printer.print_blue("Identifying files within folders.")
        for folder in self.participant_folders:
            folder._extract_self()
        printer.print_blue("Finished Identifying files.")
