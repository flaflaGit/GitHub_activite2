# -*-coding:Latin-1 -*

""" Fonctions et variables utiles pour la partie serveur
"""

import socket
import select
import os
import configparser
from sys import exit
from threading import Thread
from carte import Carte
from monTimer import *

onAttendJoueur = True

class EcouteClient(Thread):
    """Thread charg� simplement d'�couter le joueur connecter pour savoir s'il a demand� de commencer le jeu
        Avec gestion concurrence d'acc�s aux ressources (Rlock)
        Si c'est le cas, on arrete d'�couter le joueur, on pass dans la phase "jouer"
    """

    def __init__(self, cnx, id):
        Thread.__init__(self)
        self.cnx = cnx
        self.num=id
        self.aStopper=False

    def run(self):
        """Code � ex�cuter pendant l'ex�cution du thread."""
        verrou = RLock()
        self.cnx.settimeout (1)  #On sort du recv toutes les 1 secondes
        while not self.aStopper :
            try:
                msg = self.cnx.recv(1024).decode("Utf8")
            except socket.timeout:
                #print("Pour thread {} : socket timeout".format(self.num))
                pass
            except socket.error:
                print("Pour thread {} : socket error".format(self.num))
                break
            except BlockingIOError:
                print("Pour thread {} : BlockingIOError".format(self.num))
                break
            else :
                if not msg :  #ou faire test len(msg) <= 0
                    break
                else:   #si le client envoie la chaine : "c" ou "C" ==> on positionne la valeur et on stoppe le thread
                    with verrou:
                        if msg.upper() == "C":
                            idjoueur=self.num
                            self.aStopper = True
                            global onAttendJoueur
                            onAttendJoueur = False
                            print("Le joueur {} a demande que la partie commence\n".format(self.num))
                            break
                        else : 
                            print(msg)
        self.cnx.settimeout (0)  #On retire le timeout
        
    def kill(self):
        self.aStopper=True
        #print("On stoppe le thread du joueur n� {}".format(self.num))

def envoyerMsgAll(listeJ, msg,joueurSupp, saufJoueur=0):
    """ Envoi d'un message � tous les joueurs sauf si un num�ro de joueur est indiqu� dans la variable optionnelle """
    for cle,joueur in listeJ.items():
        if cle == saufJoueur : #on n'envoie pas de message
            continue
        try:                #On envoie le msg
            joueur.send(msg.encode("utf-8"))
        except ConnectionAbortedError:
            #si on trappe cette erreur, c'est que le client a quitt� le jeu sans nous le dire
            print("Le joueur n� {} a quit� le jeu !!".format(cle))
            joueurSupp.append(cle)
            pass
        except ConnectionResetError:
            #si on trappe cette erreur, c'est que le client a quitt� le jeu sans nous le dire
            print("Le joueur n� {} a quit� le jeu !!".format(cle))
            joueurSupp.append(cle)
            pass
        except BlockingIOError as e:
            #si on trappe cette erreur, je ne sais pas ce que c'est
            print("Erreur BlockingIOError quand comm avec Le joueur n� {} . Erreur = {}".format(cle, e))
            pass

def envoyerMsg(cle, joueur, msg,joueurSupp):
    """ Envoi d'un message � 1 seul joueur
        Cettefonction retourne True si pas d'erreur pendant l'envoi, sinon False
    """
    try:                #On envoie le msg
        joueur.send(msg.encode("utf-8"))
    except ConnectionAbortedError:
        #si on trappe cette erreur, c'est que le client a quitt� le jeu sans nous le dire
        print("Le joueur n� {} a quit� le jeu !!".format(cle))
        joueurSupp.append(cle)
        return False
    except ConnectionResetError:
        #si on trappe cette erreur, c'est que le client a quitt� le jeu sans nous le dire
        print("Le joueur n� {} a quit� le jeu !!".format(cle))
        joueurSupp.append(cle)
        return False
    except BlockingIOError as e:
        #si on trappe cette erreur, je ne sais pas ce que c'est
        print("Erreur BlockingIOError quand comm avec Le joueur n� {} . Erreur = {}".format(cle, e))
        return False
    else :
        return True

def envoyerLabyrinthe(listeJ, lab):
    """ Envoi du labyrinthe � tous les joueurs
        Comme le robot n'est pas represent� de le m�me fa�on en fonction des joueurs, *
        la chaine est l�g�rement modifi� avant envoi
        la gestion des joueurs supprim�s est effectu� ailleurs, donc on ne tient pas compte de la variable supp
    """
    supp=[]
    for cle,joueur in listeJ.items():
        msg="\n"+lab.donnerGrilleJoueur(cle)
        envoyerMsg(cle, joueur, msg,supp)


def ecouterJoueur(cle,joueur,attente):
    """ Cette fonction est utilis�e pour r�cup�rer les commandes des joueurs
        A noter que si au bout d'un certain temps le joueur n'a pas r�pondu, on arrete d'attendre
    """
    aStopper=False
    msg=""
    joueur.settimeout (attente)  #On sort du recv apres x secondes (x = attente pass� en param)
    while not aStopper :
        try:
            msg = joueur.recv(1024).decode("Utf8")
        except socket.timeout:
            print("Pour thread {} : socket timeout".format(cle))
            #le jour n'a pas r�pondu dans les d�lais
            aStopper=True
            break
        except socket.error:
            print("Pour thread {} : socket error".format(cle))
            break
        except BlockingIOError:
            print("Pour thread {} : BlockingIOError".format(cle))
            break
        else :
            if not msg :  #donc, le joueur n'a rien envoy� ==> on repasse dans la boucle
                continue
            else:   #on r�cup�re la commande du joueur
                print("Le joueur {} joue : {}".format(cle, msg))
                aStopper=True
                
    joueur.settimeout (0)  #On retire le timeout
    return msg

    
