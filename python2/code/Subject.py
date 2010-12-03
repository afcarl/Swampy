from RemoteObject import *
from copy import copy

class Subject(RemoteObject):
    """A Subject is an object that keeps track of the Observers
    watching it.  When the state of a subject changes, it
    notifies each Observer on the list."""

    def __init__(self, name):
        RemoteObject.__init__(self, name)
        self.observers = []

    def notify_observers(self):
        """notify all registered observers when the state of
        the subject changes"""
        
        for observer in copy(self.observers):
            try:
                print 'Notifying', observer
                ns = NameServer()
                proxy = ns.get_proxy(observer)
                proxy.notify()
            except Exception, x:
                # this clause should catch errors that occur
                # in the Observer code.
                print ''.join(Pyro.util.getPyroTraceback(x))
            except:
                # this clause should catch Pyro NamingErrors,
                # which occur when an observer dies.
                print 'Removing ' + observer
                self.observers.remove(observer)

    # the following methods are intended to be invoked remotely

    def register(self, name):
        """register a new Observer (invoked by the Observer)"""
        self.observers.append(name)
        print 'Registered ' + name

class SimpleSubject(Subject):

    def __init__(self, name, state=0):
        """The state of a SimpleSubject is a single integer named 'state'
        In a real application, the state would be a more elaborate
        data structure."""
        Subject.__init__(self, name)
        self.state = 0

    # the following methods are intended to be invoked remotely
        
    def set_state(self, state):
        """change the state of the Subject"""
        print 'New state', state
        self.state = state
        self.notify_observers()

    def get_state(self):
        """get the current state of the Subject"""
        return self.state

sub = SimpleSubject('bob')
sub.requestLoop()
    
