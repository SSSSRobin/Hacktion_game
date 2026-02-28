import pygame
import socket
from pygame.locals import *
from Outils_pygame import *
from Classe_Jeu import JeuBCI

class UdpBCIReceiver:
    def __init__(self, ip="127.0.0.1", port=5005):
        self.addr = (ip, port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(self.addr)
        self.sock.setblocking(False)  # IMPORTANT : ne bloque jamais la boucle pygame
        self.last_value = None

    def poll(self):
        """Lit tous les paquets dispo (non bloquant) et renvoie la dernière commande."""
        cmd = None
        while True:
            try:
                data, _ = self.sock.recvfrom(1024)
            except BlockingIOError:
                break  # plus rien à lire

            s = data.decode("utf-8").strip()
            print("[UDP RECU]", repr(s))
            if s == "-1":
                cmd = "gauche"
            elif s == "1":
                cmd = "droite"
            else:
                cmd = None

        return cmd

    def close(self):
        try:
            self.sock.close()
        except Exception:
            pass

def affichage_jeu(screen, clock, largeur, hauteur):

    running = True
    jeu = JeuBCI(largeur, hauteur)
    
    bci_udp = UdpBCIReceiver(ip="127.0.0.1", port=5005)
    
    while running:

        for event in pygame.event.get():
            if event.type == QUIT:
                bci_udp.close()
                return "quit"

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    bci_udp.close()
                    return "go_to_menu"

            if event.type == VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), RESIZABLE)
                largeur, hauteur = event.w, event.h
                jeu.redimensionner(largeur, hauteur)

        # ⚡ Ici tu brancheras ton vrai BCI plus tard
        commande_bci = bci_udp.poll()
        jeu.update(commande_bci)

        # ✅ victoire
        if jeu.temps_final is not None:
            bci_udp.close()
            return ("go_to_victoire", jeu.temps_final / 1000)

        screen.fill((200, 170, 255))
        jeu.draw(screen, largeur, hauteur)

        pygame.display.flip()
        clock.tick(60)
        
    bci_udp.close()
    return "go_to_menu"
