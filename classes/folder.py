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
        contents = abs_path.split('\\')  # Get a pretty name for the folder.
        self.name = contents[len(contents) - 1]  # This folder's name.
        self.xml_files = []  # Names of any xml files within this folder.
        self.tif_files = []  # Names of any tif files within this folder.
        self.absolute_path = abs_path   # Path of this folder.

    def _extract_self(self):
        """ Extracts this folder's contents. """
        printer.print_blue("=== Identifying contents for folder: " + self.name)
        self.__identify_files()
        printer.print_blue("=== Completed identification for folder: " + self.name)

    def _anonymize_folder(self):
        """ Anonymizes the name of this folder and invokes its children to do so. """
        printer.print_blue("=== Anonymizing folder: " + self.name)

        try:
            # iff this isn't the data folder
            if self.name.endswith("Data"):
                printer.print_blue("=== Anonymization not needed as this is the data folder!")
            else:
                # Get the original path excluding the original file name.
                old_path = self.absolute_path[:-len(self.name)]
                new_path = old_path + str(random.randrange(1000000, 9999999))
                os.rename(self.absolute_path, new_path)  # Do the rename
                self.absolute_path = new_path
        except OSError:
            printer.print_red("ERROR: Could not rename directory - " + self.name)

        printer.print_blue("=== Completed anonymization of folder: " + self.name)

    def _anonymize_file_names(self):
        """
        Anonymizes the name of any XML and TIFF files within this folder
        and invokes its children to do the same. """
        printer.print_blue("=== Anonymizing file names in folder: " + self.name)
        new_xmls = []
        new_tifs = []
        current_int = random.randrange(1000000, 9999999)
        # Anonymize the xml files
        for file_name in self.xml_files:
            try:
                # Get the original path excluding the original file name.
                new_name = str(current_int)
                old_path = self.absolute_path + "\\{}".format(file_name)
                new_path = self.absolute_path + "\\{}.xml".format(new_name)
                os.rename(old_path, new_path)  # Do the rename
                new_xmls.append(new_name)
                current_int = current_int + 1
            except OSError:
                printer.print_red("ERROR: Could not rename file - " + old_path)

        # Anonymize the tif files
        for file_name in self.tif_files:
                    try:
                        # Get the original path excluding the original file name.
                        new_name = str(current_int)
                        old_path = self.absolute_path + "\\{}".format(file_name)
                        new_path = self.absolute_path + "\\{}.tif".format(new_name)
                        os.rename(old_path, new_path)  # Do the rename
                        new_tifs.append(new_name)
                        current_int = current_int + 1
                    except OSError:
                        printer.print_red("ERROR: Could not rename file - " + old_path)

        self.xml_files = new_xmls
        self.tif_files = new_tifs

        printer.print_blue("=== Completed anonymization for file names within folder: " + self.name)

    def _anonymize_file_contents(self):
        """ Cycles through and anonymizes file contents. """
        printer.print_blue("=== Anonymizing file contents in folder: " + self.name)
        for file in self.xml_files:
            self._anonymize_file(file)
        printer.print_blue("=== Completed anonymization for file contents within folder: " + self.name)

    def _anonymize_file(self, file_name):
        """ Anonymizes the file name. """
        try:
            doc = parse(self.absolute_path + "\\{}.xml".format(file_name))
            root_node = doc.getroot()
            patient_node = root_node.find("PATIENT")
            patient_node.find("LAST_NAME").text = "N/A"
            patient_node.find("GIVEN_NAME").text = "N/A"
            patient_node.find("MIDDLE_NAME").text = "N/A"
            patient_node.find("NAME_PREFIX").text = "N/A"
            patient_node.find("NAME_SUFFIX").text = "N/A"
            patient_node.find("FULL_NAME").text = "N/A"
            patient_node.find("PATIENT_ID").text = "N/A"
            patient_node.find("BIRTH_DATE").text = patient_node.find("BIRTH_DATE").text[:-6] + "-01-01"

            doc.write(self.absolute_path + "\\{}.xml".format(file_name))
        except Exception as e:
            printer.print_red("ERROR: Could not modify file - " + file_name)
            print(e)

    def __identify_files(self):
        """ Identifies any xml files to be used. """
        printer.print_yellow("=== Identifying XML files.")
        self.xml_files = []
        try:
            for file in next(os.walk(self.absolute_path))[2]:
                if file.endswith(".xml"):
                    self.xml_files.append(file)
                elif file.endswith(".tif"):
                    self.tif_files.append(file)
            printer.print_yellow("=== Identified {} xml file(s) and {} tif file(s).".format(len(self.xml_files), len(self.tif_files)))
        except StopIteration:
            printer.print_yellow("=== No XML files identified.")
