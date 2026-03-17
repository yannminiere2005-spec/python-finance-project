import pandas as pd
import os

def trouver_colonne_annee(df, annee_cible):
    """Cherche l'index de la colonne qui contient l'année."""
    for r in range(min(5, len(df))):
        ligne = df.iloc[r]
        for i, valeur in enumerate(ligne):
            if str(annee_cible) in str(valeur):
                return i
    return None

def obtenir_chiffre(df, mots_cles, col_index):
    """Cherche plusieurs synonymes et renvoie la valeur si elle existe."""
    if isinstance(mots_cles, str):
        mots_cles = [mots_cles]
        
    for mot in mots_cles:
        ligne = df[df[0].str.contains(mot, case=False, na=False)]
        if not ligne.empty:
            val_brute = str(ligne.iloc[0, col_index])
            # Nettoyage des caractères spéciaux
            val_propre = val_brute.replace(',', '').replace(' ', '').replace('(', '').replace(')', '').replace('-', '0')
            try:
                return float(val_propre)
            except ValueError:
                continue
    return None 

def analyser_entreprise():
    # Définition du chemin vers le dossier data
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    print("\n--- ANALYSEUR DE RATIOS ---")
    nom_ent = input("Nom de l'entreprise : ")
    annee = input("Année à analyser : ")
    
    nom_fichier = f"bilan_{nom_ent.replace(' ', '_')}_{annee}.csv"
    chemin_csv = os.path.join(BASE_DIR, "data", nom_fichier)

    if not os.path.exists(chemin_csv):
        print(f" Erreur : Le fichier {nom_fichier} n'existe pas. Lancez l'extraction d'abord.")
        return

    # Chargement du CSV généré par le script d'extraction
    df = pd.read_csv(chemin_csv, header=None)
    col_index = trouver_colonne_annee(df, annee)

    if col_index is None:
        print(f" Impossible de trouver l'année {annee} dans le fichier.")
        return

    # --- RÉCUPÉRATION DES DONNÉES ---
    ca = obtenir_chiffre(df, ["Revenue", "Turnover", "Sales", "Chiffre d'affaires", "CA"], col_index)
    current_assets = obtenir_chiffre(df, "Current assets", col_index)
    current_liabs = obtenir_chiffre(df, "Current liabilities", col_index)
    inventories = obtenir_chiffre(df, ["Inventories", "Stocks"], col_index)
    cash = obtenir_chiffre(df, ["Cash and cash", "Trésorerie"], col_index)
    receivables = obtenir_chiffre(df, ["Trade and other receivables", "Créances clients"], col_index)
    total_assets = obtenir_chiffre(df, "TOTAL ASSETS", col_index)
    payables = obtenir_chiffre(df, "Trade and other payables", col_index)

    print(f"\n" + "="*55)
    print(f" RAPPORTS FINANCIERS : {nom_ent.upper()} ({annee})")
    print("="*55)

    # --- SECTION LIQUIDITÉ ---
    print(f"--- Ratios de Liquidité ---")
    if current_assets and current_liabs:
        print(f"1. Liquidité Générale : {current_assets / current_liabs:.2f}")
        
        if inventories is not None:
            print(f"2. Quick Ratio        : {(current_assets - inventories) / current_liabs:.2f}")
        else:
            print("2. Quick Ratio        : Donnée 'Inventories' manquante")
            
        if cash is not None:
            print(f"3. Cash Ratio         : {cash / current_liabs:.2f}")
        else:
            print("3. Cash Ratio         : Donnée 'Cash' manquante")
            
        if total_assets:
            wc_ratio = (current_assets - current_liabs) / total_assets
            print(f"4. Ratio Fonds de Roulement : {wc_ratio:.2f}")
    else:
        print(" Calcul impossible : Actif ou Passif circulant manquant.")

    # --- SECTION GESTION ---
    print(f"\n--- Ratios de Gestion ---")
    if ca:

        if receivables is not None:
            dso = (receivables / ca) * 365
            print(f"5. DSO (Délai Client) : {dso:.0f} jours")
        else:
            print("5. DSO (Délai Client) : Créances clients non trouvées")
            
        if inventories:
            print(f"6. Rotation Stocks    : {ca / inventories:.2f} fois/an")
        else:
            print("6. Rotation Stocks    : Inventaires non trouvés")

        if total_assets:
            print(f"7. Rotation Actif Total   : {ca / total_assets:.2f} fois/an")
        else:
            print("7. Rotation Actif Total   : Total Assets non trouvé")
        
        if payables:
            dpo = (payables / ca) * 365
            print(f"8. DPO (Délai Fournisseur): {dpo:.0f} jours")
        else:
            print("8. DPO (Délai Fournisseur): Dettes fournisseurs non trouvées")
    else:
        print(" Chiffre d'affaires non disponible dans le fichier fourni.")
    
    print("="*55)

if __name__ == "__main__":
    analyser_entreprise()