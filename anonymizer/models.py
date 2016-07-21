import random
import os
from xml.etree.ElementTree import parse, Element

class SystemLocation(object):
    """ Defines a location object which is in the data set. """

    def __init__(self, path):
        """ Initializes the path. """
        self._path = path
        self.files = []
    
    def anonymize(self):
        """ Locations must be anonymizeable. """
        raise NotImplementedError()


class Folder(SystemLocation):
    """ Defines a folder contianing participant data. """

    def __init__(self, path):
        """ Initializes the files list and path. """
        SystemLocation.__init__(self, path)
        self.files = []

    def anonymize(self, study, folder_count):
        """ Anonymzises all files within this folder. """
        new_name =  "{}_{}".format(study, folder_count)
        # Anonymize files first
        count = 0
        tif_count = 0
        xml_count = 0
        for file in self.files:
            count = count + 1
            if file._path.endswith(".tif"):
                tif_count = tif_count + 1
                file.anonymize(new_name, tif_count)
            elif file._path.endswith(".xml"):
                xml_count = xml_count + 1
                file.anonymize(new_name, xml_count)

        # Rename folder
        try:
            split_path = self._path.split('/')
            new_path = self._path[:-len(split_path[len(split_path) - 1])] + new_name
            os.rename(self._path, new_path)
            self._path = new_path
        except OSError as e:
            print(e)
        finally:
            return new_name
    
    def add_file(self, file):
        """ Adds the file to the folder's list. """
        self.files.append(file)


class File(SystemLocation):

    def __init__(self, path):
        """ Initializes parent class. """
        SystemLocation.__init__(self, path)
        print(path)

    def anonymize(self, folder_name, file_num):
        """ Anonymizes this file and its contents. """
        new_name = "{}_{}".format(folder_name, file_num)
        split_path = self._path.split('/')
        prev_path = self._path[:-len(split_path[len(split_path) - 1])]
        if self._path.endswith(".xml"):
            new_path = prev_path + new_name + ".xml"
            # Hide patient info
            try:
                doc = parse(self._path)
                root_node = doc.getroot()
                patient_node = root_node.find("PATIENT")
                patient_node.find("LAST_NAME").text = folder_name.split('_')[0]
                patient_node.find("GIVEN_NAME").text = ""
                patient_node.find("MIDDLE_NAME").text = ""
                patient_node.find("NAME_PREFIX").text = ""
                patient_node.find("NAME_SUFFIX").text = ""
                patient_node.find("FULL_NAME").text = new_name
                patient_node.find("PATIENT_ID").text = ""
                patient_node.find("BIRTH_DATE").text = patient_node.find("BIRTH_DATE").text[:-6] + "-01-01"

                doc.write(self._path)
            except Exception as e:
                print(e)
        elif self._path.endswith(".tif"):
            new_path = prev_path + new_name + ".tif"
        else:
            print(self._path)

        # Rename file
        try:
            os.rename(self._path, new_path)
            self._path = new_path
        except OSError as e:
            pass