## Notice d'utilisation IA
Alexis:
* debuggage du signal entre proie et env --> L'ia a apporté de l'aide pour comprendre les détails de la documentation, mais j'avais correctement compris 95% de la chose
* debuggage sur l'intiatlisation de la mémoire partagée qui représente l'état de l'herbe (normal/secheresse) --> la documentation était pas très explicite, j'essayait de faire passer une string dans une `multiprocessing.Value()` mais ce n'est apparement pas possible
* Debuggage général et check si erreur de logique que je n'avais pas vue --> repérage d'une erreur a la fermeture des connections, solution implémentée inspirée de la suggestion de l'ia
* beaucoup d'affichages d'erreures dans la console --> L'ia m'a renseigné sur la signification des messages d'erreur, j'ai pu aviser si il était pertinant de les afficher ou non
* Port sur linux (j'avais codé toute les ipc sur windows, donc sur linux il y avait moults problèmes)--> beaucoup d'erreur ont vue le jour, usage extensif pour se renseigner sur les erreur et les corriger

Martin :
* debuggage du display, notamment avec des problèmes de crash ou d'animation ne fonctionnant pas. Les réponses obtenues se sont souvent avérées inutiles car l'ia rapportait des problèmes d'optimisation ou de choix de méthodes pour la transmission d'informations (event vs queue,...) au lieu des vrais problèmes qui étaient souvent liés à la position d'une instruction par rapport aux autres.
* Beaucoup de recherches sur des forums, notamment stackoverflow, où on ne peut pas avoir l'origine du code partagé. Notamment pour l'utilisation des bouttons et l'animation de la fenêtre matplotlib.