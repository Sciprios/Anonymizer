from views import MainForm
from threading import Thread

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
        self._gui = MainForm()
        self._id_thread = Thread(target=self.identify)
        self._anon_thread = Thread(target=self.anonymize)