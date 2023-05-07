from random import randint


def show_tab(tab):
    for v in tab:
        print(v)
    print("")

def is_between(a, i, j):
    if a >= i and a < j:
        return True
    return False

class Board:
    def __init__(self, diff, hard):
        self.width = hard[diff][0][0]
        self.height = hard[diff][0][1]
        self.nb_mines = hard[diff][1]
        self.diff = diff
        self.tab = self.create_tab()
        self.tab_n = self.create_tab_n()
        
    
    def is_mine(self, x, y):
        if self.tab[y][x] == "m":
            return True
        return False
    
    def create_empty_tab(self):
        t = [["" for i in range(self.width)] for j in range(self.height)]
        return t
    
    def create_tab(self):
        t = self.create_empty_tab()
        c = 0
        while c < self.nb_mines:
            x = randint(0, self.width) - 1
            y = randint(0, self.height - 1)
            
            if t[y][x] == "":
                t[y][x] = "m"
                c += 1
        return t
    
    def nb_mines_around(self, x, y):
        nb = 0
        for i in range(y - 1, y + 2):
            for j in range(x - 1, x + 2):
                if is_between(i, 0, self.width) and is_between(j, 0, self.height):
                    if self.tab[i][j] == "m":
                        nb += 1
        if nb == 0:
            nb = ""
        return nb
    
    def create_tab_n(self):
        t = self.create_empty_tab()
        for i in range(self.width):
            for j in range(self.height):
                t[i][j] = self.nb_mines_around(j, i)
                if self.tab[i][j] == "m":
                    t[i][j] = "m"
        
        return t
