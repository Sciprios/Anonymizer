""" File contains any classes used by the service. """
try:
    from classes.colours import ColourPrint
    printer = ColourPrint()
except Exception:
    print("\033[91mError importing 'colours' library.. Exiting.")
    exit()

try:
    import os
    from xml.etree.ElementTree import parse, Element
except Exception as e:
    printer.print_red("Error importing 'os' library.. Exiting.")
    exit()


class Folder(object):
    """ A folder object represents a folder containing xml files. """

    def __init__(self, abs_path):
        """
        Initializes a Folder object with the given
        absolute path and empty contents. """
        contents = abs_path.split('/')  # Get a pretty name for the folder.
        self.name = contents[len(contents) - 1]  # This folder's name.
        self.files = []  # Names of any xml files within this folder.
        self.absolute_path = abs_path   # Path of this folder.

    def _extract_self(self):
        """ Extracts this folder's contents. """
        printer.print_yellow("Identifying files in: " + self.name)
        self._identify_files()

    def anonymize_folder(self, identifier):
        """ Anonymizes the name of this folder and invokes its children to do so. """
        printer.print_yellow("Anonymizing folder: " + self.name)

        try:
            # Get the original path excluding the original file name.
            old_path = self.absolute_path[:-len(self.name)]
            new_path = old_path + identifier
            os.rename(self.absolute_path, new_path)  # Do the rename
            self.absolute_path = new_path
            self.name = identifier
        except OSError as e:
            printer.print_red("ERROR: Could not rename directory - " + self.name)
            print(e)

    def _anonymize_file_names(self, seed):
        """
        Anonymizes the name of any XML and TIFF files within this folder
        and invokes its children to do the same. """
        printer.print_yellow("Anonymizing contents for: " + self.name)
        new_xmls = []
        new_tifs = []
        count = seed

        for file_name in self.files:    # Assuming every xml has a tif.
            try:
                new_location = self.absolute_path + "/{}_{}".format(self.name, count)
                os.rename(self.absolute_path + "/{}.xml".format(file_name), new_location + ".xml")
                os.rename(self.absolute_path + "/{}.tif".format(file_name), new_location + ".tif")
                new_xmls.append(new_location + ".xml")
                new_tifs.append(new_location + ".tif")
                count = count + 1
            except OSError as e:
                print(e)
                printer.print_red("ERROR: Could not rename a file within {}: {}".format(self.name, file_name))

        self.xml_files = new_xmls
        self.tif_files = new_tifs

    def _anonymize_file_contents(self):
        """ Cycles through and anonymizes file contents. """
        printer.print_yellow("Anonymizing file contents in folder: " + self.name)
        for file in self.xml_files:
            self._anonymize_file(file)

    def _anonymize_file(self, file_path):
        """ Anonymizes the file name. """
        try:
            doc = parse(file_path)
            root_node = doc.getroot()
            patient_node = root_node.find("PATIENT")
            patient_node.find("LAST_NAME").text = ""
            patient_node.find("GIVEN_NAME").text = ""
            patient_node.find("MIDDLE_NAME").text = ""
            patient_node.find("NAME_PREFIX").text = ""
            patient_node.find("NAME_SUFFIX").text = ""
            patient_node.find("FULL_NAME").text = ""
            patient_node.find("PATIENT_ID").text = ""
            patient_node.find("BIRTH_DATE").text = patient_node.find("BIRTH_DATE").text[:-6] + "-01-01"

            doc.write(file_path)
        except Exception as e:
            printer.print_red("ERROR: Could not modify file - " + file_name)
            print(e)

    def _identify_files(self):
        """ Identifies any xml files to be used. """
        self.files = []
        try:
            for file in next(os.walk(self.absolute_path))[2]:
                if file.endswith(".xml"):
                    self.files.append(file[:-4])
            printer.print_yellow("Identified {} file(s).".format(len(self.files)))
        except StopIteration:
            printer.print_yellow("No XML files identified.")
