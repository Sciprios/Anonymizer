""" Module to be executed to anonymize all XML files within the 'Data' folder. """
try:
    from classes.folder import Folder
    from classes.colours import ColourPrint
    printer = ColourPrint()
except Exception:
    print("Ensure you have the classes.py file.")
    exit()

try:
    import os
except Exception:
    printer.print_red("Error loading core modules.. Exiting..")
    exit()

if __name__ == '__main__':  # If this module is being executed.
    printer.print_green("==========Anonymizer==========")
    printer.print_blue("=== Steps to be taken:")
    printer.print_blue("=== 1. Identify all data files.")
    printer.print_blue("=== 2. Anonymize folder names.")
    printer.print_blue("=== 3. Anonymize file names.")
    printer.print_blue("=== 4. Anonymize file data.")

    printer.print_green("===== Beginning Identification =====")
    folder = Folder(os.getcwd() + "\Data")
    folder._extract_self()
    printer.print_green("===== Finished Identification =====")

    printer.print_green("===== Beginning Folder Anonymization =====")
    folder._anonymize_folders()
    printer.print_green("===== Finished Folder Anonymization =====")

    printer.print_green("===== Beginning File Anonymization =====")
    folder._anonymize_files()
    printer.print_green("===== Finished File Anonymization =====")

    printer.print_green("===== Beginning Contents Anonymization =====")
    printer.print_red("=== NOT IMPLEMENTED YET")
    printer.print_green("===== Finished Contents Anonymization =====")