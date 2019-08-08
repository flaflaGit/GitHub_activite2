import random
import unittest
import sys

sys.path.append("..")  #car tous mes modules sont dans le répertoire père, il faut donc ajouter dans le path pour pouvoir importer
from carte import Carte

class TestCarte(unittest.TestCase):

	"""Tests case utilisé pour tester le module carte."""

	def setUp(self):
		"""Initialisation des tests."""
		self.grille = {(1, 1): 'O', (1, 2): 'O', (1, 3): 'O', (1, 4): 'O', (1, 5): 'O', (1, 6): 'O', (1, 7): 'O', (1, 8): 'O', (1, 9): 'O', (1, 10): 'O', (2, 1): 'O', (2, 2): ' ', (2, 3): 'O', (2, 4): ' ', (2, 5): ' ', (2, 6): ' ', (2, 7): ' ', (2, 8): 'O', (2, 9): ' ', (2, 10): 'O', (3, 1): 'O', (3, 2): ' ', (3, 3): '.', (3, 4): ' ', (3, 5): 'O', (3, 6): 'O', (3, 7): ' ', (3, 8): ' ', (3, 9): ' ', (3, 10): 'O', (4, 1): 'O', (4, 2): ' ', (4, 3): 'O', (4, 4): ' ', (4, 5): 'O', (4, 6): ' ', (4, 7): ' ', (4, 8): ' ', (4, 9): ' ', (4, 10): 'O', (5, 1): 'O', (5, 2): ' ', (5, 3): 'O', (5, 4): 'O', (5, 5): 'O', (5, 6): 'O', (5, 7): ' ', (5, 8): 'O', (5, 9): '.', (5, 10): 'O', (6, 1): 'O', (6, 2): ' ', (6, 3): 'O', (6, 4): ' ', (6, 5): 'O', (6, 6): ' ', (6, 7): ' ', (6, 8): ' ', (6, 9): ' ', (6, 10): 'U', (7, 1): 'O', (7, 2): 'O', (7, 3): 'O', (7, 4): 'O', (7, 5): 'O', (7, 6): 'O', (7, 7): 'O', (7, 8): 'O', (7, 9): 'O', (7, 10): 'O'}
		self.carte = "OOOOOOOOOO\nO O    O O\nO . OO   O\nO O O   XO\nO OOOO O.O\nO O O    U\nOOOOOOOOOO\n"

	def test_initCarte(self):
		"""Test unitaire permettant de vérifier la creation d'une carte à partir d'une chaine de caractères """
		maCarte=Carte('test',self.carte)
		#1. on vérifie si carte à les bonnes dimensions
		self.assertEqual(maCarte.dim(), "(10x7)")
		#2.On vérifie qu'aucun robot n'est encore positionné
		self.assertEqual(maCarte.posRobot(), (0,0))
		#3.On vérifie que cela fait bien la représentation attendue
		self.assertEqual(maCarte.labyrinthe, self.grille)


#Pour tester le code
#unittest.main()

