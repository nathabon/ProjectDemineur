# Démineur

## Objectif 
Le but de ce projet est de créer un jeu de Démineur

Ce projet a été réalisé en Python, en utilisant la PO (*programmation orrientée objet*).


## Fonctionnalités
Le jeu permet de placer des drapeaux (clic gauche), découvrir des cases (clic droit), faire les deux en même temps (clic molette). 


## Modules utilisés
- *Pygame* afficher le jeu, gérer les interactions utilisateurs...
- *random* pour placer aléatoirement les mines



## Les classes
### Board
Cette classe permet génerer les tableaux avec les mines, et le nombre de mines à proximités pour chaque case.

**Principaux atributs** :

- *nb_mines* : (donné lors de l'initialisation de la classe) nombre de mines dans un tableau
- *width* : largeur du tableau
- *height* : longueur du tableau
- *tab* : tableau de tableau avec les mines
- *tab_n* : tableau de tableau avec le nombre de mines à proximités pour chaque case

**Principales méthodes**

- `create_tab(self)` : crée un tableau avec les mines placées aléatoirement
- `create_tab_n(self)` : crée un tableau avec le nombre de mines à proximités pour chaque case


### Play
Cette classe permet de gérer l'affichage et les interaction utilisateurs

**Principaux atributs** :
- les mêmes que ceux de la classe `Board`
- ceux relatifs à la bonne utilisation de *pygame* (font, images...)
- toutes les vérification pour la victoires, si la fenêtre est quitée...


**Principales mathodes**
- `reveal(self, x, y)` : fonction récursive, qui permet de révéler toutes les cases autour de la case où l'utilisateur a cliqué
- `add_score(self)` : fonction qui permet de sauvegarder le score de l'utilisateur dans un fichier texte
- `show_all(self, display = False)` : fonction qui affiche sur une fenêtre les chiffres, les drapeux, ou le reste s'il y a rien
- `play(self)` : fonction principale qui analyse les interactions de l'utilisateur, et qui réagi en conséquence


## Captures d'écran
![all](https://github.com/nathabon/Projects/blob/main/Démineur/images/all.png)

*Fenêtre apparant lors du lancement du programme.*

![clic middle](https://github.com/nathabon/Projects/blob/main/Démineur/images/clic-middle.png)

*Apparence si l'utilisateur clic sur la case (8, 5)*

![lose case](https://github.com/nathabon/Projects/blob/main/Démineur/images/lose-case.png)

*Apparence si l'utilisateur clic sur une mine, pendant 2 secondes*

![lose screen](https://github.com/nathabon/Projects/blob/main/Démineur/images/lose-screen.png)

*Apparence après que l'utilisateur ait perdu*

![win screen](https://github.com/nathabon/Projects/blob/main/Démineur/images/win-screen.png)

*Apparence si l'utilisateur gagne*


## Difficultées rencontrées
- Création et arret de la fonction récursive


## Améliorations possibles
- Améliorer l'apparence
