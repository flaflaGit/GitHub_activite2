
from threading import Thread, RLock
import time


class Timer(Thread):

    """
        
    """

    def __init__(self, duree):
        Thread.__init__(self)
        self.duree = duree #la duree en seconde

    def run(self):
        """Code à exécuter pendant l'exécution du thread : on se contente de faire un sleep !!
        """
        time.sleep(self.duree)



