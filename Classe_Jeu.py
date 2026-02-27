import pygame
import sys
import time
import random
from pygame.locals import *

from Classe_Boule import Boule

from Classe_Obstacle import Obstacle
pygame.display.set_caption("BCI - Boule Route Infinie")
clock = pygame.time.Clock()

# Couleurs
NOIR = (0, 0, 0)
BLANC = (255, 255, 255)
GRIS = (128, 128, 128)
ROUGE = (255, 0, 0)
VERT = (0, 255, 0)
BLEU = (0, 100, 255)


class JeuBCI:
    def __init__(self):
        self.boule = Boule()
        self.obstacles = []
        self.vitesse_route = 4  # Constante
        self.temps_depart = pygame.time.get_ticks()
        self.bloque = False
        self.temps_final = None
        self.distance = 0
        self.ligne_arrivee = 8000
        self.score_font = pygame.font.Font(None, 36)
        self.debug_font = pygame.font.Font(None, 24)
        self.spawn_timer = 0
        self.derniere_commande = None
        self.compteur_commandes = 0

    def nouvelle_commande_bci(self, commande):
        """Simule réception BCI - À remplacer par vraie interface"""
        self.derniere_commande = commande
        self.compteur_commandes += 1
        if commande:
            self.boule.update_bci(commande)

    def update(self):
        keys = pygame.key.get_pressed()
        self.boule.update_clavier(keys)  # Fallback clavier

        # Spawn obstacles (constante)
        self.spawn_timer += 1
        if self.spawn_timer > random.randint(60, 180):  # 1-3s aléatoire
            self.obstacles.append(Obstacle())
            self.spawn_timer = 0


        # Update obstacles
        vitesse_active = 0 if self.bloque else self.vitesse_route
        self.obstacles = [obs for obs in self.obstacles if not obs.update(vitesse_active)]

        # Collision
        collision = False
        for obs in self.obstacles:
            if (abs(self.boule.x - (obs.x + obs.largeur/2)) < self.boule.rayon + obs.largeur/2 and
                abs(self.boule.y - (obs.y + obs.hauteur/2)) < self.boule.rayon + obs.hauteur/2):
                self.bloque = True
                collision = True
                break

        # Déblocage auto quand plus de collision
        if self.bloque and not collision:
            self.bloque = False

        # Progression
        if not self.bloque:
            self.distance += vitesse_active
            if self.distance >= self.ligne_arrivee:
                self.temps_final = pygame.time.get_ticks() - self.temps_depart

    def draw(self, screen):
        screen.fill(NOIR)

        # Route
        route_largeur = 350
        route_x = (LARGEUR - route_largeur) // 2
        pygame.draw.rect(screen, GRIS, (route_x, 0, route_largeur, HAUTEUR))
        
        # Ligne d'arrivée
        if self.distance < self.ligne_arrivee:
            arrive_y = HAUTEUR - (self.distance / self.ligne_arrivee * HAUTEUR)
            pygame.draw.line(screen, VERT, 
                           (route_x + 20, arrive_y), 
                           (route_x + route_largeur - 20, arrive_y), 6)

        # Obstacles
        for obs in self.obstacles:
            pygame.draw.rect(screen, ROUGE, 
                           (obs.x, obs.y, obs.largeur, obs.hauteur))
            pygame.draw.rect(screen, BLANC, 
                           (obs.x, obs.y, obs.largeur, obs.hauteur), 2)

        self.boule.draw(screen)

        # UI
        temps = (pygame.time.get_ticks() - self.temps_depart) / 1000
        score_text = self.score_font.render(
            f"Temps: {temps:.1f}s | Distance: {self.distance:.0f}/{self.ligne_arrivee}", 
            True, BLANC)
        screen.blit(score_text, (10, 10))

        status = "BLOQUE" if self.bloque else "ROUTE ACTIVE"
        status_color = ROUGE if self.bloque else VERT
        status_text = self.score_font.render(status, True, status_color)
        screen.blit(status_text, (10, 50))

        # Debug BCI
        if self.derniere_commande:
            cmd_text = self.debug_font.render(
                f"BCI: {self.derniere_commande} ({self.compteur_commandes})", True, BLANC)
            screen.blit(cmd_text, (10, HAUTEUR - 60))
        
        controle_text = self.debug_font.render("A/D ou flèches (fallback)", True, BLANC)
        screen.blit(controle_text, (10, HAUTEUR - 30))

        # Victoire
        if self.temps_final:
            win_rect = pygame.Rect(LARGEUR//2 - 150, HAUTEUR//2 - 50, 300, 100)
            pygame.draw.rect(screen, VERT, win_rect)
            pygame.draw.rect(screen, NOIR, win_rect, 3)
            
            win_text = self.score_font.render(f"VICTOIRE!", True, NOIR)
            screen.blit(win_text, (LARGEUR//2 - 60, HAUTEUR//2 - 35))
            
            temps_text = self.debug_font.render(f"Temps: {self.temps_final/1000:.1f}s", True, NOIR)
            screen.blit(temps_text, (LARGEUR//2 - 50, HAUTEUR//2 - 5))

    def run(self):
        running = True
        bci_queue = []  # File commandes BCI externes
        
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    elif event.key == K_LEFT or event.key == K_a:
                        self.nouvelle_commande_bci("gauche")
                    elif event.key == K_RIGHT or event.key == K_d:
                        self.nouvelle_commande_bci("droite")
            
            # 🔄 BCI CONTINUE (à coder)
            # commande = recevoir_bci_continue()  # Ta source externe
            # if commande:
            #     bci_queue.append(commande)
            
            # Traite 1 commande max par frame (anti-spam)
            if bci_queue:
                commande = bci_queue.pop(0)
                self.nouvelle_commande_bci(commande)
            
            self.update()
            self.draw(screen)
            pygame.display.flip()
            clock.tick(60)


        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    jeu = JeuBCI()
    jeu.run()
