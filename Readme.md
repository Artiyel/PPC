# Rapport PPC

## To do:
- [ ] mémoire partagée (population de l'herbe)
- [x] signal pour tuer proprement les proies qui sont en train de faire un truc

## Notice d'utilisation IA
Alexis:
* debuggage du signal entre proie et env --> L'ia a apporté de l'aide pour comprendre les détails de la documentation, mais j'avais correctement compris 95% de la chose
* debuggage sur l'intiatlisation de la mémoire partagée qui représente l'état de l'herbe (normal/secheresse) --> la documentation était pas très explicite, j'essayait de faire passer une string dans une `multiprocessing.Value()` mais ce n'est apparement pas possible
* Debuggage général et check si erreur de logique que je n'avais pas vue --> repérage d'une erreur a la fermeture des connections, solution implémentée inspirée de la suggestion de l'ia
* beaucoup d'affichages d'erreures dans la console --> L'ia m'a renseigné sur la signification des messages d'erreur, j'ai pu aviser si il était pertinant de les afficher ou non