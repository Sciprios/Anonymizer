""" File contains any classes used by the service. """
try:
    import os
except Exception as e:
    print("\033[91mError importing 'os' library.. Exiting.")
    exit()


class Folder(Location):
    """ A folder object represents a folder potentially containing xml files. """

    def __init__(self, abs_path):
        """ Initializes a Folder object with the given absolute path and empty contents. """
        Location.__init__(self, abs_path)

        contents = abs_path.split('/') # Get a pretty name for the folder.
        self.name = contents[len(contents) - 1] # This folder's name.
        self.xml_files = [] # Names of any xml files within this folder.
        self.folders = []   # Folders inside this folder.
        self.absolute_path = abs_path   # Path of this folder.

    def _extract_self(self):
        """ Extracts this folder's contents. """
        print("\033[94m=== Extracting contents for folder: " + self.name + " ===\033[0m")
        print("\033[93m=== Identifying XML files: \033[0m")
        self.xml_files = []
        for file in next(os.walk(self.absolute_path))[2]:
            if file.endswith(".xml"):
                print("=== Found: " + file)
                self.xml_files.append(file)
        print("\033[93m=== Identified {} xml files.\033[0m".format(len(self.xml_files)))
