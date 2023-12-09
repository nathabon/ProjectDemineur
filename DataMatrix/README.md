# Data Matrix


## Objectif 
Le but de ce projet est de créer un DataMatrix (comme un QR code) de 10x10 à partir d'une chaîne de caractères de longueur 3. Pour lire ce DataMatrix, il faut avoir une application installée, la lecture de Datamatrix n'étant pas possible nativement sur la plupart des téléphones.

Ce projet a été réalisé en Python, [sans utiliser la PO](https://github.com/nathabon/Projects/blob/main/DataMatrix/README.md#améliorations-possibles) (*programmation orrientée objet*), n'étant pas à l'aise avec ce concept à ce moment là (début novembre 2022).


## Fonctionnalités
Le programme (version console en .exe & version en .py) ne demande qu'une chaîne de 3 caractères, et montre une fenêtre avec le DataMatrix à scanner, fait avec le module *turtle*.

Le programme ne prend que des caractères dans la table ASCII (0-9, a-z, A-Z, ...).

## Modules utilisés
- *Turtle* pour afficher le Datamatrix
- *reed-solomon* pour déterminer les octets de de correction


## Captures d'écran
![Invite de comande](https://github.com/nathabon/Projects/blob/main/DataMatrix/screenshot/cmd.png)

*Fenêtre apparant dans le cmd lors du lancement du .exe*

![Fenêtre](https://github.com/nathabon/Projects/blob/main/DataMatrix/screenshot/turtle.png)

*Fenêtre apparant lors de l'éxécution du code après avoir donné la chaîne de caractères. [Le DataMatrix met quelques secondes à se créer](https://github.com/nathabon/Projects/blob/main/DataMatrix/README.md#améliorations-possibles).*

![Datamatrix](https://github.com/nathabon/Projects/blob/main/DataMatrix/screenshot/datamatrix.png)

*DataMatrix crée pour le chaîne de caractère* abc *.*


## Difficultées rencontrées
- Interdiction d'utiliser des fonction natives de Python (comme `bin`),
- Novice en Python
- Utilisation imcomprise de l'algorithme *Reed-Solomon* pour avoir les 5 octets de vérification sur les 8,


## Améliorations possibles
- Adapter le code pour toutes les longueures de caractères,
- Utiliser la PO (*programmation orrientée objet*) avec les classes,
- Ajouter des commentaires et des documentations pour mieux comprendre le code,
- Essayer de comprendre l'algorithme *Reed-Solomon*,
