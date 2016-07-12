""" File contains any classes used by the service. """
try:
    import os
except Exception as e:
    print("\033[91mError importing 'os' library.. Exiting.")
    exit()

class Location(object):
    """ An item with a directory location. """
    def __init__(self, abs_path):
        """ Intiializes a Location object with the given absolute path. """
        self.absolute_path = abs_path

class Folder(Location):
    """ A folder object represents a folder potentially containing xml files. """

    def __init__(self, abs_path):
        """ Initializes a Folder object with the given absolute path and empty contents. """
        Location.__init__(self, abs_path)

        contents = abs_path.split('/') # Get a pretty name for the folder.
        self.name = contents[len(contents) - 1]
        self.xml_files = []
        self.folders = []

    def _extract_self(self):
        """ Extracts this folder's contents. """
        print("\033[94m=== Extracting contents for folder: " + self.name + " ===\033[0m")
        print("\033[93m=== Identifying XML files: \033[0m")
        files_identified = []
        count = 0
        for file in next(os.walk(self.absolute_path))[2]:
            if file.endswith(".xml"):
                print("=== Found: " + file)
                files_identified.append(file)
                count = count + 1
        print("\033[93m=== Identified {} xml files.\033[0m".format(count))
