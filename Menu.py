import pygame

from pygame.locals import *  # On importe les commandes pygame qui relient le code aux pilotes de l'ordi (clavier, souris, etc.)

from Outils_pygame import *  # On importe les fonctions précodées par moi-même utiles au développement d'une interface pygame

from sys import exit



def affichage_menu(screen, clock, largeur, hauteur):
    """
    Fonction affichant un menu avec un titre : "Menu"
    et un bouton central : "Génération du labyrinthe".
    """
    running = True

    while running :
        # ✅ 1️⃣ CALCULS BOUTONS TOUJOURS EN PREMIER (avant events)
        bouton_largeur = largeur // 3
        bouton_hauteur = hauteur // 8
        espacement = largeur // 20
        x_jeu = (largeur - 2*bouton_largeur - espacement) // 2
        x_calib = x_jeu + bouton_largeur + espacement
        y_boutons = hauteur * 2 // 5
        
        # Créer Rects pour draw_button ET collision
        bouton_jeu_rect = pygame.Rect(x_jeu, y_boutons, bouton_largeur, bouton_hauteur)
        bouton_calib_rect = pygame.Rect(x_calib, y_boutons, bouton_largeur, bouton_hauteur)

        # Nettoyage de l'écran principal
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
                
            # ✅ 2️⃣ CLIC TESTÉ DIRECT DANS LA BOUCLE (Rects définis !)
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    if bouton_jeu_rect.collidepoint(mx, my):
                        return "go_to_jeu"
                    elif bouton_calib_rect.collidepoint(mx, my):
                        return "go_to_calibrage"
                    click = True  # Garde pour compatibilité

        # Dessiner boutons (après events)
        draw_button(screen, bouton_jeu_rect, "JEUX", (255,255,255), (100,200,100))
        draw_button(screen, bouton_calib_rect, "CALIBRAGE", (255,255,255), (200,200,100))

        pygame.display.flip()
        # 60 FPS
        clock.tick(60)

