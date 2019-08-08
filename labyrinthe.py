# -*-coding:Utf-8 -*

"""Ce module contient la classe Labyrinthe."""

class Labyrinthe:

    """Classe représentant un labyrinthe."""
    coupsAutorises=('N', 'E', 'S', 'O', 'n', 'e', 's', 'o')
    mur="O"
    porte="."
    sortie="U"

    def __init__(self, robot, obstacles):
        self.robot = robot #un tuple indiquant position courante du robot au sein de la grille (le labyrinthe)
        self.grille = obstacles
        self.porte = False #cette valeur sera positionnée à True lorsque le robot sera dessus (pour éviter de mémoriser dans une variable la liste des portes) du jeu
        self.trouveSortie=False #cette variable sera positionnée à True si la sortie est trouvé
        # ...

    def afficher(self):
        """Cette fonction permet d'afficher à l'écran le labyrinthe
            ainsi que la position du robot dans ce labyrinthe
        """
        ordonnée = 1
        ch=""
        for cle,v in self.grille.items():
            #Pour debug si nécessaire : print("cle = {}, v={}".format(cle,v))
            if cle[0] == ordonnée :
                ch += v
            else :   #cela signifie qu'on est passé à la lgine suivante
                print(ch)
                ordonnée=cle[0]
                ch=v
        #A la fin de la boucle, on n'oublie pas d'afficher la dernière ligne + un saut de ligne
        print(ch+"\n")

    def deplacerUnPas(self, sens):
        """ On déplace le robot sur la grille d'un seul pas, dans le sens du paramètre
            Pas besoin de vérifier si possible ou non (cela a été vérifié avant l'appel à la fonction)
             On modifie le labyrinthe :
                a. à la place de robot, on remet la porte si y'en avait une
                b. on stocke nouvelle position du robot
        """
        sens=sens.upper() #on ne s'occupe plus de savoir si minuscule ou majuscule

        self.grille[self.robot[0],self.robot[1]] = " " # on verra plus tard pour les portes

        #calcul des nouvelles coordonnées :
        if sens == "S":
            coord = (self.robot[0]+1, self.robot[1])
        elif sens == "N":
            coord = (self.robot[0]-1,self.robot[1])
        elif sens == "O":
            coord = (self.robot[0],self.robot[1]-1)
        else:
            coord = (self.robot[0],self.robot[1]+1)

        #maintenant on met à jour grille et robot, et on memorise si y'avait une porte
        if self.porte :  #Donc le robot était dans une porte
            self.grille[self.robot] = "." #on repositionne la porte avant de mettre le reste à jour
        self.robot = coord
        if self.grille[coord] == ".":
            self.porte = True
        elif self.grille[coord] == "U":
            self.trouveSortie = True
        else:
            self.porte = False
        self.grille[coord] = "X"    #nouvelle position du robot
        return True

    def deplacer(self, mouvt):
        """ On déplace le robot sur la grille
            1. On vérifie si mouvement possible
            2. On modifie le labyrinthe :
                a. à la place de robot, on remet la porte si y'en avait une
                b. on stocke robot
            La fonction retourne True si mouvement OK, False dans tous les autres cas

            Remarque : fonction à utiliser si on ne veut pas afficher la grille pour chaque pas du robot
        """
        #On commence par s'assurer que le premier caractère est dans la liste des coups possibles
        if mouvt[0] not in coupsAutorises :
            return False
        #Maintenant on regarde si on peut effectuer le mouvement
        if self.estPossible(mouvt) == False :
            return False
        #Cool, on a le droit de déplacer le robot.
        #On met a jour position du robot + la grille
        self.grille[self.robot[0],self.robot[1]] = " " # on verra plus tard pour les portes
        if len(mouvt) >1:
            nbPas=int(mouvt[1:])   #==> Faudra ajouter un controle pour s'assurer que c'est un entier (normalement déjà vérifié)
        else:
            nbPas=1

        #calcul des nouvelles coordonnées :
        if mouvt[0].upper() == "S":
            coord = (self.robot[0]+nbPas, self.robot[1])
        elif mouvt[0].upper() == "N":
            coord = (self.robot[0]-nbPas,self.robot[1])
        elif mouvt[0].upper() == "O":
            coord = (self.robot[0],self.robot[1]-nbPas)
        else:
            coord = (self.robot[0],self.robot[1]+nbPas)

        #maintenant on met à jour grille et robot, et on memorise si y'avait une porte
        if self.porte :  #Donc le robot était dans une porte
            self.grille[self.robot] = "." #on repositionne la porte avant de mettre le reste à jour
        self.robot = coord #nouvelle position du robot
        if self.grille[coord] == ".":
            self.porte = True
        else:
            self.porte = False
        self.grille[coord] = "X"    #nouvelle position du robot
        return True
    
        
    def  estPossible(self, ch):
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
        robot = self.robot
        nbPas=1
        if len(ch) >1:
            nbPas=int(ch[1:])   #controle non nécessaire, déjà effectué lors de la saisie
        #Maintenant on vérifie réellement (il faut que pas de mur ('O') entre position courant et position future  pour pouvoir bouger
        #Faudrait aussi vérifier qu'on ne sort pas du labyrinthe
        pas=1
        while pas <= nbPas:
            if ch[0].upper() == "S":
                if grille[robot[0]+pas,robot[1]] == "O" : #y'a un mur, on ne peut pas bouger
                    return False
            elif ch[0].upper() == "N":
                if grille[robot[0]-pas,robot[1]] == "O" : #y'a un mur, on ne peut pas bouger
                    return False
            elif ch[0].upper() == "O":
                if grille[robot[0],robot[1]-pas] == "O" : #y'a un mur, on ne peut pas bouger
                    return False
            else: #donc le mouvement est vers l'est 
                if grille[robot[0],robot[1]+pas] == "O" : #y'a un mur, on ne peut pas bouger
                    return False
            pas += 1
        
        return True

    def trouverSortie(self):
        """ Cette fonction retoure True si le joueur a trouvé la sortie et false dans le cas inverse
        """
        return self.trouveSortie









        
