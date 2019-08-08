# -*-coding:Utf-8 -*

"""

Fonctions et constants nécessaires au programme robots
Mis à part pour ne pas surcharger le code

"""

import os
import pickle

#from carte import Carte
#from labyrinthe import Labyrinthe

#Les entrées possibles pour le joueur :
coups=('Q', 'N', 'E', 'S', 'O', 'q', 'n', 'e', 's', 'o')

def recup_partie(fic):
    """Cette fonction récupère les données si le fichier existe.
    On renvoie un dictionnaire :  soit l'objet dépicklé si fichier existant, soit un dictionnaire vide.
    """
  
    if os.path.exists(fic): # Le fichier existe
        fichier_donnees = open(fic, "rb")
        mon_depickler = pickle.Unpickler(fichier_donnees)
        donnees = mon_depickler.load()
        fichier_donnees.close()
    else: # Le fichier n'existe pas
        donnees = {}
    return donnees

def sauverPartie(donnees,fic):
    """
        Cette fonction enregistre les données dans le fichier passé en paramètre
        Attention : Si la partie est terminée, on ne sauvegarde rien et on supprime le fichie
    """

    if donnees["labyrinthe"].trouverSortie():
        #on ne sauvegarde rien, et on supprime le fichier si existant
        if os.path.exists(fic):
            os.remove(fic)
    else:
        fichier_donnees = open(fic, "wb") # On écrase les anciennes données si existantes
        mon_pickler = pickle.Pickler(fichier_donnees)
        mon_pickler.dump(donnees)
        fichier_donnees.close()


def checkMouvt(saisieJoueur):
    """ Fonction qui vérifie si la saisie du joueur est OK
        ==> Cela permettra d'éviter de vérifier plus tard lors du calcul du déplacement
        1: on vérifie que 1er caractère est OK
        2: on vérifie que ensuite, si non vide, c'est un numérique
    """
    if len(saisieJoueur) == 0:
        return False
    if saisieJoueur[0] not in coups:
        return False
    if len(saisieJoueur) == 1:
        return True
    pas=1
    try:
        pas==int(saisieJoueur[1:])
    except ValueError:
        #le nombre de déplacement est incorrect
        print("Votre saisie est incorrect, la fin ({}) n'est pas numérique".format(saisieJoueur[1:]))
        return False
    return True

def calculerPas(saisieJoueur):
    if len(saisieJoueur) == 1:
        return 1
    pas=1
    try:
        pas=int(saisieJoueur[1:])
    except ValueError:
        #le nombre de déplacement est incorrect
        print("Votre saisie est incorrect, la fin ({}) n'est pas numérique".format(saisieJoueur[1:]))
        return 0
    return pas
    

