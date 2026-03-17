import pandas as pd
import numpy as np

# Définir le chemin du fichier CSV pour l'extraction
file_path = 'data/bilan_lvmh_complet.csv'  # Remplacer par le chemin correct

# Lire le fichier CSV avec une gestion des en-têtes et lignes
bilan_lvmh_df = pd.read_csv(file_path, header=3)  # Le fichier commence à la ligne 4, donc header=3

# Nettoyer le DataFrame pour garder les données utiles
# Supprimer les lignes vides ou inutiles (en particulier celles en haut du fichier)
bilan_lvmh_df_cleaned = bilan_lvmh_df.dropna(how='all')  # Supprimer les lignes complètement vides

# Renommer les colonnes pour qu'elles correspondent aux années
bilan_lvmh_df_cleaned.columns = ['Asset', 'Notes', '2025', '2024', '2023']

# Filtrer et organiser les données
bilan_lvmh_df_cleaned = bilan_lvmh_df_cleaned[bilan_lvmh_df_cleaned['Asset'] != '(EUR millions)']
bilan_lvmh_df_cleaned = bilan_lvmh_df_cleaned.reset_index(drop=True)

# Créer un dictionnaire avec les actifs comme clés et les valeurs pour chaque année
financial_data_dict = {}

for index, row in bilan_lvmh_df_cleaned.iterrows():
    asset = row['Asset']
    financial_data_dict[asset] = {
        '2025': row['2025'],
        '2024': row['2024'],
        '2023': row['2023']
    }

# Convertir les valeurs en nombres flottants et gérer les tirets ('-') en les remplaçant par NaN
for asset in financial_data_dict:
    for year in financial_data_dict[asset]:
        value = financial_data_dict[asset][year]
        
        # Si la valeur est un tiret, la remplacer par NaN
        if value == '-':
            financial_data_dict[asset][year] = np.nan
        else:
            # Si la valeur est une chaîne, on enlève les virgules et on la convertit en float
            if isinstance(value, str):
                financial_data_dict[asset][year] = float(value.replace(',', ''))
            # Si la valeur est déjà un nombre, on la garde telle quelle

# Affichage des 10 premiers éléments du dictionnaire pour validation
list(financial_data_dict.items())[:10]  # Affichage des 10 premiers éléments

# Exemple de comment récupérer les données pour un actif donné :
# Par exemple, pour "Brands and other intangible assets", obtenir les valeurs pour 2025, 2024, 2023 :
brand_data = financial_data_dict["Brands and other intangible assets"]
print(f"Brand data: {brand_data}")