import random
import os

class SystemLocation(object):
    """ Defines a location object which is in the data set. """

    def __init__(self, path):
        """ Initializes the path. """
        self._path = path
        self.files = []
    
    def anonymize(self):
        """ Locations must be anonymizeable. """
        raise NotImplementedError()


class Folder(object):
    """ Defines a folder contianing participant data. """

    def __init__(self, path):
        """ Initializes the files list and path. """
        SystemLocation.__init__(self, path)
        self.files = []

    def anonymize(self, study, folder_count):
        """ Anonymzises all files within this folder. """
        new_name =  "/{}_{}".format(study, folder_count)
        
        # Anonymize files first
        count = 0
        for file in self.files:
            file.anonymize(new_name, count)
        
        # Rename folder
        try:
            current_name = self.path.split('/')
            new_path = self.path[:-len(current_name)] + new_name
            os.rename(self.path, new_path)
        except OSError as e:
            print(e)


class File(SystemLocation):

    def __init__(self, path):
        """ Initializes parent class. """
        SystemLocation.__init__(self, path)

    def anonymize(self, folder_name, file_num):
        """ Anonymizes this file and its contents. """
        if self.path[:-4] == ".xml":
            new_name = "{}_{}.{}".format(folder_name, count, file[:-4])
            current_name = self.path.split('/')
            new_path = self.path[:-len(current_name)] + new_name
            
            # Hide patient info
            try:
                doc = parse(self.path)
                root_node = doc.getroot()
                patient_node = root_node.find("PATIENT")
                patient_node.find("LAST_NAME").text = study
                patient_node.find("GIVEN_NAME").text = ""
                patient_node.find("MIDDLE_NAME").text = ""
                patient_node.find("NAME_PREFIX").text = ""
                patient_node.find("NAME_SUFFIX").text = ""
                patient_node.find("FULL_NAME").text = new_name
                patient_node.find("PATIENT_ID").text = ""
                patient_node.find("BIRTH_DATE").text = patient_node.find("BIRTH_DATE").text[:-6] + "-01-01"

                doc.write(self.path)
            except Exception as e:
                print(e)
        # Rename file
        try:
            os.rename(self.path, new_path)
            self.path = new_path
        except OSError as e:
            print(e)