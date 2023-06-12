from turtle import *
from reedSalomon import reed_salomon

nb_Char = 3
nb_octets = nb_Char + 5
CodeWords = [0 for _ in range(nb_Char)]
CodeWords_bin = [0 for _ in range(nb_octets)]
tracer(2)

def dessine(t):
    for i in range(len(t)):
        for j in range(len(t[i])):
            if t[i][j] == 1:
                up()
                goto(30 * j, -30 * i)
                down()
                begin_fill()
                for _ in range(4):
                    forward(30)
                    left(90)
                end_fill()

def finder_pattern(t):
    ligne = [0] * (len(t) + 2)
    ligne = [0 for i in range(len(t) + 2)]
    for j in range(0, len(t) + 2, 2):
        ligne[j] = 1
    t.insert(0, ligne)
    for i in range(1, len(t)):
        t[i].insert(0, 1)
        if i % 2 == 1 :
            t[i].append(1)
    ligne = [1] * (len(t) + 1)
    t.append(ligne)

def binaire(nb):
    bin = []
    while nb >= 1:
        bin.insert(0, nb % 2)
        nb = nb // 2
    while len(bin) < 8:
        bin.insert(0, 0)
    return bin

pattern = [[21, 22, 36, 37, 38, 43, 44, 45],[23, 24, 25, 51, 52, 46, 47, 48], [26, 27, 28, 53, 54, 55, 11, 12],  [15, 61, 62, 56, 57, 58, 13, 14],[18, 63, 64, 65, 81, 82, 16, 17],[72, 66, 67, 68, 83, 84, 85, 71],[74, 75, 31, 32, 86, 87, 88, 73],[77, 78, 33, 34, 35, 41, 42, 76]]
DataMatrix = [i for i in pattern]
print("Quels sont les 3 caractères que vous voulez écrire ?")
Char = input()
for i in range(nb_Char):
    CodeWords[i] = ord(Char[i]) + 1
CodeWords += reed_salomon([CodeWords[0], CodeWords[1], CodeWords[2]])
for i in range(nb_octets):
    CodeWords_bin[i] = list(binaire(CodeWords[i]))
for i in range(nb_octets):
    for j in range(nb_octets):
        pos = pattern[i][j]
        pos_word = (pos // 10) - 1
        pos_bit = (pos % 10) - 1
        DataMatrix[i][j] = int(CodeWords_bin[pos_word][pos_bit])
finder_pattern(DataMatrix)
dessine(DataMatrix)