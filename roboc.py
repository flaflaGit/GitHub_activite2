# -*-coding:Utf-8 -*

"""Ce fichier contient le code principal du jeu.

Exécutez-le avec Python pour lancer le jeu.

Améliorations possibles :
1. Sauvegarde du jeu en cours :
    a) possibilité de sauvegarder plusieurs jeu ==> aucun soucis pour mettre en place :
        - création d'un abjet contenant comme champs, les données sauvegardées actuellement
        - remplacer les données actuelles du dico par des instances de l'objet ci-dessus
    b) Comme pour l'exercice "pendu", on pourrait conserver les scores par utilisateur si on demandait nom de l'utilisateur
2. Gestion des erreurs : je ne l'ai pas effectué partout mais ce devrait être fait (pas trop le temps si je veux finit le cours avant la fin de la semaine)
3. Affichage graphique : si on voulait afficher plus jolimlent le labyrinthe, juste à remplacer la fonction d'affichage de la classe labyrinthe

"""

import os
from sys import exit

from carte import Carte
from labyrinthe import Labyrinthe
from fonctions import *

#Variables pour stocker la partie en cours
repCartes="cartes"
saveFic="sauvegardePartie.lab"  #nom du fichier où seront stockées les données
save=dict()                 #la variable contenant les données à sauvegarder


# On charge les cartes existantes
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

# Si il y a une partie sauvegardée, on l'affiche
#==> on fera plus tard car je ne sais pas encore comment je stockerai les données)
save=recup_partie(saveFic)
if bool(save):  #donc le fichier existait avec des données
    i+=1
    print("  {} - {} - dimension : {}. Il s'agit d'une partie en cours (nb de coups joués : {})".format(i+1, save["nom"], save["dimension"], save["nbCoups"]))

#1. On demande au joueur avec quel labyrinthe il veut jouer
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

#2. On affiche le labyrinthe et on enregistre la position du robot
#S'il s'agit de la partie sauvegardée, on continue le jeu avec les données qui étaient enregistrée
if bool(save) and choix==i+1 :
    jeu=save["labyrinthe"]
else:
    robot=cartes[choix-1].posRobot()
    jeu=Labyrinthe(robot,cartes[choix-1].labyrinthe)
    save["nom"]=cartes[choix-1].nom
    save["dimension"]=cartes[choix-1].dim()
    save["labyrinthe"]=jeu
    save["nbCoups"]=0
jeu.afficher()

#3. On boucle tant que le robot n'est pas sorti du labyrinthe
finJeu=False
#pour comptabiliser le nbr de coups (pourrait être utile si on voulait enregistrer des scores
nbCoups=save["nbCoups"]

while finJeu == False :
    saisieJoueur = input("Entrez le mouvement de votre robot : ")
    if checkMouvt(saisieJoueur) == False:    #saisie incorrecte
        continue
    if saisieJoueur[0].upper() == 'Q':
        break
#  Les deux lignes ci-dessous en commentaire : fonctionne si on ne veut pas faire du pas à pas 
#    if jeu.deplacer(saisieJoueur) == False:
#        print("Déplacement impossible ... Vérifiez s'il n'y a pas un mur entre votre position et la case finale")

#Pour le déplacement & affichage pas à pas :
    if jeu.estPossible(saisieJoueur) == False :
        print("Déplacement impossible ... Vérifiez s'il n'y a pas un mur entre votre position et la case finale")
    else :
        #On déplace le robot pas à pas  (mais on comptabilise qu'1 seul coup)
        nbCoups += 1
        pas=calculerPas(saisieJoueur)
        while pas > 0:
            jeu.deplacerUnPas(saisieJoueur[0])
            jeu.afficher()
            if jeu.trouverSortie():
                print("Bravo, vous avez réussi à sortir !!! (nb de coups : {})".format(nbCoups))
                finJeu=True
                break
            pas -= 1
        #maintenant on enregistre données et on sauvegarde la partie en cours
        save["labyrinthe"]=jeu
        save["nbCoups"]=nbCoups
        sauverPartie(save,saveFic)

#A la sortie de la boucle, on enregistre les données
if jeu.trouverSortie() == False:
    print("Vous n'avez pas encore trouvé la sortie (nb de coups : {})".format(nbCoups))
    print("Votre partie est sauvegardée, vous pourrez continuer plus tard ...")
sauverPartie(save,saveFic)

