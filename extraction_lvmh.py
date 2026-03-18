import pdfplumber
import pandas as pd

# 1. Nom de votre nouveau fichier à une page
pdf_path = "LVMH.pdf"

print(f"Extraction complète du tableau depuis : {pdf_path}")

try:
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[0]
        
        # On utilise des réglages de précision pour ne pas rater les textes à gauche
        table = page.extract_table(table_settings={
            "vertical_strategy": "text", 
            "horizontal_strategy": "text"
        })
        
        if table:
            # On crée le DataFrame avec toutes les données brutes
            df = pd.DataFrame(table)
            
            # Nettoyage rapide : on enlève les lignes totalement vides
            df = df.dropna(how='all')
            
            # Sauvegarde en CSV (lisible par Excel)
            # On garde l'encodage 'utf-8-sig' pour que les symboles € s'affichent bien dans Excel
            df.to_csv("bilan_lvmh_complet.csv", index=False, header=False, encoding='utf-8-sig')
            
            print("Succès ! Le fichier 'bilan_lvmh_complet.csv' contient tout le tableau.")
            print("Vous y trouverez les intitulés et les années 2025, 2024, 2023.")
        else:
            print("Aucun tableau détecté. Essayez la stratégie par défaut.")
            # Stratégie de secours si le tableau est complexe
            table_simple = page.extract_table()
            pd.DataFrame(table_simple).to_csv("bilan_lvmh_complet.csv", index=False, header=False)

except Exception as e:
    print(f"Erreur : {e}")