import cv2 as cv
import time as tm
from datetime import datetime
from math import *
import sys
import serial
from serial.tools import list_ports

cap = cv.VideoCapture (0)  # Capture de la caméra
_, frame = cap.read()


hauteur_cap, largeur_cap, canaux_cap = frame.shape
print(f"L'image comporte {hauteur_cap} pixels en hauteur et {largeur_cap} pixels en largeur")

def blanc(i, j, frame): #Test de si on est sur un pixel avec une nuance de blanc
    if (frame.item(i, j, 2) >= 230) and (frame.item(i, j, 1) >= 230) and (frame.item(i, j, 0) >= 230):
        return True
    return False


def rouge(i, j, frame): #Test de si on est sur un pixel avec une nuance de rouge
    if (frame.item(i, j, 2) >= 200) and (frame.item(i, j, 1) >= 30) and (frame.item(i, j, 0) >= 30):
        return True
    return False


def etape1_seuillage(h, l, frame):
    """
    h : hauteur en pixel de l'image capturée par la caméra USB
    l : largeur en pixel de l'image capturée par la caméra USB
    frame : objet représentatif de l'image capturée par la caméra USB
    Renvoie un objet représentatif de l'image maintenant en noir et blanc
    """
    for i in range(h):
        for j in range(l//2):
            if blanc(i, j, frame): #Test de si on est sur un pixel avec une nuance de blanc ou de rouge si laser moins fort
                frame.itemset((i, j, 2), 255)
                frame.itemset((i, j, 1), 255)
                frame.itemset((i, j, 0), 255)
            else:
                frame.itemset((i, j, 2), 0)
                frame.itemset((i, j, 1), 0)
                frame.itemset((i, j, 0), 0)
        for k in range(l//2, l):
            frame.itemset((i, k, 2), 0)
            frame.itemset((i, k, 1), 0)
            frame.itemset((i, k, 0), 0)
               
    return frame


def etape2_desepaisse(h, l, frame, pscan):
    """
    h : hauteur en pixel de l'image capturée par la caméra USB
    l : largeur en pixel de l'image capturée par la caméra USB
    frame : objet représentatif de l'image capturée par la caméra USB, necesite le module opencv 2
    Renvoie un objet représentatif de l'image maintenant désépaissie
    """
    t = 0
    before = False
    for i in range(h):
        before = False 
        t = 0
        if i % pscan != 0:  #Si on veut scanner que pscan % des pixels, on vérifie si on est sur un dex pixels que l'on ne veut pas scanner, et on met tout en noir
            for x in range(l//2):
                frame.itemset((i, x, 0), 0)
                frame.itemset((i, x, 1), 0)
                frame.itemset((i, x, 2), 0)
        for j in range(l//2):
            if (frame.item(i, j, 2) >= 255) and (frame.item(i, j, 1) >= 255) and (frame.item(i, j, 0) >= 255): #Test de si on est sur un pixel blanc
                t += 1
            elif t > 0: #Test de si on est sur un pixel noir, si il n'y a pas eu de pixel noir isolé et qu'il y a eu du blanc juste avant
                before = True 
                tpr = ceil(t / 2) #Arrondi t au supérieur, donc le seul pixel blanc sera au milieu-droite si t est pair
                for k in range(1, t):
                    if k != tpr: #Test de si on est pas au milieu de la ligne de pixel
                        frame.itemset((i, j-k, 0), 0)
                        frame.itemset((i, j-k, 1), 0)
                        frame.itemset((i, j-k, 2), 0)
            elif before :
                before = False 
                break
    
    return frame

def calculs_coord(x, y, Lp, lp, Beta):
    """
    x : coordonée du pixel sur l'axe x
    y : coordonée du pixel sur l'axe y
    Lp : largeur (ou hauteur) de l'image
    lp : longeur de l'image
    Beta : angle de la rotation actuelle
    
    Renvoie une liste de coordonées 3D x, y et z de chque pixels blanc 
    """
    xcentre = lp//2 - x
    h = Lp - y
    p = xcentre / sin(325)
    Z3D = h
    X3D = p * cos(Beta)
    Y3D = p * sin(Beta)
    pixels = [X3D, Y3D, Z3D]
    
    return pixels


def etape4_coord3D(Lp, lp, frame, Beta):
    """
    Lp : largeur (ou hauteur) de l'image
    lp : longeur de l'image
    frame : objet représentatif de l'image capturée par la caméra USB, necesite le module opencv
    Beta : angle de la rotation actuelle
    """
    pixels = []
    coord = []
    for i in range(Lp):
        for j in range(lp//2):
            if (frame.item(i, j, 2) >= 255) and (frame.item(i, j, 1) >= 255) and (frame.item(i, j, 0) >= 255): #Test de si on est sur un pixel blanc
                pixels = calculs_coord(j, i, Lp, lp, Beta)
                coord.append(pixels)
    return coord
            
datet = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
name = input("Comment voulez-vous appeler votre fichier .ply ? ")
if name == "":
    Fname = f"fichiers_ply\{datet}.ply"
else:
    Fname = f"fichiers_ply\{name}.ply"

pscan = input("Combien de % des pixels voulez-vous scanner ? ")
if pscan == "":
    pscan = 2
else:
    pscan = int(round(100 / int(pscan)))

def main(frame, pscan):
    ser = serial.Serial('COM8')
    angleObjet = 0
    coord = []
    rota = 0
    while angleObjet < 360: #Simulation de la rotation de l'objet*
        angleObjet = 0.7 * rota
        _, frame = cap.read()
        etape1_seuillage(hauteur_cap, largeur_cap, frame)
        etape2_desepaisse(hauteur_cap, largeur_cap, frame, pscan)
        pixels = etape4_coord3D(hauteur_cap, largeur_cap, frame, angleObjet)
        cv.imshow("frame", frame)
        coord.append(pixels)
        
        nbrota = 4
        ser.write(b'foot 2')
        
        rota += nbrota
        
        scan = round((angleObjet/360) * 100, 1)
        print(f"Scan effectué à {scan} %")
        
        if cv.waitKey(1) == ord('q'):
            break   

    print("Rotation de l'objet fini ou interrompu.")

    ser.close()
    cv.destroyAllWindows()
    cap.release()
    
    return coord, angleObjet

coord, angleObjet = main(frame, pscan)

long = 0
for i in range(len(coord)):
    long += len(coord[i])

if angleObjet >= 350:
    debutFile = f"ply\nformat ascii 1.0\nelement vertex {long}\nproperty float x\nproperty float y\nproperty float z\nend_header\n"
    with open(Fname, "w") as file:
        file.write(debutFile)
        for i in range(len(coord)):
            for j in range(len(coord[i])):
                for k in range(3):
                    file.write(str(coord[i][j][k]))
                    file.write(" ")
                file.write("\n")
    print(f"Enregistrement du fichier .ply à l'emplacement \"{Fname}\" résussi ")
else:
    rep = input(f"Voulez-vous enregistrer le fichier ply sous le nom '{Fname}' ? (o/n)")
    if rep == "o":
        debutFile = f"ply\nformat ascii 1.0\nelement vertex {long}\nproperty float x\nproperty float y\nproperty float z\nend_header\n"
        with open(Fname, "w") as file:
            file.write(debutFile)
            for i in range(len(coord)):
                for j in range(len(coord[i])):
                    for k in range(3):
                        file.write(str(coord[i][j][k]))
                        file.write(" ")
                    file.write("\n")
