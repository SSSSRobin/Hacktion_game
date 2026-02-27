import pygame

from Menu import affichage_menu  # affichage_menu -> Fonction affichant le menu

from Console import affichage_console  # affichage_console -> Fonction affichant la console au sein de laquelle l'utilisateur entre les dimensions du damier de base

from Damier import affichage_damier  # affichage_damier -> Fonction affichant le damier aux dimensions voulu à partir duquel on construit le labyrinthe

from Labyrinthe import affichage_labyrinthe, excavation
# affichage_labyrinthe -> Fonction affichant le labyrinthe généré par un parcours en profondeur (DFS)
# excavation -> Fonction générant le labyrinthe au sein du graphe avec un parcours en profondeur (DFS) -> "détruit les murs"

from Aleatoire import affichage_aleatoire  # Fonction affichant le chemin généré par un parcours en profondeur (DFS)

from Meilleur import affichage_meilleur  # Fonction affichant le chemin généré par un algorithme de Dijkstra



# Initialisation de tous les modules pygame
pygame.init()

# On récupère la taille de l'écran diminuée de 10% pour un affichage adapté à toute taille d'écran
info = pygame.display.Info()
largeur = int(info.current_w * 0.9)
hauteur = int(info.current_h * 0.9)

# On affiche la page avec son nom
screen = pygame.display.set_mode((largeur, hauteur), pygame.RESIZABLE)
pygame.display.set_caption("Labyrinthe")

# On initialise l'horloge
clock = pygame.time.Clock()

# La page par défaut est le menu
current_page = 'menu'
running = True



while running:

    # Si on est sur le menu, on regarde si on veut rester, le quitter ou naviguer sur une autre page, càd, la console de saisie des dimensions
    if current_page == "menu":
        result = affichage_menu(screen, clock, largeur, hauteur)
        if result == 'go_to_console':
            current_page = 'console'
        elif result == 'quit':
            running = False

            
    # Si on est sur la console, on regarde si on veut rester, la quitter ou naviguer sur une autre page, càd :
    #   - la page de génération de damier,
    #   - la page de menu
    if current_page == "console":
        result = affichage_console(screen, clock, largeur, hauteur)
        if result[0] == "go_to_damier":
            current_page = "damier"
            n = result[1]
            p = result[2]
        elif result[0] == "go_to_menu":
            current_page = "menu"
        elif result[0] == "quit":
            running = False


    # Si on est sur le générateur de damier, on regarde si on veut rester, le quitter ou naviguer sur une autre page, càd :
    #   - la page de génération du labyrinthe,
    #   - la console de saisie des dimensions
    if current_page == 'damier':
        result = affichage_damier(screen, clock, largeur, hauteur, n, p)
        if result[0] == 'go_to_labyrinthe':
            current_page = 'labyrinthe'
            graphe = result[1]
            # Je génère à ce moment le labyrinthe pour que dans la navigation des pages suivantes on prenne toujours en compte le même labyrinthe.
            # Il faut donc revenir au damier pour générer un nouveau labyrinthe.
            labyrinthe, case_entree, cote_entree, case_sortie, cote_sortie = excavation(graphe)
        if result[0] == "go_to_console":
            current_page = "console"
        elif result[0] == 'quit':
            running = False

            
    # Si on est sur le générateur de labyrinthe, on regarde si on veut rester, le quitter ou naviguer sur une autre page, càd :
    #   - la page de génération du chemin par parcours en profondeur,
    #   - la page de génération du chemin par Dijkstra,
    #   - la page de génération du damier
    if current_page == 'labyrinthe':
        result = affichage_labyrinthe(screen, clock, largeur, hauteur,
                                  labyrinthe, case_entree, cote_entree, case_sortie, cote_sortie)
        if result[0] == 'go_to_damier':
            current_page = 'damier'
        # Si on génère un chemin il me faut garder le labyrinthe construit mais aussi les infos sur l'entrée et la sortie
        elif result[0] == "go_to_aleatoire":
            current_page = "aleatoire"
            labyrinthe = result[1]
            case_entree = result[2]
            cote_entree = result[3]
            case_sortie = result[4]
            cote_sortie = result[5]
        elif result[0] == "go_to_meilleur":
            current_page = "meilleur"
            labyrinthe = result[1]
            case_entree = result[2]
            cote_entree = result[3]
            case_sortie = result[4]
            cote_sortie = result[5]
        elif result[0] == 'quit':
            running = False


    # Si on est sur le générateur de chemin par parcours en profondeur, on regarde si on veut rester, le quitter ou naviguer sur une autre page, càd,
    # la page de génération du labyrinthe
    if current_page == "aleatoire":
        result = affichage_aleatoire(screen, clock, largeur, hauteur, labyrinthe, case_entree, cote_entree, case_sortie, cote_sortie)
        # Si on revient en arrière, pour ne pas générer un nouveau labyrinthe et afficher le même, je renvoie le labyrinthe que je transporte de page en page
        if result[0] == 'go_to_labyrinthe':
            current_page = 'labyrinthe'
            labyrinthe = result[1]
        elif result[0] == 'quit':
            running = False


    # Si on est sur le générateur de chemin par algorithme de Dijkstra, on regarde si on veut rester, le quitter ou naviguer sur une autre page, càd,
    # la page de génération du labyrinthe
    if current_page == "meilleur":
        result = affichage_meilleur(screen, clock, largeur, hauteur, labyrinthe, case_entree, cote_entree, case_sortie, cote_sortie)
        # Si on revient en arrière, pour ne pas générer un nouveau labyrinthe et afficher le même, je renvoie le labyrinthe que je transporte de page en page
        if result[0] == 'go_to_labyrinthe':
            current_page = 'labyrinthe'
            labyrinthe = result[1]
        elif result[0] == 'quit':
            running = False
pygame.quit()
