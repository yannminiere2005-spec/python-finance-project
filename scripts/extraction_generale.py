import pdfplumber
import pandas as pd
import os
from tkinter import filedialog, Tk

# On définit le chemin de base du projet pour les sauvegardes
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def selectionner_pdf():
    """Ouvre une fenêtre Finder pour choisir le fichier PDF."""
    root = Tk()
    root.withdraw()
    root.attributes('-topmost', True) # Force la fenêtre au premier plan sur Mac
    
    print(" Veuillez sélectionner le fichier PDF de la Balance Sheet...")
    chemin_pdf = filedialog.askopenfilename(
        title="Sélectionnez le bilan (PDF)",
        filetypes=[("Fichiers PDF", "*.pdf")]
    )
    root.destroy()
    return chemin_pdf

def extraire_vers_dataframe(chemin_pdf):
    """Extrait le tableau de la première page du PDF."""
    print(f" Extraction en cours sur : {os.path.basename(chemin_pdf)}...")
    try:
        with pdfplumber.open(chemin_pdf) as pdf:
            page = pdf.pages[0]
            
            # Extraction 
            table = page.extract_table({
                "vertical_strategy": "text",
                "horizontal_strategy": "text",
                "snap_y_tolerance": 4,
            })
            
            if table:
                df = pd.DataFrame(table)
                # Nettoyage des lignes totalement vides
                df = df.dropna(how='all')
                return df
            else:
                return None
    except Exception as e:
        print(f" Erreur lors de l'extraction : {e}")
        return None

def main():
    # 1. Sélection du fichier
    chemin = selectionner_pdf()
    
    if not chemin:
        print(" Opération annulée : aucun fichier choisi.")
        return

    # 2. Saisie des informations de l'entreprise
    print("\n" + "="*40)
    nom_entreprise = input("Entrez le nom de l'entreprise : ")
    annee_saisie = input(f"Quelle année souhaitez-vous analyser pour {nom_entreprise} ? : ")
    print("="*40)

    # 3. Extraction technique
    df_brut = extraire_vers_dataframe(chemin)

    if df_brut is not None:
        print(f"\n Succès ! Le document de {nom_entreprise} a été chargé.")
        
        # --- SAUVEGARDE DANS LE DOSSIER DATA ---
        # Nom de fichier clair :
        nom_fichier_csv = f"bilan_{nom_entreprise.replace(' ', '_')}_{annee_saisie}.csv"
        chemin_sauvegarde = os.path.join(BASE_DIR, "data", nom_fichier_csv)
        
        # Création du dossier data s'il n'existe pas
        if not os.path.exists(os.path.join(BASE_DIR, "data")):
            os.makedirs(os.path.join(BASE_DIR, "data"))
            
        # Sauvegarde physique du fichier
        df_brut.to_csv(chemin_sauvegarde, index=False, header=False, encoding='utf-8-sig')
        
        print(f" Fichier sauvegardé : data/{nom_fichier_csv}")
        print(f" {len(df_brut)} lignes détectées.")
        
        # 4. Aperçu rapide dans le terminal
        print("\n--- Aperçu des premières lignes ---")
        print(df_brut.head()) 
        
    else:
        print(" Échec de l'extraction du tableau. Vérifiez que le PDF contient du texte sélectionnable.")

if __name__ == "__main__":
    main()