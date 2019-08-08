import random
import unittest
import sys

sys.path.append("..")  #car tous mes modules sont dans le répertoire père, il faut donc ajouter dans le path pour pouvoir importer
from labyrinthe import *
from carte import Carte

class TestLabyrinthe(unittest.TestCase):

	"""Test case utilisé pour tester le module labyrinthe."""

	def setUp(self):
		"""Initialisation des tests."""
		self.robot = (4,9)
		self.grille = {(1, 1): 'O', (1, 2): 'O', (1, 3): 'O', (1, 4): 'O', (1, 5): 'O', (1, 6): 'O', (1, 7): 'O', (1, 8): 'O', (1, 9): 'O', (1, 10): 'O', (2, 1): 'O', (2, 2): ' ', (2, 3): 'O', (2, 4): ' ', (2, 5): ' ', (2, 6): ' ', (2, 7): ' ', (2, 8): 'O', (2, 9): ' ', (2, 10): 'O', (3, 1): 'O', (3, 2): ' ', (3, 3): '.', (3, 4): ' ', (3, 5): 'O', (3, 6): 'O', (3, 7): ' ', (3, 8): ' ', (3, 9): ' ', (3, 10): 'O', (4, 1): 'O', (4, 2): ' ', (4, 3): 'O', (4, 4): ' ', (4, 5): 'O', (4, 6): ' ', (4, 7): ' ', (4, 8): ' ', (4, 9): ' ', (4, 10): 'O', (5, 1): 'O', (5, 2): ' ', (5, 3): 'O', (5, 4): 'O', (5, 5): 'O', (5, 6): 'O', (5, 7): ' ', (5, 8): 'O', (5, 9): '.', (5, 10): 'O', (6, 1): 'O', (6, 2): ' ', (6, 3): 'O', (6, 4): ' ', (6, 5): 'O', (6, 6): ' ', (6, 7): ' ', (6, 8): ' ', (6, 9): ' ', (6, 10): 'U', (7, 1): 'O', (7, 2): 'O', (7, 3): 'O', (7, 4): 'O', (7, 5): 'O', (7, 6): 'O', (7, 7): 'O', (7, 8): 'O', (7, 9): 'O', (7, 10): 'O'}
		self.carte = "OOOOOOOOOO\nO O    O O\nO . OO   O\nO O O   XO\nO OOOO O.O\nO O O    U\nOOOOOOOOOO\n"
		self.listeVide = [(2, 2), (2, 4), (2, 5), (2, 6), (2, 7), (2, 9), (3, 2), (3, 4), (3, 7), (3, 8), (3, 9), (4, 2), (4, 4), (4, 6), (4, 7),(4, 8), (4, 9), (5, 2), (5, 7), (6, 2), (6, 4), (6, 6), (6, 7), (6, 8), (6, 9)]
		self.jeu=Labyrinthe(self.grille)
		#self.jeu.afficher()

	def test_creationLabyrinthe(self):
		"""Test unitaire permettant de vérifier la creation du labyrinthe à partir d'une carte, et le placement aléatoire des robots des joueurs """
		jeu=Labyrinthe(self.grille)
		#1. On ajoute un robot, et on vérifie que sa position est bien dans une place de la grille qui était vide
		jeu.ajouterRobot(1)
		self.assertIn(jeu.robot[1], self.listeVide)
		#2. On vérifie que si on ajouter aun autre robot, il est dans liste vide et différent de position du 1er robot
		jeu.ajouterRobot(2)
		self.assertIn(jeu.robot[2], self.listeVide)
		self.assertNotEqual(jeu.robot[1], jeu.robot[2])

	def test_calculCoord(self):
		"""Test le fonctionnement de la fonction 'calculerCoordonnees' """
		self.assertEqual(Labyrinthe.calculerCoordonnees((4,9),"E"),(4,10))
		self.assertEqual(Labyrinthe.calculerCoordonnees((4,9),"S"),(5,9))
		self.assertEqual(Labyrinthe.calculerCoordonnees((4,9),"N"),(3,9))
		self.assertEqual(Labyrinthe.calculerCoordonnees((4,9),"O"),(4,8))
		self.assertEqual(Labyrinthe.calculerCoordonnees((4,9),"E", 3),(4,12))
                
		
	def test_checkdeplacementRobot(self):
		"""Test le fonctionnement de la fonction 'checkMouvt' qui vérifie si on peut déplacer un robot."""
		#1.On positionne manuellement le robot
		self.jeu.robot[1]=self.robot
		self.jeu.grille[self.robot]=1
		#self.jeu.afficher() #pour debug et vérifier le positionnement des robot sur la grille
		#2. maintenant on teste
		self.assertTrue(self.jeu.checkMouvt(1,"N"))
		self.assertTrue(self.jeu.checkMouvt(1,"N2"))
		self.assertFalse(self.jeu.checkMouvt(1,"N4"))
		self.assertTrue(self.jeu.checkMouvt(1, "S"))
		self.assertTrue(self.jeu.checkMouvt(1, "O"))
		self.assertFalse(self.jeu.checkMouvt(1, "E"))
		self.assertFalse(self.jeu.checkMouvt(1, "mN"))  #il ne peut pas faire un mur au nord
		self.assertTrue(self.jeu.checkMouvt(1, "mS"))   #il peut murer la porte au sud
		self.assertFalse(self.jeu.checkMouvt(1, "pE"))  #il ne peut pas percer une porte en Est (c'est l'enceinte du labyrinthe)
		self.assertFalse(self.jeu.checkMouvt(1, "pS"))  #il ne peut pas percer une porte en Sud (y'a dejà une porte)
		#3. On remplace la porte en S du robot par un mur pour voir si on peut percer la porte
		self.jeu.grille[(5,9)]="O"
		self.assertTrue(self.jeu.checkMouvt(1, "pS"))  #il  peut maintenant percer une porte en Sud

	def test_deplacementRobot(self):
		"""Test le fonctionnement de la fonction 'deplacer' qui déplace un robot."""
		#1.On positionne manuellement le robot
		self.jeu.robot[1]=self.robot
		self.jeu.porte[1]=False
		self.jeu.grille[self.robot]=1
		#self.jeu.afficher() #pour debug et vérifier le positionnement des robot sur la grille
		#2. maintenant on teste : On va faire descendre le robot en S2 puis en E1 pour sortir (auparavant on essayera de sortir du labyrinthe
		retour=self.jeu.deplacer(1, "E")
		self.assertFalse(retour[0])
		retour=self.jeu.deplacer(1, "pE")  #on n'a pas le droit, c'est le mur extérieur du labyrinthe
		self.assertFalse(retour[0])
		self.assertEqual(retour[1], "Mouvement non autorisé")
		retour=self.jeu.deplacer(1, "s2")
		self.assertTrue(retour[0])
		self.assertEqual(retour[1], "Déplacement effectué")
		self.assertFalse(self.jeu.trouverSortie())
		retour=self.jeu.deplacer(1, "mN")
		self.assertTrue(retour[0])
		self.assertEqual(retour[1], "Action effectuée")
		#3. Test sortie trouvée
		retour=self.jeu.deplacer(1, "e")
		self.assertTrue(retour[0])
		self.assertEqual(retour[1], "Déplacement effectué")
		self.assertTrue(self.jeu.trouverSortie())

#Pour tester le code
#unittest.main()

