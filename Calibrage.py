import pygame
import random
from pylsl import StreamInfo, StreamOutlet, local_clock

from Classe_Calibrage import CalibrageBCI

def affichage_calibrage(screen, clock, largeur, hauteur):
    calibrage = CalibrageBCI(largeur, hauteur)
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return ("quit",)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "go_to_menu"

        result = calibrage.update()
        if result == "finish":
            return "go_to_menu"

        calibrage.draw(screen)

        pygame.display.flip()
        clock.tick(60)
