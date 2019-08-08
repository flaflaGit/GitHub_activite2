# -*-coding:Latin-1 -*

""" le serveur doit :
    1. Construire le labyrinthe en fonction de la carte qui sera choisie
    2. Une fois la carte construite, ouvrir un port d'écoute pour permettre aux joueurs de se connecter
    3. On limitera le nombre de joueurs pouvant se connecter
    4. Quand un client se connecte, on le positionne dans le labyrinthe
    5. A chaque modification du labyrinthe (nouveau joueur, déplacement, etc... ) il est renvoyé à tous les joueurs connectés
"""

import socket
import select
import os
import configparser
from sys import exit
from threading import Thread
from carte import Carte
from monTimer import *
from labyrinthe import Labyrinthe
from fonctionServeur import *

    
#Lecture fichier de configuration :
config = configparser.ConfigParser()
config.read('labyrinthe.ini')

port = int(config["COMMUN"]["port"])
msgFin = config["COMMUN"]["MSGFIN"]
msgVotreTour = config["COMMUN"]["MSGAVOUS"]

hote = config["SERVEUR"]["hote"]
repCartes=config["SERVEUR"]["repCartes"] #répertoire où sont stockées les cartes pour pouvoir joueur
joueurMax=int(config["SERVEUR"]["joueurMax"])   #On limite le nombre de joueurs pouvant joueur en même temps
attenteCnx=int(config["SERVEUR"]["attenteCnx"])   #le temps d'attente en secondes pour que les joueurs se connectent au serveur
attenteJoueur=int(config["SERVEUR"]["attenteJoueur"])   #le temps d'attente en secondes pour que le joueur donne sa réponse


#Chargement des cartes + demander laquelle utiliser
cartes = []
try:
    for nom_fichier in os.listdir(repCartes):
        if nom_fichier.endswith(".txt"):
            chemin = os.path.join(repCartes, nom_fichier)
            nom_carte = nom_fichier[:-3].lower()
            with open(chemin, "r") as fichier:
                contenu = fichier.read()
                # Création d'une carte, à compléter
                cartes.append(Carte(nom_carte,contenu))
                fichier.close()
except FileNotFoundError as e :
    print("Erreur de configuration : ")
    print(e)
    exit(1)
except:
    raise
    exit(1)

# On affiche les cartes existantes (ou on sort si aucune carte disponible)
if bool(cartes) == False:
    #aucune carte présente dans le répertoire ==> on stoppe tout
    print("Aucune carte disponible dans le répertoire '{}'".format(repCartes))
    exit(1)

print("Labyrinthes existants :")
for i, carte in enumerate(cartes):
    print("  {} - {} - dimension : {}".format(i + 1, carte.nom, carte.dim()))

#1. On demande avec quel labyrinthe on veut jouer
#==> on pourrait faire une boucle tant que y'a une erreur
try:
    choix=int(input("Entrez un numéro de labyrinthe pour commencer à jouer : "))
except ValueError:
    #La valeur n'est sans doute pas numérique
    print("Votre saisie est incorrecte ...  Fin du programme")
    exit(1)

if choix <1 or choix > i+1:
    print("Labyrinthe inexistant (pas dans la liste proposée) !!!")
    exit(1)

jeu=Labyrinthe(cartes[choix-1].labyrinthe)
#Quand on arrive ici, c'est que le serveur est prêt
#Il ne reste donc plus qu'à ouvrir connexion pour se mettre à l'écoute des connexions des joueurs


cnx = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cnx.bind((hote, port))
cnx.listen(5)  

print("On attend que les clients se connectent sur le port {}".format(port))

serveur_lance = True
#onAttendJoueur = True ==> cette variable est déclaré dans le fichier fonctionServeur
clients_connectes = []
listeJoueurs=dict()
mesThread=dict()  #utilisé pour stocker les threads en écoute de chacun des joueurs qui viennent de se connecter
nbClient=0  #cette variable contiendra le nombre de clients connectés

#On effectue une première boucle pour attendre les joueurs
#Mais pour ne pas attendre indéfiniment, dés qu'un joueur s'est connecté, on attend maximum 5mn (parametrable)
#avant de commencer le jeu
threadTimer=Timer(attenteCnx)  #On crée le thread q'on va utiliser plus tard avec attenteCnx secondes (le tmps pour que les joueurs se connectent)
threadStarted=False
while serveur_lance and onAttendJoueur :
    # On va vérifier que de nouveaux clients ne demandent pas à se connecter
    # Pour cela, on écoute la connexion_principale en lecture
    # On attend maximum 50ms
    # On ne boucle que pendant un certain temps
    if threadStarted == False :
        threadStarted=True
        threadTimer.start()
    else:
        if threadTimer.is_alive() == False :  #Donc le temps est dépassé
            print("Temps d'attente terminée ...  Nombre de joueurs = {}".format(nbClient))
            onAttendJoueur = False
            continue
            
    connexions_demandees, wlist, xlist = select.select([cnx], [], [], 0.05)
    
    for connexion in connexions_demandees:
        nbClient +=1
        connexion_avec_client, infos_connexion = connexion.accept()
        print("Un nouveau joueur vient de se connecter, c'est le n°{}".format(nbClient))
        print("Infos cnx client : {}".format(infos_connexion))
        if nbClient > joueurMax:  #on a accepté le nombre max de joueurs possibles
            #On lui envoie un message pour lui dire que KO (nbr de joueurs max atteint)
            connexion_avec_client.send(b"Trop de joueurs, essayer une prochaine fois !!!")
            connexion.close()
            onAttendJoueur=False
            break
        else:
            #On lui envoi un message pour lui dire que OK + On envoie le labyrinthe à tous ceux qui sont connectés
            msg="Bienvenu dans le jeu. Vous êtes le joueur n° "+str(nbClient)
            msg += "\nVotre robot est identifiable par 'V', ceux des autres joueurs par 'r'"
            connexion_avec_client.send(msg.encode("Utf8"))
            # On ajoute le socket connecté à la liste des clients
            # Et on crée le thread qui ecoute ce que dit ce joueur
            mesThread[nbClient] = EcouteClient(connexion_avec_client,nbClient)
            mesThread[nbClient].start()
            clients_connectes.append(connexion_avec_client)
            listeJoueurs[nbClient]=connexion_avec_client
            #Puis on positionne aléatoirement son robot dans le labyrinthe et on envoie le labyrinthe à tous les joueurs
            jeu.ajouterRobot(nbClient)
            envoyerLabyrinthe(listeJoueurs, jeu)
            
    #Il est possible qu'on arrive ici avec suffisemment de joueurs connectés ==> on sort de la boucle
    if nbClient >= joueurMax:
        onAttendJoueur = False

if nbClient == 0 :
    print("Aucun joueur ne s'est connecté, on stoppe le serveur")
    exit(1)
else :
    print("Le jeu peut commencer, nombre de joueurs connectés {}".format(len(clients_connectes)))

#Avant de commencer, on kill les thread qui seraient encore en ecoute  :
for j,t in mesThread.items():
    if t.is_alive():
        #print("Pour le joueur n° {}, le thread est encore actif ==> on le stoppe".format(j))
        t.kill()
    #else:
    #    print("Pour le joueur n° {}, le thread n'est plus actif".format(j))
    t.join()

#               **** Le jeu peut enfin commencer  *****

#On maintient à jour une liste des joueurs qui sont partis en cour de parties)
joueurSupp=[]
envoyerMsgAll (listeJoueurs,"Le jeu commence avec "+str(len(clients_connectes))+" joueurs ",joueurSupp)
msg=""    
#On affiche sur la console du serveur pour vérifier (les robots identifiables par numéro du joueur)
jeu.afficher()
while serveur_lance:
    #print("On boucle sur le jeu")
    # Maintenant, on écoute tour à tour (c'est les specs) la liste des clients connectés et on regarde s'ils ont quelque chose à dire
    for cle,joueur in listeJoueurs.items():
        if cle in joueurSupp:
            print("Le joueur {} a quitte la partie".format(cle))
            continue
        print("On écoute si client {} a qq chose à dire".format(cle))
        #On informe le joueur que c'est son tour de jour
        if not envoyerMsg(cle,joueur,msgVotreTour,joueurSupp): #y'a eu un pb lors de l'envoi du message, on passe au joueur suivant
            continue

        reponse=ecouterJoueur(cle,joueur,attenteJoueur)
        if reponse :
            #On vérifie si le joueur veut quitter le jeu (si c'est le cas, on le vire du jeu)
            if reponse.upper() == 'Q':
                msg="Le joueur "+str(cle)+" abandonne ..."
                print(msg)
                envoyerMsgAll (listeJoueurs,msg,joueurSupp, cle)
                #On met à jour le labyrinthe en retirant ce joueur
                jeu.retirerJoueur(cle)
                joueurSupp.append(cle)
                continue
            #On vérifie si réponse correcte
            if jeu.checkMouvt(cle, reponse) == False:  #donc mouvement incorrect
                envoyerMsg(cle,joueur,"Mouvement invalide, vous passez un tour !!!",joueurSupp)
                msg="Le mouvement du joueur "+ str(cle)+" est invalide (pas de modification du labyrinthe)"
                print(msg)
                envoyerMsgAll (listeJoueurs,msg,joueurSupp, cle)  #Ce message est envoyé à tous sauf ou joueur qui a joué
            else : #Donc OK ==> on deplace puis on renvoie le labyrinthe modifié à tous les joueurs
                res=jeu.deplacer(cle,reponse)
                msg="Le joueur "+str(cle)+" a joué : "+reponse
                envoyerMsgAll (listeJoueurs,msg,joueurSupp, cle)
                #On vérifie si le joueur a gagné :
                if jeu.trouverSortie():
                    serveur_lance=False
                    envoyerMsg(cle,joueur,"Bravo !!! vous avez gagné !!! ",joueurSupp)
                    msg="Le joueur "+str(cle)+" a trouvé la sortie, le jeu est terminé"
                    envoyerMsgAll (listeJoueurs,msg,joueurSupp,cle)
                    envoyerMsgAll (listeJoueurs,msgFin,joueurSupp)  #Ce message est envoyé pour que les clients ferment la connexion
                    break
                #On renvoie le labyrinthe à tout le monde
                envoyerLabyrinthe(listeJoueurs, jeu)
                #On l'affiche aussi sur la console du serveur pour vérifier
                jeu.afficher()
        else :
            envoyerMsg(cle,joueur,"Vous n'avez pas repondu dans les delais, vous etes enleve du jeu",joueurSupp)
            print("Le joueur {} ne repond pas, il a été supprimé du jeu".format(cle))
            #On met à jour le labyrinthe en retirant ce joueur
            jeu.retirerJoueur(cle)
            joueurSupp.append(cle)

    #Lorsqu'on arrive ici, on remet à jour la liste des joueurs encore connectés avant de relire les sockets (si plus de joueurs, on arrete le serveur)
    for j in joueurSupp:
        if j in listeJoueurs : 
            del(listeJoueurs[j])
            jeu.retirerJoueur(cle) 
    joueurSupp.clear()
    if len(listeJoueurs) <= 0:  #tous les joueurs sont partis avant la fin de la partie
        print("Il n'y a plus de joueur connecté, on stoppe tout")
        serveur_lance=False
        
print("Fermeture des connexions")
for client in clients_connectes:
    client.close()

cnx.close()
