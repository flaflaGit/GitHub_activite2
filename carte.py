# -*-coding:Utf-8 -*

"""Ce module contient la classe Carte.
    Avec cette évolution (version client serveur ==> la carte ne doit plus contenir de position du robot
    ==> Si on trouve un bobot, on le remplace pas un espace (cela évite de refaire les cartes existantes)
"""
def creer_labyrinthe_depuis_chaine(chaine):
    """ on transforme la chaine en 1 type dict pour stocker le labyrinthe
        (on aura un clé représentée par un tuple : (ordonnee, abcisse))
            Les valeurs possibe dans la chaine sont :
            'O' : pour un mur
            '.' : pour une porte
            ' ' : pour un vide
            'U' : pour la sortie
            'X' : la position de départ pour le robot ==> si existe, on remplace par un vide
    """
    lab=dict()
    i=1
    j=1
    for c in chaine:
        if c=='\n':
            j += 1
            i = 1
        else:
            if c.upper()=='X':
                c=' '
            lab[j,i] = c
            i += 1
    return lab


class Carte:

    """Objet de transition entre un fichier et un labyrinthe."""

    def __init__(self, nom, chaine):
        self.nom = nom
        self.labyrinthe = creer_labyrinthe_depuis_chaine(chaine)

    def __repr__(self):
        return "<Carte {}>".format(self.nom)

    def dim (self):
        """ Retourne la dimension du labyrinthe sous forme d'une chaine """
        abcisse=0
        ordonnee=0
        for k,v in self.labyrinthe:
            if v > abcisse:
                abcisse=v
            if k > ordonnee:
                ordonnee=k
        return "("+str(abcisse)+"x"+str(ordonnee)+")"

    #A priori cette version n'est plus utile car les cartes initiales ne doivent plus contenir de robot
    def posRobot(self):
        """ Retourne la position du robot sur la carte """
        for cle,val in self.labyrinthe.items():
            if val=="X":
                return cle
        return (0,0)  #A corriger plus tard (faire raiseerror si robot non trouvé ?)


