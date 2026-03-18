import pandas as pd
import os

def trouver_index_annee(df, annee_recherchee):
    """Parcourt la première ligne du CSV pour trouver la colonne de l'année."""
    premiere_ligne = df.iloc[0] 
    for i, valeur in enumerate(premiere_ligne):
        if str(annee_recherchee) in str(valeur):
            return i
    return None

def obtenir_valeur(df, libelle, col_index):
    """Cherche un libellé et récupère la valeur dans la colonne col_index."""
    # On utilise .str.contains pour plus de souplesse sur les noms de lignes
    ligne = df[df[0].str.contains(libelle, case=False, na=False)]
    if not ligne.empty:
        val_brute = str(ligne.iloc[0, col_index])
        # Nettoyage des caractères spéciaux financiers
        val_propre = val_brute.replace(',', '').replace(' ', '').replace('-', '0').replace('(', '').replace(')', '')
        try:
            return float(val_propre)
        except ValueError:
            return 0.0
    return 0.0

def lancer_analyse():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_path = os.path.join(BASE_DIR, "data", "bilan_lvmh_complet.csv")

    if not os.path.exists(csv_path):
        print("Erreur : Le CSV est introuvable. Lancez l'extraction PDF d'abord.")
        return

    # Lecture du CSV sans headers
    df = pd.read_csv(csv_path, header=None)

    # --- INPUTS UTILISATEUR ---
    print("\n" + "="*40)
    nom_entreprise = input("Entrez le nom de l'entreprise analysée : ")
    print(f"Bienvenue dans l'analyseur de l'entreprise {nom_entreprise}")
    print("="*40)
    
    annee_saisie = input(f"Quelle année souhaitez-vous analyser pour {nom_entreprise} ? (ex: 2025) : ")

    # Recherche automatique de la colonne
    col_index = trouver_index_annee(df, annee_saisie)

    if col_index is None:
        print(f"Désolé, l'année {annee_saisie} n'a pas été trouvée dans le document.")
        return

    print(f"\nAnalyse en cours pour {nom_entreprise} ({annee_saisie})...")

    # --- EXTRACTION DES DONNÉES ---
    current_assets = obtenir_valeur(df, "Current assets", col_index)
    current_liabilities = obtenir_valeur(df, "Current liabilities", col_index)
    inventories = obtenir_valeur(df, "Inventories", col_index)
    cash = obtenir_valeur(df, "Cash and cash equivalents", col_index)

    # --- CALCULS ET AFFICHAGE ---
    if current_liabilities > 0:
        liq_gen = current_assets / current_liabilities
        quick_ratio = (current_assets - inventories) / current_liabilities
        cash_ratio = cash / current_liabilities
        
        print("-" * 50)
        print(f"Voici les ratios de liquidité de l'entreprise {nom_entreprise} pour l'année {annee_saisie} :")
        print(f" > Liquidité Générale : {liq_gen:.2f}")
        print(f" > Quick Ratio        : {quick_ratio:.2f}")
        print(f" > Cash Ratio         : {cash_ratio:.2f}")
        print("-" * 50)
    else:
        print(f"⚠️ Erreur : Les données de passif pour {nom_entreprise} sont introuvables.")

if __name__ == "__main__":
    lancer_analyse()