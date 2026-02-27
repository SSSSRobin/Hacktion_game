import pygame

from Menu import affichage_menu  # affichage_menu -> Fonction affichant le menu

from Jeu import affichage_jeu

from Victoire import affichage_victoire

from Calibrage import *



# Initialisation de tous les modules pygame
pygame.init()

# On récupère la taille de l'écran diminuée de 10% pour un affichage adapté à toute taille d'écran
info = pygame.display.Info()
largeur = int(info.current_w * 0.9)
hauteur = int(info.current_h * 0.9)

# On affiche la page avec son nom
screen = pygame.display.set_mode((largeur, hauteur), pygame.RESIZABLE)
pygame.display.set_caption("Jeu BCI")

# On initialise l'horloge
clock = pygame.time.Clock()

# La page par défaut est le menu
current_page = 'menu'
running = True



while running:


    if current_page == "menu":
        result = affichage_menu(screen, clock, largeur, hauteur)
        if result == 'go_to_jeu':
            current_page = 'jeu'
        elif result == 'go_to_calibrage':
            current_page = 'calibrage'
        elif result == 'quit':
            running = False

            
    if current_page == "jeu":
        result = affichage_jeu(screen, clock, largeur, hauteur)
        if isinstance(result, tuple) and result[0] == "go_to_victoire":
            temps_victoire = result[1]
            current_page = "victoire"
        elif result == "go_to_menu":
            current_page = "menu"
        elif result == "quit":
            running = False



    if current_page == 'calibrage':
        result = affichage_calibrage(screen, clock, largeur, hauteur)
        if result == "go_to_menu":
            current_page = "menu"
        elif result[0] == 'quit':
            running = False

    if current_page == "victoire":
        result = affichage_victoire(screen, clock, largeur, hauteur, temps_victoire)
        if result == "go_to_menu":
            current_page = "menu"
        elif result == "quit":
            running = False

            
    
pygame.quit()

