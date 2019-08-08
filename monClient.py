import socket
import random
from sys import exit
import configparser
from threading import Thread, RLock
import time

class EcouteServeur(Thread):
    """Thread chargé simplement d'écouter le serveur et d'afficher ce qu'il envoie
        Avec gestion concurrence d'accès aux ressources (Rlock)
        (pour ne pas mixer avec saisie utilisateur gérée dans pgm principal)
    """

    def __init__(self, cnx, fin, monTour):
        Thread.__init__(self)
        self.cnx = cnx
        self.amoi=False
        self.continuer=True
        self.msgFin=fin
        self.msgMonTour=monTour

    def run(self):
        """Code à exécuter pendant l'exécution du thread.
            On lit les envoi du serveur, et on les affiche sur la console.
            Dans le cas où le serveur envoi "votre tour", c'est que c'est à moi de joueur
        """
        verrou = RLock()
        while self.continuer :
            try:
                msg = self.cnx.recv(1024).decode("Utf8")
                if not msg :
                    break
                else:   #si le serveur envoie la chaine : "votre tour" ==> on positionne la valeur
                    #print("Message reçu : {}".format(msg))
                    if self.msgMonTour == msg:
                        self.amoi=True
                    elif self.msgFin == msg:  #on a recu du serveur l'ordre de fin
                        self.continuer=False
                    else:
                        #with verrou:
                        print(msg)
            except ConnectionResetError:
                print("Le serveur a fermé la connexion, on arrete donc le thread")
                self.continuer=False
                break
            except ConnectionAbortedError:
                print("Le serveur a fermé la connexion, on arrete donc le thread")
                self.continuer=False
                break
            except BlockingIOError:
                print("Exception : BlockingIOError")
                pass

    def monTour(self):
        return self.amoi
    
    def setMonTour(self, b):
        self.amoi=b

    def stop(self):
        """ Pour terminer proprement le Thread, on positionne la variable de la boucle principale à False """
        self.continuer=False
        exit(0)

#Lecture fichier de configuration :
config = configparser.ConfigParser()
config.read('labyrinthe.ini')

hote = config["CLIENT"]["hote"]
port = int(config["COMMUN"]["port"])
msgFin = config["COMMUN"]["MSGFIN"]
msgVotreTour = config["COMMUN"]["MSGAVOUS"]

connexion_avec_serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connexion_avec_serveur.connect((hote, port))
print("Connexion établie avec le serveur sur le port {}".format(port))

#On cree le thread qui sert à lire et afficher ce que le serveur envoie puis on le démarre
monThread = EcouteServeur(connexion_avec_serveur,msgFin, msgVotreTour)
monThread.start()

#time.sleep(20) #pour voir si affichage OK si pas dans boucle while avec send

msg_a_envoyer = b""
while msg_a_envoyer != b"q" and msg_a_envoyer != b"Q":
    if monThread.monTour() : # c'est donc a moi de jouer
        monThread.setMonTour(False)
        msg_a_envoyer = input("A vous > ")
        # Peut planter si on tape des caractères spéciaux  ==> à modifier plus tard (devrait fonctionner avec encode utf-8)
        msg_a_envoyer = msg_a_envoyer.encode()
        # On envoie le message
        connexion_avec_serveur.send(msg_a_envoyer)
    else:  #on fait une pause de 1s et on boucle de nouveau (on vérifie si serveur tjrs là)
        time.sleep(1)
        if not monThread.is_alive() :
            break

print("Le jeu est terminé, on ferme tout")
monThread.stop()
#monThread.join() ==> pas necessaire puisqu'on quitte le process (donc thread seront automatiquement termine)

connexion_avec_serveur.close()
