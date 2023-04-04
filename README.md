# TkinterCheckers
## Explication
Cette interface en Tkinter pour jouer a un jeu de dames simplifier a été réaliser dans le cadre d'un TP a l'EPSI en "eme année.
Pour simplifier les pion ne peuvent fair qu'une prise par tout et les dames ne peuvent se déplacer que d'un casse.

## Mode je jeu
Possibilité de jouer a deux joueur en local; contre l'ordinateur ou regarder deux ordinateur jouer l'un contre l'autre.

## Lancer
Pour lancer l'interface il suffit de cloner le repot et d'executer interface.py ```(python interface.py / py interface.py)```
Pour changer la difficulté de l'ordinateur ou la taille du plateau vous pouvez changer les valeurs dans constant.py

## IA
L'ia choisie le meilleurs un score pour toutes les possibilité, elle pars du principe que l'adverse réalise lui aussi le meilleurs coup possible (Algorithme minimax voir: https://fr.wikipedia.org/wiki/Algorithme_minimax)
Pour limiter les calcule l'IA fait aussi un élagage pour ne pas calculer des coups qui ne servent a rien (Alpha-beta prunning)
