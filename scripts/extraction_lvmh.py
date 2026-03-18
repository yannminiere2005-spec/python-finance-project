import pdfplumber
import pandas as pd
import os

# Chemins robustes
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
pdf_path = os.path.join(BASE_DIR, "data", "LVMH.pdf")
output_path = os.path.join(BASE_DIR, "data", "bilan_lvmh_complet.csv")

print(f"🚀 Extraction du bilan complet en cours...")

try:
    with pdfplumber.open(pdf_path) as pdf:
        # On cible la page du bilan (Page 1 de votre extrait)
        page = pdf.pages[0]
        
        # Configuration pour capturer les intitulés à gauche et les colonnes d'années
        table_settings = {
            "vertical_strategy": "text",
            "horizontal_strategy": "text",
            "snap_y_tolerance": 4,
        }
        
        table = page.extract_table(table_settings)
        
        if table:
            df = pd.DataFrame(table)
            
            # On nettoie les lignes vides
            df = df.dropna(how='all')
            
            # Sauvegarde avec intitulés et années
            df.to_csv(output_path, index=False, header=False, encoding='utf-8-sig')
            
            print(f" Terminé ! Le fichier '{output_path}' est prêt.")
            print(f" {len(df)} lignes extraites avec succès.")
        else:
            print(" Aucun tableau trouvé. Vérifiez le PDF dans le dossier data.")

except Exception as e:
    print(f" Erreur : {e}")