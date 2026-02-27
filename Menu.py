from Classe_Graphe import Graphe  # On importe ma classe graphe
import pygame

from pygame.locals import *  # On importe les commandes pygame qui relient le code aux pilotes de l'ordi (clavier, souris, etc.)

from Outils_pygame import *  # On importe les fonctions précodées par moi-même utiles au développement d'une interface pygame

from sys import exit



def affichage_menu(screen, clock, largeur, hauteur):
    """
    Fonction affichant un menu avec un titre : "Menu"
    et un bouton central : "Génération du labyrinthe".

    Une fois cliqué
    on lance l'affichage de la console pour entrer les dimensions
    du labyrinthe/damier.
    """
    running = True

    while running :
        # Nettoyage de l’écran principal
        screen.fill((200, 200, 200))

        # On récupère les coordonnées du curseur de la souris
        mx, my = pygame.mouse.get_pos()       
        click = False

        for event in pygame.event.get():
            # Si croix cochée on quitte l'interface
            if event.type == QUIT:
                return "quit"

            # Si bouton escape touché on quitte l'interface
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return "quit"

            # Adapte la fenêtre au redimensionnement
            if event.type == VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), RESIZABLE)
                largeur, hauteur = event.w, event.h
                
            # Si click gauche effectué, click devient True
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        # On dessine le titre de la page
        titre_font = adapt_font("Menu", font_path, largeur, hauteur // 40)
        draw_text("Menu", titre_font, (0,0,0), screen, largeur // 80, hauteur // 80)

                    
        # On dessine le bouton central de manière dynamique, en fonction de la résolution de l'écran
        button_damier = pygame.Rect(largeur // 3, hauteur // 3, largeur // 3, hauteur // 3)
        draw_button(screen, button_damier, "Génération aléatoire du labyrinthe", (0, 0, 0), (255, 255, 255))

        # Si le bouton central est cliqué on sort de la boucle en renvoyant dans Main : "go_to_console"
        if click and button_damier.collidepoint((mx, my)):
            return "go_to_console"



        pygame.display.flip()
        # 60 FPS
        clock.tick(60)

