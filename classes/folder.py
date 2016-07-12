""" File contains any classes used by the service. """
try:
    import os
except Exception as e:
    print("\033[91mError importing 'os' library.. Exiting.")
    exit()


class Folder(object):
    """ A folder object represents a folder potentially containing xml files. """

    def __init__(self, abs_path):
        """ Initializes a Folder object with the given absolute path and empty contents. """
        contents = abs_path.split('/') # Get a pretty name for the folder.
        self.name = contents[len(contents) - 1] # This folder's name.
        self.xml_files = [] # Names of any xml files within this folder.
        self.folders = []   # Folders inside this folder.
        self.absolute_path = abs_path   # Path of this folder.

        #Extract 

    def _extract_self(self):
        """ Extracts this folder's contents. """
        print("\033[94m=== Identifying contents for folder: " + self.name + " \033[0m")
        
        # Identify XML files.
        print("\033[93m=== Identifying XML files: \033[0m")
        self.xml_files = []
        for file in next(os.walk(self.absolute_path))[2]:
            if file.endswith(".xml"):
                print("=== Found: " + file)
                self.xml_files.append(file)
        print("\033[93m=== Identified {} xml file(s).\033[0m".format(len(self.xml_files)))

        # Identify folders.
        print("\033[93m=== Identifying folders: \033[0m")
        self.xml_files = []
        for folder in next(os.walk(self.absolute_path))[1]:
            print("=== Found: " + folder)
            self.folders.append(Folder(self.absolute_path + "{}/".format(folder)))
        print("\033[93m=== Identified {} folder(s).\033[0m".format(len(self.folders)))
