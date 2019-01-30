# Langtris - A tetris inspired language game using Pygame
This is an unfinished Tetris style game for learning vocabulary/spelling.

# Background

This is a small, unfinished game that I made in Python using Pygame. The goal is to construct words from the letters which fall, by placing them in logical order. Each word constructed disappears, leaving place for others - just like in Tetris. The possible words are limited to those supplied in the dictionary file. In order to optimise the matches, the letters that fall in the game correspond to the letters and their frequency in the words supplied in that file. For compatability, accents are not used in the supplied dictionary (see below).

# Usage
If launched with Python 2, this game will not work correctly with non-standard ASCII characters (é, ê, à and so on are not accepted). So, in the file "testdict.txt", they are removed from the French words supplied. If you want to use it with accents, launch it with Python 3. For this, you must have Pygame installed. If you use Linux, you can find instructions for installing Pygame on this forum (last answer for Linux 18): https://askubuntu.com/questions/401342/how-to-download-pygame-in-python3-3

You can change the target words in the file "testdict.txt", and the settings (speed, number of letters at the start, etc) in the "settings.ini" file.

# Conclusion

This game is just a little project. It was useful for testing the concept (and learning Pygame), but I don't intend to develop it further. Do what you want with the code.

[Version Française en bas]

##################################################################################################

# Version Française

# 2013_Langtris
Un petit jeu de Tetris avec des lettres pour apprendre de la vocabulaire cible

# Contexte

C'est un petit jeu, pas fini, que j'ai crée avec Python en utilisant Pygame. Le but est de construire des mots à partir des lettres qui tombent en les utilisant dans des combinaisons logiques. Chaque mot construit disparaît, laissant de la place pour des autres - comme dans le jeu de Tetris. Les mots possible sont limités à ceux qui se trouvent dans la dictionnaire annexe. À fin d'optimiser les chances, les lettres qui tombent corresponds en sorte et fréquence à ceux qui se trouve dans les mots fournis dans ce fichier.

# Usage
Lorsque la programme lance avec Python 2, ce dernier ne marche pas correctemment avec les accents sur les lettres en français (ascii-unicode bug). Donc dans le fichier testdict.txt, je n'ai pas mis des accents. 

Si vous voulez l'utiliser avec les accents, il vaut mieux la lancer en Python 3. Pour ce faire, il faut avoir pygame installé. Si vous utiliser Linux, vous pouvez trouver des instructions pour ce faire sur ce forum (dernière réponse pour Linux 18) : https://askubuntu.com/questions/401342/how-to-download-pygame-in-python3-3

Vous pouvez changer les mots cibles dans le fichier testdict.txt, et les paramettres (vitesse, nombre de lettres au début etc) dans "settings.ini"

# Conclusion

Ce jeu est juste un petit projet. Faites ce que vous voulez avec le code. 
