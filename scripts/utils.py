import pandas as pd
import pdfplumber

def extraire_donnees_pdf(pdf_file):
    try:
        with pdfplumber.open(pdf_file) as pdf:
            all_rows = []
            for page in pdf.pages:
                # extract_table est plus stable que extract_tables pour la fusion
                table = page.extract_table(table_settings={
                    "vertical_strategy": "text", 
                    "horizontal_strategy": "text"
                })
                if table:
                    all_rows.extend(table)
            
            if all_rows:
                # On crée le DataFrame à partir de toutes les lignes récupérées
                df = pd.DataFrame(all_rows).fillna("")
                return df
        return None
    except Exception as e:
        return None

def trouver_colonne_annee(df, annee_recherchee):
    annee_str = str(annee_recherchee)
    
    # On scanne les 5 premières lignes au cas où l'année est un peu plus bas
    nb_lignes_a_scanner = min(5, len(df))
    
    for r in range(nb_lignes_a_scanner):
        for i, val in enumerate(df.iloc[r]):
            if annee_str in str(val):
                return i
    return None

def obtenir_chiffre(df, mots_cles, col_index):
    if isinstance(mots_cles, str):
        mots_cles = [mots_cles]
    
    for mot in mots_cles:
        for r in range(len(df)):
            # On cherche le mot dans toute la ligne pour plus de flexibilité
            ligne_complete = " ".join([str(val) for val in df.iloc[r]]).lower()
            
            if mot.lower() in ligne_complete:
                try:
                    val_brute = str(df.iloc[r, col_index])
                    # Nettoyage des caractères non numériques courants
                    val_propre = val_brute.replace('\n', '').replace(',', '').replace(' ', '').replace('-', '0')
                    
                    # Gestion des parenthèses pour les chiffres négatifs
                    if '(' in val_propre:
                        val_propre = '-' + val_propre.replace('(', '').replace(')', '')
                    
                    # Gestion du point comme séparateur de milliers (spécifique Hermès)
                    if '.' in val_propre and len(val_propre.split('.')[-1]) == 3:
                        val_propre = val_propre.replace('.', '')

                    return float(val_propre)
                except (ValueError, IndexError):
                    continue
    return None