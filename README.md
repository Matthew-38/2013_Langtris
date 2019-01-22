# 2013_Langtris
Un petit jeu de Tetris avec des lettres pour apprendre de la vocabulaire cible

# Contexte

C'est un petit jeu, pas fini, que j'ai crée avec Python en utilisant Pygame. Le but est de construire des mots à partir des lettres qui tombent en les utilisant dans des combinaisons logiques. Chaque mot construit disparaît, laissant de la place pour des autres - comme dans le jeu de Tetris. Les mots possible sont limités à ceux qui se trouvent dans la dictionnaire annexe. À fin d'optimiser les chances, les lettres qui tombent corresponds en sorte et fréquence à ceux qui se trouve dans les mots fournis dans ce fichier.

# Usage
Lorsque la programme lance avec Python 2, ce dernier ne marche pas correctemment avec les accents sur les lettres en français (ascii-unicode bug). Donc dans le fichier testdict.txt, je n'ai pas mis des accents. 

Si vous voulez l'utiliser avec les accents, il vaut mieux la lancer en Python 3. Pour ce faire, il faut avoir pygame installé. Si vous utiliser Linux, vous pouvez trouver des instructions pour ce faire sur ce forum (dernière réponse pour Linux 18) : https://askubuntu.com/questions/401342/how-to-download-pygame-in-python3-3

Vous pouvez changer les mots cibles dans le fichier testdict.txt, et les paramettres (vitesse, nombre de lettres au début etc) dans settings.ini

# Conclusion

Ce jeu est juste un petit projet. Faites ce que vous voulez avec le code. 
