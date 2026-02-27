import random

class Obstacle:
    def __init__(self, largeur_ecran, hauteur_ecran, route_x, route_largeur, scale):
        self.route_x = route_x
        self.route_largeur = route_largeur

        self.largeur_ecran = largeur_ecran
        self.hauteur_ecran = hauteur_ecran
        self.scale = scale

        # tailles de base
        self.base_largeur = 60 + random.randint(-20, 40)
        self.base_hauteur = 35

        self.largeur = int(self.base_largeur * scale)
        self.hauteur = int(self.base_hauteur * scale)

        # position aléatoire dans la route
        self.x = random.randint(
            route_x,
            route_x + route_largeur - self.largeur
        )

        self.y = -self.hauteur

    def redimensionner(self, largeur_ecran, hauteur_ecran, route_x, route_largeur, scale):
        """appelé quand la fenêtre change"""
        self.largeur_ecran = largeur_ecran
        self.hauteur_ecran = hauteur_ecran
        self.route_x = route_x
        self.route_largeur = route_largeur
        self.scale = scale

        # recalcul tailles
        self.largeur = int(self.base_largeur * scale)
        self.hauteur = int(self.base_hauteur * scale)

        # garde l’obstacle dans la route
        self.x = max(
            route_x,
            min(route_x + route_largeur - self.largeur, self.x)
        )

    def update(self, vitesse_route):
        self.y += vitesse_route
        return self.y > self.hauteur_ecran
