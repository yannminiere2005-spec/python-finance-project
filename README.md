# Analyseur de Bilans Financiers (PDF to Dashboard)

Ce projet permet d'extraire automatiquement des données comptables à partir de rapports annuels au format PDF (bilans consolidés) pour générer un tableau de bord de ratios financiers.

## Fonctionnalités Finales
- **Interface Streamlit** : Une application web interactive pour uploader les PDF et visualiser les résultats instantanément.
- **Extraction Intelligente** : Analyse du texte des PDF pour identifier les postes du bilan (Assets, Liabilities, Equity, etc.).
- **Calcul Dynamique** : Génération de 15 ratios financiers (Liquidité, Solvabilité, Gestion, Structure).
- **Personnalisation** : Saisie du nom de l'entreprise et de l'année pour des rapports personnalisés.

## Structure du Projet
- `scripts/app_final.py` : Le cœur de l'application (Interface et Affichage).
- `scripts/utils.py` : Le moteur technique (Extraction PDF et calculs).
- `requirements.txt` : Liste des dépendances nécessaires.

## Installation et Lancement
1. Installer les dépendances : `pip install -r requirements.txt`
2. Lancer l'application : `streamlit run scripts/app_final.py`

## Ratios calculés
- **Liquidité** : Générale, Quick Ratio, Cash Ratio, FdR Net.
- **Solvabilité** : Autonomie financière, Gearing, Leverage, Debt/Assets.
- **Gestion** : Rotation des stocks, DSO (Délais clients), % Cash/Actif.