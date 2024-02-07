# Instructions:

Voici votre petit challenge technique ! L'idée c'est de voir comment vous vous débrouillez et organisez votre code et votre pensée face à un descriptif de projet volontairement très succinct. Le projet est simple dans sa structure : vous avez un FastAPI qui interroge une BDD que vous devez préalablement remplir.

## Docker / Docker-compose:
	- Un container avec FastAPI
	- Un container avec un gestionnaire de BDD au choix

## Importation des données :
	- Récupérer le fichier csv à cette URL : [CSV des communes](https://www.data.gouv.fr/fr/datasets/r/dbe8a621-a9c4-4bc3-9cae-be1699c5ff25) 
	- Ne garder que les colonnes code_postal, nom_commune_complet
	- Mettre les noms des communes en MAJ
	- Calculer le département de la commune
	- Envoyer ces données dans votre base

## Méthodes de votre FastAPI :
	- Pousser / Mettre à jour une commune, son code postal et son 
	- département dans ta BDD
	- Récupérer les informations d'une commune sur la base de son nom
	- Récupérer la liste de toutes les communes d'un département

## Tips / Bonus / Contraintes :
	- Contrainte : du python, (mais pas de  pandas, contrainte non respectée)

## Bonus : calculer vous-même les coordonnées GPS des communes. Tips du bonus : vous pouvez trouver des mappers open-source dockerisés pour ça... 
Tips 0 : la méthodologie ETL peut aider à structurer votre code
Tips 1 : des bons commentaires simplifient la lecture du code
Tips 2 : utilise votre git !

Nous ferons un petit debrief de tout cela : comment vous vous êtes organisé, quels ont été vos choix techniques, comment vous êtes allé chercher les infos qui vous manquaient, où avez-vous eu des difficultés et comment vous les avez contournées et finalement, comment vous auriez pu améliorer tout ça selon vous :)

# ============================================================

# To do:

- faire fonctionner la partie import de données geocoding dans la bdd.
- implémenter un moyen visuel de connaitre l'etat du deploiement. 
- optimisation des process.


# infos:

- je note un delta apres traitement entre le nombre de ligne à la source (39 902 lignes) et le nombre d'entrées dans la bdd (36 369). à creuser.