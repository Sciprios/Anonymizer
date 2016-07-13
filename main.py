""" Module to be executed to anonymize all XML files within the 'Data' folder. """
try:
    from classes.folder import Folder
    from classes.colours import ColourPrint
    from classes.processor import Anonymizer
    printer = ColourPrint()
except Exception:
    print("Ensure you have the classes folder.")
    exit()

try:
    import os
except Exception:
    printer.print_red("Error loading core modules.. Exiting..")
    exit()

if __name__ == '__main__':  # If this module is being executed.
    anonimizer = Anonymizer("TestStudy",os.getcwd() + "\Data")
    anonimizer.anonymize_data()