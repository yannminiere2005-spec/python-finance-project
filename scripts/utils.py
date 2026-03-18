import pandas as pd
import pdfplumber

def extraire_donnees_pdf(pdf_file):
    try:
        with pdfplumber.open(pdf_file) as pdf:
            all_tables = []
            # On parcourt TOUTES les pages au lieu de juste la première
            for page in pdf.pages:
                tables = page.extract_tables(table_settings={
                    "vertical_strategy": "text", 
                    "horizontal_strategy": "text"
                })
                for t in tables:
                    all_tables.append(pd.DataFrame(t))
            
            if all_tables:
                # On fusionne tout pour avoir accès au Bilan ET au Compte de Résultat
                return pd.concat(all_tables, ignore_index=True).fillna("")
        return None
    except Exception as e:
        return None

def trouver_colonne_annee(df, annee_cible):
    """Cherche l'année dans tout le tableau nettoyé."""
    annee_str = str(annee_cible).strip()
    for r in range(len(df)):
        for i, valeur in enumerate(df.iloc[r]):
            val_nettoyee = str(valeur).replace('\n', '').replace(' ', '')
            if annee_str in val_nettoyee:
                return i
    return None

def obtenir_chiffre(df, mots_cles, col_index):
    if isinstance(mots_cles, str):
        mots_cles = [mots_cles]
    
    for mot in mots_cles:
        for r in range(len(df)):
            # On cherche le mot dans TOUTE la ligne (au cas où il y a un décalage de colonne)
            ligne_complete = " ".join([str(val) for val in df.iloc[r]]).lower()
            
            if mot.lower() in ligne_complete:
                val_brute = str(df.iloc[r, col_index])
                # Nettoyage
                val_propre = val_brute.replace('\n', '').replace(',', '').replace(' ', '').replace('-', '0')
                
                if '(' in val_propre:
                    val_propre = '-' + val_propre.replace('(', '').replace(')', '')
                
                # Gestion du point comme séparateur de milliers (ex: 2.797 dans Hermès)
                if '.' in val_propre and len(val_propre.split('.')[-1]) == 3:
                    val_propre = val_propre.replace('.', '')

                try:
                    return float(val_propre)
                except ValueError:
                    continue
    return None