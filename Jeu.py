import pygame
from pygame.locals import *
from Outils_pygame import *
from Classe_Jeu import JeuBCI  # Ta classe

def affichage_jeu(screen, clock, largeur, hauteur):
    """
    Interface jeu BCI boule route infinie
    Compatible avec structure Main.py / Menu.py
    """
    running = True
    jeu = JeuBCI(largeur, hauteur)  # Initialise avec dimensions écran
    
    while running:
        # Événements (cohérent avec Menu.py)
        mx, my = pygame.mouse.get_pos()
        click = False
        
        for event in pygame.event.get():
            if event.type == QUIT:
                return "quit"
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return "go_to_menu"
            if event.type == VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), RESIZABLE)
                largeur, hauteur = event.w, event.h
                jeu.redimensionner(largeur, hauteur)  # Met à jour ta classe
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        
        # Commandes BCI / Clavier (flèches G/D)
        keys = pygame.key.get_pressed()
        commande_bci = None
        if keys[K_LEFT] or keys[K_a]:
            commande_bci = "gauche"
        elif keys[K_RIGHT] or keys[K_d]:
            commande_bci = "droite"
        
        # Update jeu (ta classe gère tout)
        jeu.update(commande_bci, bloque=jeu.bloque)
        
        # Nettoyage écran + affichage (cohérent Menu.py)
        screen.fill((20, 20, 40))  # Fond bleu nuit
        
        # Dessine avec ta classe (adapte à tes dims)
        jeu.draw(screen, largeur, hauteur)
        
        pygame.display.flip()
        clock.tick(60)  # 60 FPS comme Menu.py
    
    return "go_to_menu"

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600), RESIZABLE)
    clock = pygame.time.Clock()
    result = affichage_jeu(screen, clock, 800, 600)
