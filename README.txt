Auteur : François Flandin

Voici mon projet de résolution de problèmes, 
le programme pour effectuer les liaisons Xml -> Dot et Dot -> Xml est le fichier xml2pdf_dot2xml.py
pour le lancer, il faut effectuer la commande suivante :

python3 xml2pdf_dot2xml.py fichier_entree <options> fichier_sortie

* le nom de fichier d'entrée est obligatoire, et l'extension de fichier est automatiquement détéctée

voici les options disponibles :
* --show : affiche le graphe généré par dot
* --save : choisi le nom/emplacement du fichier généré (attention : pas d'extension, l'extension est automatiquement générée en fonction du type de fichier d'entrée)
