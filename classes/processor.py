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
    import random
    import csv
    from threading import Thread
except Exception:
    printer.print_red("Error loading core modules.. Exiting..")
    exit()

class Anonymizer(object):
    """ Anonymizer object anonymizes any patient folders in the Data folder. """

    def __init__(self, study_name):
        """ Initializes an anonymizer object for the given study. """
        self.study = study_name
        self.participant_folders = []
        self.participant_hash = []
    
    def anonymize_data(self):
        """ Anonymize the data in the Data folder. """
        printer.print_green("=== Anonymizing Data ===")
        self._identify_patient_folders()
        self._identify_files()
        self._patch_folder_names()
        self._patch_file_names()
        self._patch_file_content()
        self._output_hash()

    def _only_anonymize(self):
        """ Anonymizes the data held without identification. """
        self._patch_folder_names()
        self._patch_file_names()
        self._patch_file_content()
        # self._output_hash()
    
    def _only_identify(self):
        """ Identifies files and folders. """
        self._identify_patient_folders()
        self._identify_files()

    def _identify_patient_folders(self):
        """ Identifies patient folders within the Data folder. """
        self.participant_folders = []
        try:
            printer.print_blue("=== Identifying participant folders")
            for folder_name in next(os.walk(self.folder_path))[1]:
                self.participant_folders.append(Folder(self.folder_path + "/{}".format(folder_name)))
                printer.print_yellow("Found folder: " + folder_name)
        except StopIteration:
            printer.print_yellow("No participant folders found.")

    def _identify_files(self):
        """ Calls Folders to idnntify their files. """
        printer.print_blue("=== Identifying files within folders.")
        patient_total = len(next(os.walk(self.folder_path))[1])
        count = 0
        for folder in self.participant_folders:
            folder._extract_self()

    def _patch_folder_names(self):
        """ Calls for folders to change their names. """
        printer.print_blue("=== Anonymizing folder names")
        count = random.randint(1000000, 9999999)
        for folder in self.participant_folders:
            new_name = self.study + "_{}".format(count)
            self.participant_hash.append((folder.name, new_name))   # Store a hash of new and old identifiers.
            print(new_name)
            folder.anonymize_folder(new_name)
            count = count + 1

    def _patch_file_names(self):
        """ Calls for folders to rename any of their files. """
        printer.print_blue("=== Anonymizing file names")
        for folder in self.participant_folders:
            folder._anonymize_file_names(random.randint(1000000, 9999999))

    def _patch_file_content(self):
        """ Calls for folders to patch their XML file content """
        printer.print_blue("=== Anonymizing file content")
        for folder in self.participant_folders:
            folder._anonymize_file_contents()

    def _output_hash(self):
        """ Outputs the hash of identifiers. """
        printer.print_blue("=== Outputting hash of identifiers")
        try:
            os.remove("Data\identifiers.csv")
            printer.print_yellow("Overwriting identifiers file.")
        except OSError:
            printer.print_yellow("No identifiers file to be removed.")
            printer.print_yellow("Creating identifiers file.")
        finally:
            with open("Data\identifiers.csv", "a") as csv_file:
                writer = csv.writer(csv_file, delimiter=",")
                for participant in self.participant_hash:
                    writer.writerow([participant[0], participant[1]])