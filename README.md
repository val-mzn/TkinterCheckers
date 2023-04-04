#TkinterCheckers
## Intro
TkinterCheckers est une interface en Tkinter pour jouer à un jeu de dames simplifié, développée dans le cadre d'un TP à l'EPSI en 3ème année. Dans cette version, les pions ne peuvent faire qu'une seule prise à la fois, et les dames ne peuvent se déplacer que d'un seul case.

## Mode de jeu
Le jeu peut être joué en local entre deux joueurs, contre l'ordinateur, ou en regardant deux ordinateurs jouer l'un contre l'autre.

## Lancer le jeu
Pour lancer l'interface, il suffit de cloner le dépôt et d'exécuter le fichier interface.py avec Python (py interface.py). Pour modifier la difficulté de l'ordinateur (profondeur) ou la taille du plateau, vous pouvez changer les valeurs dans le fichier constant.py.

## Focntionnement IA
L'IA utilise l'algorithme minimax (voir : https://fr.wikipedia.org/wiki/Algorithme_minimax) pour choisir le meilleur score parmi toutes les possibilités. Elle suppose que l'adversaire joue également le meilleur coup possible. Afin de limiter les calculs, l'IA effectue également une élagage en utilisant l'algorithme alpha-beta pruning pour ne pas calculer des coups qui ne servent à rien.
