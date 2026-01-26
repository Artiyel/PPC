# Rapport PPC

## Notice d'utilisation IA
Alexis:
* debuggage du signal entre proie et env --> L'ia a apporté de l'aide pour comprendre les détails de la documentation, mais j'avais correctement compris 95% de la chose
* debuggage sur l'intiatlisation de la mémoire partagée qui représente l'état de l'herbe (normal/secheresse) --> la documentation était pas très explicite, j'essayait de faire passer une string dans une `multiprocessing.Value()` mais ce n'est apparement pas possible
* Debuggage général et check si erreur de logique que je n'avais pas vue --> repérage d'une erreur a la fermeture des connections, solution implémentée inspirée de la suggestion de l'ia
* beaucoup d'affichages d'erreures dans la console --> L'ia m'a renseigné sur la signification des messages d'erreur, j'ai pu aviser si il était pertinant de les afficher ou non

## Rapport
Notre projet comporte 5 fichier,les quatre classiques : `env.py` `proie.py` `predateur.py` `display.py` ainsi qu'une addition afin de simplifier `env.py` : `grass.py`.
Nous avons pris une approche que l'on pourrait décrire comme spéciale dans la conception de notre projet, c'est a dire que le code permettant l'accès a la mémoire partagée se trouve entièrement dans `env.py` mais que l'appel a ces différentes fonction se fait de manière asynchrone par différent thread gérant les sockets communiquant avec les individus présents dans la simulation. Nous reviendrons plus en détail sur ceci dans les parties suivantes.


## `env.py` 
* `main()`: Notre main gère la naissance de la première génération de proie et prédateurs, ainsi que l'initialisation du programme `grass.py` (qui reçoit l'addresse de la mémoire partagée). Chaque individu d'une espèce est un Process différent. (sauf herbe, il n'y a qu'un seul process Herbe)
  De plus, il initialise la communication par signaux, et gère les signaux qu'il serait suceptible de reçevoir (depuis le display par exemple)
  Le main initialise aussi la mémoire partagée qui sera utilisée par les autres programmes.
  Enfin, il y a une boucle dans le main qui, tant que la simulation n'est pas indiquée comme finie, gère et accepte les nouveaux individus dans la simulation. (sous la forme de connexion a travers des sockets.)
* handling des signaux: Le programme est conçu pour recevoir et traiter différement 2 signaux : ``SIGINT`` quand on essaye d'interrompre >>>``martinn ??`` 