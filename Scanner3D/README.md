# Scanner 3D

## Objectif 
Le but de ce projet est de créer un fichier 3D en .ply compatible avec le standard *PLY*, à partir d'un objet. Pour lire ce fichier 3D, il est conseillé d'utiliser le logiciel [Meshlab](https://www.meshlab.net/).

Ce projet a été réalisé en Python, [sans utiliser la PO](https://github.com/nathabon/Projects/blob/main/Scanner3D/README.md#améliorations-possibles) (*programmation orrientée objet*), n'étant pas à l'aise avec ce concept à ce moment là (début décembre 2022).


## Fonctionnalités
Pour utiliser ce code, il faut un équipement particulier et configuré pour le programme :

- une caméra USB
- un laser permettant d'éclairer le profil de l'objet scanné
- une boite pour limiter la lumière
- une carte électronique MycroPython Pyboard

![setup scanner](https://github.com/nathabon/Projects/tree/main/Scanner3D/screenshot/setup_scanner.jpg)

## Modules utilisés
- *Opencv* pour recevoir les images de la caméra
- *Pyb* pour faire tourner les moteurs sur la carte Pyboard
- *serial* pour se connecter à la carte Pyboard avec les ports USB
- *time* pour les différents besion de temps et d'attente pour le focus
- *math* pour calculer les position dans un plan (x, y, z) à partir de l'image


## Différentes étapes
- Aquisition : récupérer l'image issu de la caméra
- Seuillage : seuiller le niveau de rouge pour séparer l'image du laser du reste
- Désépaississement : désépaissier la ligne de pixels du laser, pour n'avoir qu'un seul pixel par ligne
- Calculs : obtenir les coordonnées 3D à partir de l'image
- Génération du fichier : créer le fichier .ply d'après les coordonnées 3D 


## Captures d'écran
![Aquisition](https://github.com/nathabon/Projects/blob/main/Scanner3D/screenshot/aquisition.jpg)

*Fenêtre apparant lors de l'aquisition de l'image. [La video est en quelques FPS](https://github.com/nathabon/Projects/blob/main/Scanner3D/README.md#améliorations-possibles).*

![Fenêtre](https://github.com/nathabon/Projects/blob/main/Scanner3D/screenshot/image3d.png)

*Fenêtre du logiciel Meshlab après la scan d'un verre.*


## Difficultées rencontrées
- Gérer les tableux relatifs à l'image
- Essayer d'optimiser la rapidité de l'image


## Améliorations possibles
- Utiliser la PO (*programmation orrientée objet*) avec les classes,
- Code très peu optimisé, utiliser le module *numpy* pour gérer plus rapidement les tableaux des images
