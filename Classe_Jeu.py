import pygame
import sys
import time
from pygame.locals import *

from Classe_Boule import Boule


class JeuBCI:
    def __init__(self, largeur=800, hauteur=600):  # ← AJOUT PARAMÈTRES
        self.largeur = largeur
        self.hauteur = hauteur
        self.boule = Boule()
        self.obstacles = []
        self.vitesse_route = 4
        self.temps_depart = pygame.time.get_ticks()
        self.bloque = False
        self.temps_final = None
        self.distance = 0
        self.ligne_arrivee = 8000
        self.route_largeur = 350  # ← AJOUT pour draw()
        self.score_font = pygame.font.Font(None, 36)
        self.debug_font = pygame.font.Font(None, 24)
        self.spawn_timer = 0
        self.derniere_commande = None
        self.compteur_commandes = 0

    def redimensionner(self, largeur, hauteur):  # ← CORRIGÉ
        """Adapte à nouveau écran"""
        self.largeur = largeur
        self.hauteur = hauteur
        self.boule.x = largeur // 2  # Recentre

    def update(self, commande_bci=None):  # ← SIMPLIFIÉ (1 seul param)
        """Logique complète"""
        # BCI (seulement si commande + non bloqué)
        if commande_bci and not self.bloque:
            self.nouvelle_commande_bci(commande_bci)

        # Spawn obstacles (aléatoire 1-3s)
        self.spawn_timer += 1
        if self.spawn_timer > random.randint(60, 180):
            self.obstacles.append(Obstacle())
            self.spawn_timer = 0

        # Update obstacles
        vitesse_active = 0 if self.bloque else self.vitesse_route
        self.obstacles = [obs for obs in self.obstacles if not obs.update(vitesse_active)]

        # Collision → bloque
        collision = False
        for obs in self.obstacles:
            if (abs(self.boule.x - (obs.x + obs.largeur/2)) < self.boule.rayon + obs.largeur/2 and
                abs(self.boule.y - (obs.y + obs.hauteur/2)) < self.boule.rayon + obs.hauteur/2):
                self.bloque = True
                collision = True
                break

        # Déblocage
        if self.bloque and not collision:
            self.bloque = False

        # Progression
        if not self.bloque:
            self.distance += vitesse_active
            if self.distance >= self.ligne_arrivee:
                self.temps_final = pygame.time.get_ticks() - self.temps_depart

    def draw(self, screen, largeur, hauteur):  # ← PARAMS EXTERNES
        """Dessin complet"""
        screen.fill(NOIR)

        # Route (relative à largeur)
        route_x = (largeur - self.route_largeur) // 2
        pygame.draw.rect(screen, GRIS, (route_x, 0, self.route_largeur, hauteur))

        # Ligne arrivée
        if self.distance < self.ligne_arrivee:
            arrive_y = hauteur - (self.distance / self.ligne_arrivee * hauteur)
            pygame.draw.line(screen, VERT, 
                           (route_x + 20, arrive_y), 
                           (route_x + self.route_largeur - 20, arrive_y), 6)

        # Obstacles
        for obs in self.obstacles:
            pygame.draw.rect(screen, ROUGE, (obs.x, obs.y, obs.largeur, obs.hauteur))
            pygame.draw.rect(screen, BLANC, (obs.x, obs.y, obs.largeur, obs.hauteur), 2)

        self.boule.draw(screen)

        # UI (relative à hauteur)
        temps = (pygame.time.get_ticks() - self.temps_depart) / 1000
        score_text = self.score_font.render(
            f"Temps: {temps:.1f}s | Distance: {self.distance:.0f}/{self.ligne_arrivee}", 
            True, BLANC)
        screen.blit(score_text, (10, 10))

        status = "BLOQUE" if self.bloque else "ROUTE ACTIVE"
        status_color = ROUGE if self.bloque else VERT
        status_text = self.score_font.render(status, True, status_color)
        screen.blit(status_text, (10, 50))

        if self.derniere_commande:
            cmd_text = self.debug_font.render(
                f"BCI: {self.derniere_commande} ({self.compteur_commandes})", True, BLANC)
            screen.blit(cmd_text, (10, hauteur - 60))

        # Victoire
        if self.temps_final:
            win_rect = pygame.Rect(largeur//2 - 150, hauteur//2 - 50, 300, 100)
            pygame.draw.rect(screen, VERT, win_rect)
            pygame.draw.rect(screen, NOIR, win_rect, 3)
            win_text = self.score_font.render("VICTOIRE!", True, NOIR)
            screen.blit(win_text, (largeur//2 - 60, hauteur//2 - 35))
