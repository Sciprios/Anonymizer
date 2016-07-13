""" File contains any classes used by the service. """
try:
    from classes.colours import ColourPrint
    printer = ColourPrint()
except Exception:
    print("\033[91mError importing 'colours' library.. Exiting.")
    exit()

try:
    import os
    import random
except Exception as e:
    printer.print_red("Error importing 'os' library.. Exiting.")
    exit()


class Folder(object):
    """ A folder object represents a folder containing xml files. """

    def __init__(self, abs_path):
        """
        Initializes a Folder object with the given
        absolute path and empty contents. """
        contents = abs_path.split('\\')  # Get a pretty name for the folder.
        self.name = contents[len(contents) - 1]  # This folder's name.
        self.xml_files = []  # Names of any xml files within this folder.
        self.folders = []   # Folders inside this folder.
        self.absolute_path = abs_path   # Path of this folder.

    def _extract_self(self):
        """ Extracts this folder's contents. """
        printer.print_blue("=== Identifying contents for folder: " + self.name)
        self.__identify_files()
        self.__identify_folders()
        printer.print_blue("=== Completed identification for folder: " + self.name)

    def __identify_files(self):
        """ Identifies any xml files to be used. """
        printer.print_yellow("=== Identifying XML files.")
        self.xml_files = []
        try:
            for file in next(os.walk(self.absolute_path))[2]:
                if file.endswith(".xml"):
                    self.xml_files.append(file)
            printer.print_yellow("=== Identified {} xml file(s).".format(len(self.xml_files)))
        except StopIteration:
            printer.print_yellow("=== No XML files identified.")

    def __identify_folders(self):
        """ Identifies any folders within this folder. """
        printer.print_yellow("=== Identifying folders.")
        self.xml_files = []
        try:
            for folder in next(os.walk(self.absolute_path))[1]:
                self.folders.append(Folder(self.absolute_path + "\\{}".format(folder)))
            printer.print_yellow("=== Identified {} folder(s).".format(len(self.folders)))

            # Extract inner folders.
            printer.print_yellow("=== Extracting {} folder(s):".format(len(self.folders)))
            for folder in self.folders:
                folder._extract_self()
        except StopIteration:
            printer.print_yellow("=== No folders identified.")
