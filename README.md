# Analyseur de Bilans Financiers (PDF to Streamlit)

## Présentation du projet
Ce projet a pour objectif l'automatisation de l'analyse financière à partir de rapports annuels au format PDF. L'application extrait les données comptables brutes pour calculer et afficher instantanément les principaux ratios de liquidité, de solvabilité et de gestion.

## Choix technologiques
Nous avons sélectionné trois bibliothèques Python pour répondre aux besoins spécifiques du projet :
* **Streamlit** : Utilisé pour développer l'interface utilisateur web interactive. Cela permet un déploiement rapide et une gestion simplifiée de l'importation des fichiers.
* **Pandas** : Centralise la manipulation des données. Les tableaux extraits sont convertis en DataFrames pour garantir la précision des calculs mathématiques.
* **Pdfplumber** : Choisi pour sa capacité à extraire des tableaux complexes. Contrairement à d'autres outils, il permet de conserver la structure des lignes, ce qui est crucial pour identifier les postes du bilan.

## Structure du répertoire
* `scripts/app_final.py` : Point d'entrée de l'application gérant l'interface et l'affichage des métriques.
* `scripts/utils.py` : Moteur d'extraction contenant les fonctions de nettoyage de données et de recherche par mots-clés.
* `requirements.txt` : Liste des dépendances nécessaires au projet.

## Utilisation
1. Installation des dépendances : `pip install -r requirements.txt`
2. Lancement de l'interface : `streamlit run scripts/app_final.py`
3. Utilisation : Saisir le nom de l'entreprise, l'année souhaitée, puis uploader le rapport financier au format PDF.

## Précision technique
Le programme intègre un algorithme de nettoyage de données capable de gérer les variations de formatage entre entreprises (ex: gestion des majuscules, suppression des parenthèses comptables pour les passifs et traitement des séparateurs de milliers).

## Limites de notre projet
Bien que l'algorithme soit robuste face aux variations de nomenclature, il présente certaines limites liées à la structure des documents sources. En effet, le programme repose sur une lecture horizontale des données. Si le PDF présente des colonnes mal alignées, fusionnées ou une disposition verticale (années empilées dans une même cellule), l'extraction peut échouer.
Notre code nécessite des documents au format "texte natif". Les scans d'états financiers (images PDF) ne sont pas supportés.
Une amélioration future pourrait être d'intégrer un système de "Fuzzy Matching" (correspondance approximative) plus poussé pour couvrir 100% des variantes de libellés comptables rencontrées dans les rapports internationaux.