import pygame
from pygame.locals import *
from Outils_pygame import *
from Classe_Jeu import JeuBCI

def affichage_jeu(screen, clock, largeur, hauteur):

    running = True
    jeu = JeuBCI(largeur, hauteur)
    
    while running:

        for event in pygame.event.get():
            if event.type == QUIT:
                return "quit"

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return "go_to_menu"

            if event.type == VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), RESIZABLE)
                largeur, hauteur = event.w, event.h
                jeu.redimensionner(largeur, hauteur)

        # ⚡ Ici tu brancheras ton vrai BCI plus tard
        commande_bci = None

        # Exemple test BCI (optionnel)
        # if some_lsl_variable == "left":
        #     commande_bci = "gauche"

        jeu.update(commande_bci)

        # ✅ victoire
        if jeu.temps_final is not None:
            return ("go_to_victoire", jeu.temps_final / 1000)

        screen.fill((20, 20, 40))
        jeu.draw(screen, largeur, hauteur)

        pygame.display.flip()
        clock.tick(60)

    return "go_to_menu"
