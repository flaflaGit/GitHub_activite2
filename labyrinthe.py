# -*-coding:Utf-8 -*

"""Ce module contient la classe Labyrinthe.
    Ce module a été modifié pour satisfaire l'évolution en client serveur
"""
from collections import OrderedDict
import random

class Labyrinthe:

    """Classe représentant un labyrinthe."""
    coupsAutorises=('N', 'E', 'S', 'O', 'n', 'e', 's', 'o', 'M', 'm', 'P', 'p')
    directions=('N', 'E', 'S', 'O', 'n', 'e', 's', 'o')
    special=('m', 'M', 'P', 'p')
    mur="O"
    porte="."
    sortie="U"
    robotP="V"  #V signifie que c'est le robot du joueur
    robotA="r"  #r signifie qu'il s'agit d'un robot d'un autre joueur
    vide=" "

    def calculerCoordonnees(coord,direction, nbPas=1):
        """ Cette fonction retourne les nouvelles coordonnées en fonction d'une direction et d'un nombre de pas (optionnel)
        """
        if direction.upper() == "S":
            nouvCoord = (coord[0]+nbPas, coord[1])
        elif direction.upper() == "N":
            nouvCoord = (coord[0]-nbPas,coord[1])
        elif direction.upper() == "O":
            nouvCoord = (coord[0],coord[1]-nbPas)
        else:  #donc E
            nouvCoord = (coord[0],coord[1]+nbPas)
        return nouvCoord


    def __init__(self, laGrille):
        self.robot = dict() #Cette variable sera utilisé plus tard pour memoriser la position du robot des différents joueurs
        self.porte = dict() #Cette variable sera utilisée pour mémoriser si le robot d'un joueur est sur une porte on non
        self.grille = OrderedDict(sorted (laGrille.items(),key=lambda t: t[0]))
        self.abcisseMax=0
        self.ordonneeMax=0
        self.trouveSortie=False #cette variable sera positionnée à True si la sortie est trouvé par 1 joueur
        #On calcule abcisse & oordonnee max de la grille ==> A faire  (pour connaitre murs extérieurs du labyrinthe)
        for key in self.grille:
            if key[0]>self.abcisseMax:
                self.abcisseMax=key[0]
            if key[1]>self.ordonneeMax:
                self.ordonneeMax=key[1]

    def ajouterRobot(self, numJoueur):
        """ Cette fonctionne positionne le robot du joueur numJoueur aléatoirement dans le jeu
                1. on cherche la liste de toutes les positions vides
                2. on fait un random sur cette liste
                3. on stocke la position du robot et on met à jour le labyrinthe
        """
        listeVide=list()
        for cle, valeur in self.grille.items():
            if valeur == Labyrinthe.vide :
                listeVide.append(cle)

        posRobot=random.choice(listeVide)
        self.grille[posRobot]=numJoueur  #le robot du joueur est positionné dans le labyrinthe
        self.robot[numJoueur]=posRobot
        self.porte[numJoueur]=False #le robot n'est pas à l'emplacement d'une porte

    def donnerGrilleJoueur(self, numJoueur):
        """ Cette fonction retourne la grille du labyrinthe en mettant V pour le robot correspondant au joueur passé en parametre et r pour les autres robots
            Attention : on ne modifie pas le labyrinthe, on retourne simplement une chaine de caractères à afficher
        """
        retour=""
        ordonnée = 1
        for cle,v in self.grille.items():
            valeur=""
            if type(v) == int:
                #Donc a cette position du labyrinthe y'a un robot
                if v == numJoueur:
                    valeur=Labyrinthe.robotP
                else:
                    valeur=Labyrinthe.robotA
            else:
                valeur=self.grille[cle]
           
            if cle[0] == ordonnée :
                retour += valeur
            else :   #cela signifie qu'on est passé à la ligne suivante
                retour += "\n"
                ordonnée=cle[0]
                retour +=valeur
        retour += "\n"    
        return retour

    def checkMouvt(self, numJoueur, mvt):
        """ Cette fonction verifie que le joueur peut jouer le mouvement indiqué
        """
        #Première vérification : hors contexte du labyrinthe
        if len(mvt) == 0:
            return False
        if mvt[0] not in Labyrinthe.coupsAutorises:
            return False

        #Ici, on vérifie que si le 1er caractère est m, M, P ou P, alors il est suivi d'un seul cartère : S, N, E ou O
        if len(mvt) == 2:
            if mvt[0] in Labyrinthe.special:
                if mvt[1] not in Labyrinthe.directions:
                    return False
                #else:
                #    return True
            else:  #Donc mouvement standard, le 2ème caractère doit être numérique
                try:
                    pas=int(mvt[1])
                except ValueError:
                    #le nombre de déplacement est incorrect
                    return False
                
        pas=1
        if len(mvt) > 1 and mvt[1] not in Labyrinthe.directions:
            try:
                pas=int(mvt[1:])
            except ValueError:
                #le nombre de déplacement est incorrect
                return False

        #2ème vérification : dans le contexte du labyrinthe, à savoir en tenant compte de la position du joueur, et de la grille actuelle
        #Pour cela on a besoin de connaitre la position du joueur. Rappel, elle est stockée dans le dictionnaire : self.robot
        if mvt[0].upper() == "M":
            #on ne peut murer l'emplacement que si à cet endroit il y a une porte 
            return self.estPorte(self.robot[numJoueur], mvt[1])
        elif mvt[0].upper() == "P":
            #On ne peut percer une porte que si à la place, il y a un mur et que ce mur ne fait par partie de l'enceinte du Labyrinthe
            return self.estMur(self.robot[numJoueur], mvt[1])
        else :
            #Donc il s'agit d'un mouvement standard qui n'est valide que si entre la position actuelle et celle souhaitée, la voie est libre
            return self.estMouvPossible(numJoueur, mvt)

        return True

    def estPorte(self,posJoueur, direction):
        """ Cette fonction vérifie si dans la direction (E, S, O, N) de la postion +1 du joueur, il y a une porte """
        coord=(0,0)
        if direction.upper() == "S":
            coord = (posJoueur[0]+1, posJoueur[1])
        elif direction.upper() == "N":
            coord = (posJoueur[0]-1,posJoueur[1])
        elif direction.upper() == "O":
            coord = (posJoueur[0],posJoueur[1]-1)
        else:
            coord = (posJoueur[0],posJoueur[1]+1)
        try :
            if self.grille[coord] == Labyrinthe.porte:   
                return True
            else :
                return False
        except KeyError :   #On sort du labyrinthe
            return False
            
        
    def estMur(self,posJoueur, direction):
        """ Cette fonction vérifie si dans la direction (E, S, O, N) de la postion +1 du joueur, il y a un mur qui peut être percé pour mettre une porte
        """
        #Attention, on ne peut pas mettre une porte sur l'enceinte du labyrinthe (identifié grace à self.abcisseMax et self.ordonneeMax
        coord=(0,0)
        if direction.upper() == "S":
            coord = (posJoueur[0]+1, posJoueur[1])
        elif direction.upper() == "N":
            coord = (posJoueur[0]-1,posJoueur[1])
        elif direction.upper() == "O":
            coord = (posJoueur[0],posJoueur[1]-1)
        else:
            coord = (posJoueur[0],posJoueur[1]+1)

        if coord[0] == self.abcisseMax or coord[1] == self.ordonneeMax:
            #on est au bord du labyrinthe
            return False
        try :
            if self.grille[coord] == Labyrinthe.mur:   
                return True
            else :
                return False
        except KeyError :   #On sort du labyrinthe
            return False
            
        
    def afficher(self):
        """Cette fonction permet d'afficher à l'écran le labyrinthe
            ainsi que la position des robots dans ce labyrinthe
        """
        ordonnée = 1
        ch=""
        for cle,v in self.grille.items():
            #Pour debug si nécessaire : print("cle = {}, v={}".format(cle,v))
            if cle[0] == ordonnée :
                ch += str(v)
            else :   #cela signifie qu'on est passé à la ligne suivante
                print(ch)
                ordonnée=cle[0]
                ch=str(v)
        #A la fin de la boucle, on n'oublie pas d'afficher la dernière ligne + un saut de ligne
        print(ch+"\n")

    def deplacer(self, numJoueur, mouvt):
        """ On déplace le robot sur la grille
            1. On vérifie si mouvement possible
            2. On modifie le labyrinthe :
                a. à la place de robot, on remet la porte si y'en avait une
                b. on stocke robot

            La fonction retourne un tuple : (True/False, une chaine de commentaire)
        """
        #On commence par s'assurer que le premier caractère est dans la liste des coups possibles
        if mouvt[0] not in Labyrinthe.coupsAutorises :
            return (False,"Mouvement inconnu")
        #Maintenant on regarde si on peut effectuer le mouvement
        if self.checkMouvt(numJoueur, mouvt) == False :
            return (False,"Mouvement non autorisé")
        #Cool, on a le droit de déplacer le robot.
        #On met a jour position du robot (Rappel, elle est stockée dans le dictionnaire : self.robot) + la grille

        coordJoueur=self.robot[numJoueur]   #coord actuelles du robot

        if mouvt[0] in Labyrinthe.special:
            if mouvt[0].upper() == "P":
                nouvCoord=Labyrinthe.calculerCoordonnees(coordJoueur,mouvt[1])
                self.grille[nouvCoord] = Labyrinthe.porte
            else :
                nouvCoord=Labyrinthe.calculerCoordonnees(coordJoueur,mouvt[1])
                self.grille[nouvCoord] = Labyrinthe.mur
            return (True, "Action effectuée")
        
        if len(mouvt) >1:
            nbPas=int(mouvt[1:])   #==> Faudrait ajouter un controle pour s'assurer que c'est un entier (normalement déjà vérifié avant d'arriver ici)
        else:
            nbPas=1

        #calcul des nouvelles coordonnées :
        coord=Labyrinthe.calculerCoordonnees(coordJoueur,mouvt[0], nbPas)            

        #maintenant on met à jour grille et robot, et on mémorise si y'avait une porte
        if self.porte[numJoueur]:
            #Le joueur était positionné sur une porte
            self.grille[coordJoueur] = Labyrinthe.porte
            self.porte[numJoueur]=False
        else:
            self.grille[coordJoueur] = Labyrinthe.vide 
        self.robot[numJoueur] = coord #nouvelle position du robot

        if self.grille[coord] == Labyrinthe.porte:
            self.porte[numJoueur] = True
        else:
            self.porte[numJoueur] = False
        if self.grille[coord] == Labyrinthe.sortie:
            #Le joueur a trouvé la sortie, le jeu va s'arreter
            self.trouveSortie=True
        self.grille[coord] = numJoueur    #nouvelle position du robot
        return (True, "Déplacement effectué")
    
        
    def  estMouvPossible(self, numJoueur,ch):
        """Cette fonction vérifie si le déplacement demandé est possible ou non
            Si le déplacement est possible, la fonction retourne True, False sinon

            Le lien entre points cardinaux et grille :
                S : on augmente ordonnées ==> si robot dans la grille en (o,a), il faut passer en (o+1,a)
                N : on décroit ordonnées ==> si robot dans la grille en (o,a), il faut passer en (o-1,a)
                O : on décroit abcisses ==> si robot dans la grille en (o,a), il faut passer en (o,a-1)
                E : on augmente abcisses ==> si robot dans la grille en (o,a), il faut passer en (o,a+1)

            Remarque : comme dans l'énoncé ce nétait pas clair, nous avons pris l'option de ne pas déplacer le robot si
                       le déplacement global est faux. Une autre option aurait pu être prise : on déplace le robot
                       jusqu'au blocage
        """
        grille=self.grille
        robot = self.robot[numJoueur]

        #Cas spéciaux :
        if ch[0] in Labyrinthe.special:
            return True  #déjà testé    
        
        nbPas=1
        if len(ch) >1:
            nbPas=int(ch[1:])   #controle non nécessaire, déjà effectué lors de la saisie
        #Maintenant on vérifie réellement (il faut que pas de mur ('O') entre position courant et position future  pour pouvoir bouger
        #Faudrait aussi vérifier qu'on ne sort pas du labyrinthe ==> c'est bon, j'ai ajouté
        pas=1
        while pas <= nbPas:
            nouvCoord=Labyrinthe.calculerCoordonnees(robot, ch[0], pas)
            if nouvCoord not in grille:
                return false  #on est sorti du labyrinthe
            if grille[nouvCoord] == Labyrinthe.mur or type(grille[nouvCoord]) == int : #y'a un mur ou un autre robot, on ne peut pas bouger
                return False
            pas += 1
        
        return True

    def retirerJoueur(self, numJoueur):
        """ Cette fonction enlève un joueur du jeu :
            Suppression dans la grille (en remplacant donc sa position par un espace ou une porte
            ==> Pour être vriment clean, on devrait aussi le supprimer des dictionnaires (à faire plus tard)
        """
        coordJoueur=self.robot[numJoueur]   #coord actuelles du robot

        #maintenant on met à jour grille 
        if self.porte[numJoueur]:
            #Le joueur était positionné sur une porte
            self.grille[coordJoueur] = Labyrinthe.porte
            self.porte[numJoueur]=False
        else:
            self.grille[coordJoueur] = Labyrinthe.vide 

        #Pour être vriment clean, faudrait le virer de self.porte et de self.robot

        return True

    def trouverSortie(self):
        """ Cette fonction retoure True si 1 joueur a trouvé la sortie et false dans le cas inverse
        """
        return self.trouveSortie









        
