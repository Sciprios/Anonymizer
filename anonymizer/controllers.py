from models import Folder, File
from threading import Thread
import os
import csv


class Subject(object):
    """ Defines an object which can be listened to. """

    def __init__(self):
        """ Initializes an empty list of observers. """
        self._observers = []
    
    def subscribe(self, observer):
        """ Adds an observer to the subscription list. """
        if observer not in self._observers:
            self._observers.append(observer)
    
    def unsubscribe(self, observer):
        """ Removes the given observer from the subscription list. """
        if observer in self._observers:
            self._observers.remove(observer)

    def notify_observers(self):
        """ Notifies all observers in the subscription list. """
        for observer in self._observers:
            observer.notify()


class Observer(object):
    """ Defines an object which can be updated by Subjects. """
    def notify(self):
        """ A method to be overwritten to update this entity. """
        raise NotImplementedError()


class ControlAnonymizer(Subject):
    """ Defines a control object for the naonymization process. """

    def __init__(self, gui):
        """ Initializes the gui and the relevant threads. """
        Subject.__init__(self)
        self._gui = gui
        self._id_thread = None
        self._anon_thread = None
        self.id_progress = 0
        self.anon_progress = 0
        self._folders = []
    
    def start(self):
        """ Starts the gui. """
        self._gui.mainloop()
    
    def anonymize(self, study, data_location):
        """ Starts a thread to anonymize the data. """
        self._anon_thread = Thread(target=self._anonymize, args=[study, data_location])
        self._anon_thread.start()

    def _anonymize(self, study, data_location):
        """ Anonymizes the folders and files. """
        num_participants = len(os.listdir(data_location))
        count = 0
        for folder in self._folders:
            split_path = folder._path.split('/')
            cur_name = split_path[len(split_path) - 1]
            new_name = folder.anonymize(study, count)

            # Add to hash file
            with open("identifiers.csv", "a") as csv_file:
                writer = csv.writer(csv_file, delimiter=",")
                writer.writerow([cur_name, new_name])
            count = count + 1
            self.anon_progress = (count / num_participants) * 100
            self.notify_observers()
        
    def identify(self, data_location):
        """ Launches a thread to identify folders and files. """
        self._id_thread = Thread(target=self._identify, args=[data_location])
        self._id_thread.start()
    
    def _identify(self, data_location):
        """ Identifies files and folders within the data set. """
        try:
            num_participants = len(os.listdir(data_location))
            for dir_name in next(os.walk(data_location))[1]:
                fld_dir = data_location + "/" + dir_name
                new_folder = Folder(fld_dir)
                self._folders.append(new_folder)

                try:
                    # Extract files
                    for file in next(os.walk(fld_dir))[2]:
                        new_folder.add_file(File(fld_dir + "/" + file))
                except Exception as e:
                    print(e)
                
                # Update observers
                self.id_progress = (len(self._folders) / num_participants) * 100
                self.notify_observers()
        except OSError as e:
            print(e)
        
    
    def reset(self):
        """ Resets currently held data. """
        self._folders = []
        self._name_hash = []
        self.id_progress = 0
        self.anon_progress = 0
        try:
            os.remove("identifiers.csv")
        except OSError:
            print("Nothing to remove..")
        self.notify_observers()
