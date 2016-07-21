from views import MainForm
from models import Folder
from threading import Thread
import os


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

    def __init__(self):
        """ Initializes the gui and the relevant threads. """
        Subject.__init__(self)
        self._gui = MainForm(self)
        self._id_thread = None
        self._anon_thread = None
        self.id_progress = 0
        self.anon_progress = 0
        self._folders = []
    
    def start(self):
        """ Starts the gui. """
        self._gui.main_loop()
    
    def anonymize(self, study, data_location):
        """ Starts a thread to anonymize the data. """
        self._anon_thread = Thread(target=self._anonymize, args=[study, data_location])
    
    def _anonymize(self, study, data_location):
        """ Anonymizes the folders and files. """
        num_participants = len(os.listdir(data_location))
        for folder in self._folders:
            folder.anonymize(study, len(self._folders))
            # Add to hash file
            with open("identifiers.csv", "a") as csv_file:
                writer = csv.writer(csv_file, delimiter=",")
                for participant in self.participant_hash:
                    writer.writerow([participant[0], participant[1]])
            self.anon_progress = (len(self._folders) / num_participants) * 100
            super(Subject, self).notify_observers()
        
    def identify(self, data_location):
        """ Launches a thread to identify folders and files. """
        self._id_thread = Thread(target=self._identify, args=[data_location])
        
    
    def _identify(self, data_location):
        """ Identifies files and folders within the data set. """
        num_participants = len(os.listdir(data_location))
        for dir_name in next(os.walk(data_location))[1]:
            new_folder = Folder(data_location + "/" + dir_name)
            self._folders.append(new_folder)

            # Extract files
            for file in next(os.walk(self.absolute_path))[2]:
                new_folder.add_file(data_location + "/" + dir_name + "/" + file) 

            # Update observers
            self.id_progress = (len(self._folders) / num_participants) * 100
            super(Subject, self).notify_observers()
    
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
        super(Subject, self).notify_observers()
