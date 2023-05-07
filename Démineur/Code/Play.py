import Board as bd
import pygame, time, math, platform, exception

def clean(tab):
    for i, e in enumerate(tab):
        for j, v in enumerate(tab):
            if e == v and i != j:
                del tab[j]
    return tab

def color(n):
    c = (0, 0, 0)

    if n == "1":
        c = (0, 150, 0) 
    elif n == "2":
        c = (0, 0, 200) 
    elif n == "3":
        c = (200, 0, 0)
    elif n == "4":
        c = (10, 10, 10)
    return c

def exist_in(v, tab, indi = False):
    if not indi:
        for i in tab:
            if v == i:
                return True
    else:
        for i, e in enumerate(tab):
            if e == v:
                return i, True 
    return False



class Demin:
    """
    Pour jouer, faire : '
    game = Demin(ici le dificulté voulue, 0, 1 ou 2)
    game.play()'
    Les modules pygame, time, math, platform, exception et le fichier Board sont requis.
    
    Pour jouer:
     - Appuyer sur le clic gauche pour révéler les cases
     - Appuyer sur le clic molette pour révéler les cases autour d'un nombre si tous les drapeaux on étés posés
     - Appuyer sur le clic droit pour poser un drapeau
    """
    
    def __init__(self, diff):
        self.hard = [[(10, 10), 10, 50], [(16, 16), 40, 40], [(20, 20), 50, 40]]
        self.diff = diff
        self.board = bd.Board(self.diff, self.hard)
        self.tab = self.board.tab
        self.tab_n = self.board.tab_n
        self.tab_suspect = self.board.create_empty_tab()
        self.tab_discorver = self.board.create_empty_tab()
        
        self.pixels = self.hard[self.diff][2]
        self.nb_font_size = round(self.pixels * 0.9)
        self.nb_font_size_sub = round(self.pixels * 0.6)
        self.win_font_size_sub = 30
        self.lose_font_size = 70
        self.win_font_size = 50
    
    def initPygame(self):
        """
        Initialise tous les modules et paramètres propre à Pygame
        """
        
        pygame.init()
        self.window = pygame.display.set_mode((len(self.tab[0]) * self.pixels - 2, len(self.tab) * self.pixels - 2))
        pygame.display.set_caption("Démineur")

        self.nb_font = pygame.font.SysFont(None, self.nb_font_size)
        self.lose_font = pygame.font.SysFont(None, self.lose_font_size)
        self.lose_font_sub = pygame.font.SysFont(None, self.nb_font_size_sub)
        self.win_font = pygame.font.SysFont(None, self.win_font_size)
        self.win_font_sub = pygame.font.SysFont(None, self.win_font_size_sub)

        self.platform = platform.system()
        if self.platform == "Windows":
            self.flag_path = "flag_icon.png"
            self.mine_path = "mine.png"

        elif self.platform == "Darwin":
            self.flag_path = "/Volumes/BONTOUX/1ere B/Numeriques et Sciences Informatiques/Projets/2 - Démineur/flag_icon.png"
            self.mine_path = "/Volumes/BONTOUX/1ere B/Numeriques et Sciences Informatiques/Projets/2 - Démineur/mine.png"
        else:
            print("Platform system cannot be determined")
            raise exception.InvalidPlatformSystem(self.platform)
        

        self.flag = pygame.image.load(self.flag_path).convert_alpha()
        self.flag = pygame.transform.scale(self.flag, (round(self.pixels * 0.9), round(self.pixels * 0.9)))


        self.mine = pygame.image.load(self.mine_path).convert_alpha()
        self.mine = pygame.transform.scale(self.mine, (round(self.pixels * 0.9), round(self.pixels * 0.9)))
    
    def initGameRules(self):
        """
        Initialise tous les paramètres propre au jeu selon les règles
        """
        
        self.quite = False
        self.first_play = True
        self.is_playing = True
        self.is_god_mod = False
        self.has_god_mod = False
        self.debug = False
        self.has_lose = False
        self.has_win = False
        self.nb_suspect = 0
        self.nb_good = 0
        self.time_aft = 0
        self.score = 0
        self.mid_discover = []
        self.lose_p = ()
    
    def init(self):
        """
        Exécute les méthodes 'self.initPygame' et 'self.initGameRules'
        """
        
        self.initPygame()
        self.initGameRules()
    
    def replay(self):
        print("Partie recommencée")
        self.__init__(self.diff)
        self.init()

    def posi(self, l, c):
        """
        Renvoi la position voulue pour les lignes
        """
        
        return (c * self.pixels, l * self.pixels, self.pixels - 2, self.pixels - 2)
    
    def posia(self, l, c):
        """
        Renvoi la position voulue pour les cases
        """
        
        return (c * self.pixels + 2, l * self.pixels + 2, self.pixels - 2, self.pixels - 2)
    
    def quit(self):
        self.quite = True
        self.is_playing = False
        self.has_lose = False
        self.has_win = False
        print("Partie stopée")

    def lose(self):
        print("Vous avez perdu ! Appuyez sur 'R' pour recommencer une partie.")
        self.is_playing = False
        self.has_lose = True
    
    
    def suspected_around(self, x, y):
        """
        Renvoi le nombre de drapeau autour d'une case
        """
        
        s = 0
        for i in range(-1 + y, 2 + y):
            for j in range(-1 + x, 2 + x):
                if (0 <= i < len(self.tab[0]) and 0 <= j < len(self.tab)) and self.tab_suspect[i][j] == "s":
                    s += 1
        return s
    

    def add_suspected(self, x, y):
        """
        Switch en drapeau et non-drapeau pour une case
        """
        
        if self.tab_suspect[y][x] == "s":
            self.tab_suspect[y][x] = ""
            self.nb_suspect -= 1
        else:
            self.tab_suspect[y][x] = "s"
            self.nb_suspect += 1
            print(f"Vous avez découvert {self.nb_suspect} mines sur {self.hard[self.diff][1]}. Il vous en restes donc {self.hard[self.diff][1] - self.nb_suspect} à découvrir.")
    

    def add_discover(self, tab):
        """
        Met une case en gris
        """
        
        for v in tab:
            self.tab_discorver[v[0]][v[1]] = "d"
    


    def reveal(self, x, y):
        """
        Renvoi toutes les cases à révéler (fonction récursive)
        """
        
        if not (0 <= x < len(self.tab[0]) and 0 <= y < len(self.tab)): # Si pas dans le tableau
            return []

        if (y, x) in self.mid_discover: # Si déjà découvert
            return []

        self.mid_discover.append((y, x))

        revealed = [(y, x)]

        if self.tab_n[y][x] == "":
            for i in range(y - 1, y + 2):
                for j in range(x - 1, x + 2):
                    if i != y or j != x:
                        revealed.extend(self.reveal(j, i))
                        

        return revealed
    
    def reveal_all(self, x, y):
        if self.suspected_around(x, y) == self.tab_n[y][x]:
            for i in range(-1 + y, 2 + y):
                for j in range(-1 + x, 2 + x):
                    if (0 <= i < len(self.tab[0]) and 0 <= j < len(self.tab)) and self.tab_suspect[i][j] != "s":
                        self.user_clic(j, i)

    
    def x_ray(self):
        """
        Découvre toutes les cases et montre les bombes. Méthode non-réversible
        """
        
        for i in self.tab_discorver:
            for v in range(len(i)):
                i[v] = "d"
        self.is_god_mod = True
    
    
    def user_clic(self, colonne, ligne):
        """
        Simule un clic utilisateur pour une case
        """
        
        self.start.append(time.time())
        if self.board.is_mine(colonne, ligne):
            self.lose_p = (ligne, colonne)
            self.lose()
        r = self.reveal(colonne, ligne)
        self.add_discover(r)
    
    def add_score(self):
        """
        Ajoute le score dans le fichier correspondant au niveau de difficulté. Si il y a une erreur, affiche le score.
        """
        
        time = self.time_aft
        diff = self.diff

        try:
            fName = f"score{diff}.txt"  
            with open(fName, "r") as f:
                txt = f.read()
                txtL = txt.split("\n")
                txtL = [float(v) for v in txtL]

                f.close()

            txtL.append(float(time))
            txtL.sort()
            txt = ""
            for i in range(len(txtL)):
                txt += f"{txtL[i]}\n"
            txt = txt[:-1]

            with open(fName, "w") as f:
                f.write(txt)
            
            ind = None
            with open(fName, "r") as f:
                txt = f.read()
                txtL = txt.split("\n")
                for i in range(len(txtL)):
                    if txtL[i]== str(time):
                        ind = i + 1
        except :
            print(f"Votre score n'a pas pu être enregistré, vous avez fait {time}")

        return ind

    def show_empty(self):
        """
        Affiche une fenêtre avec dun quadrillage vide
        """
        
        for l in range(len(self.tab)):
            for c in range(len(self.tab[l])):
                pygame.draw.rect(self.window, (10, 200, 10), self.posi(l,c))

        

    def show_all(self, display = False):
        """
        Affiche une fenêtre avec les drapeaux, les nombres, et les mines si 'Display' est True
        """
        
        self.show_empty()
        for l in range(len(self.tab)):
            for c in range(len(self.tab[l])):
                
                
                if self.tab_discorver[l][c] == "d":
                    pygame.draw.rect(self.window, (200, 200, 200), self.posi(l,c))

                    # Afficher le nombre de mines à coté
                    txt = self.tab_n[l][c]
                    if isinstance(txt, int):
                        txt = str(txt)
                    else:
                        txt = ""
                    nb = self.nb_font.render(txt, True, color(txt))
                    pos = (c * self.pixels + self.pixels // 4, l * self.pixels + self.pixels // 4)
                    self.window.blit(nb, pos)
                    
                
                # Afficher flag si suspected
                elif self.tab_suspect[l][c] == "s":
                    self.window.blit(self.flag, self.posia(l,c))
                
                if self.has_lose and self.lose_p == (l, c):
                    pygame.draw.rect(self.window, (255, 0, 0), self.posi(l,c))
                
                # Afficher case noire si GOD MOD
                if self.tab[l][c] == "m" and display:
                    self.window.blit(self.mine, self.posia(l,c))
                    
                
        pygame.display.update()

    def lose_screen(self):
        """
        Affiche la fenêtre si l'utilisateur perd 
        """
        
        for l in range(len(self.tab)):
            for c in range(len(self.tab[l])):
                pygame.draw.rect(self.window, (255, 255, 255), self.posi(l,c))
                
                # Afficher case noire 
                pygame.draw.rect(self.window, (10, 10, 10), self.posi(l,c))
                
                txt = "Vous avez perdu"
                texte = self.lose_font.render(txt, True, (255, 0, 0))
                self.window.blit(texte, ((len(self.tab) // 6 * self.pixels), (len(self.tab) // 7 * 4 * self.pixels)))
                
                if self.nb_suspect == self.board.nb_mines:
                    txt = "Car vous avez mal placé vos drapeaux"
                    texte = self.lose_font_sub.render(txt, True, (255, 0, 0))
                    self.window.blit(texte, ((len(self.tab) // 6 * self.pixels), (len(self.tab) // 7 * 6 * self.pixels)))
                else:
                    txt = "Car vous avez appuyé sur une bombe"
                    texte = self.lose_font_sub.render(txt, True, (255, 0, 0))
                    self.window.blit(texte, ((len(self.tab) // 6 * self.pixels), (len(self.tab) // 7 * 6 * self.pixels)))

                txt = "Appuyez sur 'r' pour recommencer"
                texte = self.lose_font_sub.render(txt, True, (255, 0, 0))
                self.window.blit(texte, ((len(self.tab) // 6 * self.pixels), (len(self.tab) // 7 * 8 * self.pixels)))
                
                
                    
        pygame.display.update()
    
    def win_screen(self):
        """
        Affiche la fenêtre si l'utilisateur gagne 
        """
        
        for l in range(len(self.tab)):
            for c in range(len(self.tab[l])):
                pygame.draw.rect(self.window, (255, 255, 255), self.posi(l,c))
                
                # Afficher case noire 
                pygame.draw.rect(self.window, (10, 10, 10), self.posi(l,c))
                
                txt = "Bravo, vous avez gagné !"
                texte = self.win_font.render(txt, True, (0, 200, 0))
                self.window.blit(texte, ((len(self.tab) // 6 * self.pixels), (len(self.tab) // 7 * 4 * self.pixels)))
                
                txt = f"Temps : {int(self.time_aft // 60)} minutes et {round(self.time_aft % 60)} secondes"
                texte = self.win_font_sub.render(txt, True, (0, 200, 0))
                self.window.blit(texte, ((len(self.tab) // 6 * self.pixels), (len(self.tab) // 7 * 6 * self.pixels)))
                
                txt = f"pour découvrir {self.board.nb_mines} mines ! "
                texte = self.win_font_sub.render(txt, True, (0, 200, 0))
                self.window.blit(texte, ((len(self.tab) // 6 * self.pixels), (len(self.tab) // 7 * 7 * self.pixels)))

                if (not self.has_god_mod) or self.debug:
                    txt = f"Vous êtes classé {self.score} ème"
                else:
                    txt = "Vous avez triché !"
                texte = self.win_font_sub.render(txt, True, (0, 200, 0))
                self.window.blit(texte, ((len(self.tab) // 6 * self.pixels), (len(self.tab) // 7 * 8 * self.pixels)))

                txt = "Appuyez sur 'r' pour recommencer"
                texte = self.lose_font_sub.render(txt, True, (0, 200, 0))
                self.window.blit(texte, ((len(self.tab) // 6 * self.pixels), (len(self.tab) // 7 * 2 * self.pixels)))
        
        pygame.display.update()
    
    
    def play(self):
        """
        Fonction principale, qui enregistre le temps, et qui réagit eux interaction utilisateur
        """
        
        self.init()
        print("Partie commencée")
        while not self.quite:

            self.start = []
            while self.is_playing and self.nb_suspect != self.hard[self.diff][1]:
                self.show_all(self.is_god_mod)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT: #Pour fermer l'application
                        self.quit()
                    
                    if event.type == pygame.KEYDOWN: # Appuyer sur clavier
                        if event.key == 114: # Rejouer 'r'
                            self.replay()
                        
                        if event.key == pygame.K_UP:
                            self.is_god_mod = not self.is_god_mod
                            self.has_god_mod = True
                            print("Vous trichez ...")
                        
                        if event.key == pygame.K_DOWN:
                            self.x_ray()
                            self.has_god_mod = True
                            print("Vous trichez ...")
                        
                        if event.key == pygame.K_LEFT:
                            self.debug = True
                            print("DEBUG ON")

                    if event.type == pygame.MOUSEBUTTONDOWN: # Appuyer sur un bouton de le souris
                        ligne = event.pos[1] // self.pixels
                        colonne = event.pos[0] // self.pixels
                        a = (ligne, colonne)

                        if event.button == 1: # Clic gauche
                            self.user_clic(colonne, ligne)
                        
                        if event.button == 3: # Clic droit
                            self.start.append(time.time())
                            self.add_suspected(colonne, ligne)
                        
                        if event.button == 2: #Bouton du scroll
                            self.reveal_all(colonne, ligne)
                

                self.show_all(self.is_god_mod)
                end = time.time()
            
            # All flag
            self.time_aft = end - self.start[0]
            if self.nb_suspect == self.board.nb_mines:
                for i in range(len(self.tab)):
                    for j in range(len(self.tab[i])):
                        if self.tab[i][j] == "m" and self.tab_suspect[i][j] == "s":
                            self.nb_good += 1  
                        else:
                            self.has_lose = True

                if self.nb_good == self.board.nb_mines:
                    self.has_win = True
                    self.has_lose = False
                else:
                    self.has_lose = True
            


            while self.has_lose:
                self.x_ray()
                self.show_all(self.is_god_mod)
                time.sleep(2)
                while self.has_lose:
                    self.lose_screen()
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT: #Pour fermer l'application
                            self.quit()
                        
                        if event.type == pygame.KEYDOWN: # Appuyer sur clavier
                            if event.key == 114: # Rejouer 'r'
                                self.replay()

            if self.has_win and (not self.has_god_mod or self.debug):
                self.score = self.add_score()

            while self.has_win:
                self.win_screen()
                for event in pygame.event.get():
                        if event.type == pygame.QUIT: #Pour fermer l'application
                            self.quit()
                        
                        if event.type == pygame.KEYDOWN: # Appuyer sur clavier
                            if event.key == 114: # Rejouer 'r'
                                self.replay()
        pygame.quit()

if __name__ == "__main__":
    diff = 0
    game = Demin(diff)
    game.play()