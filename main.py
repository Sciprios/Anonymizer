""" Module to be executed to anonymize all XML files within the 'Data' folder. """
try:
    from classes.folder import Folder
except Exception as e:
    print("Ensure you have the classes.py file.")

if __name__ == '__main__':  # If this module is being executed.
    print("\033[92m==========Anonymizer==========\033[0m")
    data_folder = Folder("C:\git\Anonymizer\Data")
    data_folder._extract_self()