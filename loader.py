#Ce module gère l'importation et la vérification du fichier Excel
import pandas as pd
import os

class DataLoader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = None

    def load_data(self):
        """Charge le fichier Excel et vérifie s'il existe."""
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"Le fichier {self.file_path} est introuvable.")
        
        # Lecture du fichier Excel
        self.data = pd.read_excel(self.file_path)
        
        # Suppression des lignes totalement vides
        self.data.dropna(how='all', inplace=True)
        print(f"✅ {len(self.data)} lignes chargées avec succès.")
        return self.data

    def get_company_data(self, company_name):
        """Récupère toutes les lignes d'une entreprise spécifique."""
        if self.data is None:
            self.load_data()
            
        company_df = self.data[self.data['entreprise'] == company_name]
        return company_df

# --- TEST DU CODE ---
if __name__ == "__main__":
    # Remplace 'donnees.xlsx' par ton vrai nom de fichier
    try:
        loader = DataLoader('donnees.xlsx')
        df = loader.load_data()
        print(df.head()) # Affiche les 5 premières lignes pour vérifier
    except Exception as e:
        print(f"❌ Erreur : {e}")