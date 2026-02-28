import pygame
import random
from pygame.locals import *

from Classe_Obstacle import Obstacle
from Classe_Boule import Boule

# Couleurs RGB
NOIR = (0, 0, 0)
BLANC = (255, 255, 255)
ROUGE = (255, 0, 0)
VERT = (0, 255, 0)
GRIS = (128, 128, 128)
LILAS = (245, 230, 255)
MAUVE = (230, 215, 250)

class JeuBCI:
    def __init__(self, largeur, hauteur):
        self.image_arrivee_originale = pygame.image.load("Images/Ligne_Arrivee.png").convert_alpha()
        self.image_arrivee = None
        
        self.coeff_vitesse_obstacles = 0.5
        
        self.largeur = largeur
        self.hauteur = hauteur
        
        self.base_largeur = 800
        self.base_hauteur = 600

        self.scale_x = largeur / self.base_largeur
        self.scale_y = hauteur / self.base_hauteur
        self.scale = min(self.scale_x, self.scale_y)

        self.boule = Boule(largeur, hauteur, self.scale)
        self.obstacles = []

        self.vitesse_route = 4 * self.scale * self.coeff_vitesse_obstacles

        # Ligne d'arrivée
        self.arrivee_generee = False
        self.arrivee_rect = None

##        self.image_arrivee = pygame.transform.scale(
##            self.image_arrivee_originale,
##            (self.arrivee_rect.width, self.arrivee_rect.height))
        
        self.arrivee_vitesse = self.vitesse_route
        
        self.temps_depart = pygame.time.get_ticks()
        self.bloque = False
        self.temps_final = None
        self.distance = 0
        self.ligne_arrivee = 8000
        self.route_largeur = largeur // 3

        self.score_font = pygame.font.Font(None, 36)
        self.debug_font = pygame.font.Font(None, 24)

        self.spawn_timer = 0
        self.derniere_commande = None
        self.compteur_commandes = 0

    def redimensionner(self, largeur, hauteur):

        self.largeur = largeur
        self.hauteur = hauteur

        self.scale_x = largeur / self.base_largeur
        self.scale_y = hauteur / self.base_hauteur
        self.scale = min(self.scale_x, self.scale_y)
        
        self.vitesse_route = 4 * self.scale * self.coeff_vitesse_obstacles

        # Mettre à jour seulement la vitesse, sans reset l'état de victoire
        self.arrivee_vitesse = self.vitesse_route
        
        self.route_largeur = largeur // 3
        route_x = (largeur - self.route_largeur) // 2

        # Si la ligne d'arrivée existe, la recaler sur la nouvelle route
        if self.arrivee_rect is not None:
            self.arrivee_rect.x = route_x
            self.arrivee_rect.width = self.route_largeur

        if self.arrivee_rect is not None:
            self.image_arrivee = pygame.transform.scale(
                self.image_arrivee_originale,
                (self.arrivee_rect.width, self.arrivee_rect.height))

        self.score_font = pygame.font.Font(None, int(36 * self.scale))
        self.debug_font = pygame.font.Font(None, int(24 * self.scale))

        for obs in self.obstacles:
            obs.redimensionner(largeur, hauteur, route_x, self.route_largeur, self.scale)

        self.boule.redimensionner(largeur, hauteur, self.scale)

    # ✅ NOUVELLE MÉTHODE PROPRE
    def nouvelle_commande_bci(self, commande):
        self.derniere_commande = commande
        self.compteur_commandes += 1
        self.boule.update_bci(commande)

    def update(self, commande_bci=None):

        keys = pygame.key.get_pressed()

        # ✅ Mouvement autorisé même si bloqué
        if commande_bci:
            self.nouvelle_commande_bci(commande_bci)
        else:
            self.boule.update_clavier(keys)

        # ✅ Limite la boule à la route
        route_x = (self.largeur - self.route_largeur) // 2
        limite_gauche = route_x + self.boule.rayon
        limite_droite = route_x + self.route_largeur - self.boule.rayon
        self.boule.x = max(limite_gauche, min(limite_droite, self.boule.x))

        # ✅ Spawn obstacles UNIQUEMENT si pas bloqué
        if not self.bloque:
            self.spawn_timer += 1
            if self.spawn_timer > random.randint(120, 300):

                route_x = (self.largeur - self.route_largeur) // 2

                self.obstacles.append(
                    Obstacle(
                        self.largeur,
                        self.hauteur,
                        route_x,
                        self.route_largeur,
                        self.scale
                    )
                )

                self.spawn_timer = 0

        # ✅ Update obstacles (figés si bloqué)
        vitesse_active = 0 if self.bloque else self.vitesse_route
        self.obstacles = [obs for obs in self.obstacles if not obs.update(vitesse_active)]

        # Déplacement ligne d'arrivée
        if self.arrivee_generee and self.arrivee_rect and self.temps_final is None:
            if not self.bloque:
                self.arrivee_rect.y += self.arrivee_vitesse

        # ✅ Collision
        collision = False
        for obs in self.obstacles:
            if (abs(self.boule.x - (obs.x + obs.largeur/2)) < self.boule.rayon + obs.largeur/2 and
                abs(self.boule.y - (obs.y + obs.hauteur/2)) < self.boule.rayon + obs.hauteur/2):
                self.bloque = True
                collision = True
                break

        # Collision ligne arrivée = victoire
        if self.arrivee_rect and self.temps_final is None:
            if self.arrivee_rect.colliderect(
                pygame.Rect(
                    self.boule.x - self.boule.rayon,
                    self.boule.y - self.boule.rayon,
                    self.boule.rayon * 2,
                    self.boule.rayon * 2
                )
            ):
                self.temps_final = pygame.time.get_ticks() - self.temps_depart

        # ✅ Déblocage automatique
        if self.bloque and not collision:
            self.bloque = False

        # Distance progresse tant que pas encore généré la ligne
        if not self.bloque and not self.arrivee_generee:
            self.distance += vitesse_active

            if self.distance >= self.ligne_arrivee:
                self.arrivee_generee = True

                route_x = (self.largeur - self.route_largeur) // 2

                hauteur_arrivee = int(80 * self.scale)  # ← augmente l'épaisseur ici

                self.arrivee_rect = pygame.Rect(
                    route_x,
                    -hauteur_arrivee,
                    self.route_largeur,
                    hauteur_arrivee
                )

                self.image_arrivee = pygame.transform.scale(
                    self.image_arrivee_originale,
                    (self.arrivee_rect.width, self.arrivee_rect.height))
                
    def draw(self, screen, largeur, hauteur):

        screen.fill(MAUVE)

        route_x = (largeur - self.route_largeur) // 2
        pygame.draw.rect(screen, LILAS, (route_x, 0, self.route_largeur, hauteur))

        # Dessiner ligne d'arrivée
        if self.arrivee_rect and self.image_arrivee:
            screen.blit(self.image_arrivee, self.arrivee_rect)
            
        for obs in self.obstacles:
            obs.draw(screen)
    
        self.boule.draw(screen)

        temps = (pygame.time.get_ticks() - self.temps_depart) / 1000
        score_text = self.score_font.render(
            f"Temps: {temps:.1f}s | Distance: {self.distance:.0f}/{self.ligne_arrivee}", 
            True, BLANC)
        screen.blit(score_text, (10, 10))
