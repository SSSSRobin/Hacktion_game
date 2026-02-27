import pygame
import sys
import time
from pygame.locals import *

pygame.display.set_caption("BCI - Boule Route Infinie")
clock = pygame.time.Clock()

# Couleurs
NOIR = (0, 0, 0)
BLANC = (255, 255, 255)
GRIS = (128, 128, 128)
ROUGE = (255, 0, 0)
VERT = (0, 255, 0)
BLEU = (0, 100, 255)


class Obstacle:
    def __init__(self):
        self.largeur = 60 + random.randint(-20, 40)
        self.hauteur = 35
        self.x = random.randint(100, LARGEUR - 200)
        self.y = -self.hauteur

    def update(self, vitesse_route):
        self.y += vitesse_route
        return self.y > HAUTEUR
