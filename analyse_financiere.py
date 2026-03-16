import pandas as pd

# 1. LA RECETTE (Ta classe Bilan)
class Bilan:
    def __init__(self, entreprise, actif_circulant, passif_circulant):
        self.entreprise = entreprise
        self.actif_c = actif_circulant
        self.passif_c = passif_circulant

    def calculer_liquidite(self):
        if self.passif_c == 0:
            return "Indéfini (pas de dettes)"
        return round(self.actif_c / self.passif_c, 2)

    def diagnostic(self):
        ratio = self.calculer_liquidite()
        if isinstance(ratio, str): return ratio
        
        if ratio >= 1:
            return "✅ Santé correcte : l'actif couvre les dettes."
        else:
            return "⚠️ Alerte : Risque de problème de trésorerie !"

# 2. LE MOTEUR (La lecture de l'Excel)
def lancer_analyse_globale(nom_fichier_excel):
    try:
        # On lit le fichier avec Pandas
        df = pd.read_excel(nom_fichier_excel)
        
        print("\n" + "="*40)
        print("🔍 ANALYSE AUTOMATISÉE DES BILANS")
        print("="*40 + "\n")

        # On parcourt chaque ligne du fichier Excel
        for index, ligne in df.iterrows():
            # On crée l'objet pour l'entreprise de la ligne actuelle
            mon_bilan = Bilan(
                entreprise=ligne['entreprise'],
                actif_circulant=float(ligne['actif_circulant']),
                passif_circulant=float(ligne['passif_circulant'])
            )

            # On affiche les résultats proprement
            print(f"🏢 Entreprise : {mon_bilan.entreprise}")
            print(f"📊 Ratio de Liquidité : {mon_bilan.calculer_liquidite()}")
            print(f"💡 Verdict : {mon_bilan.diagnostic()}")
            print("-" * 40)

    except Exception as e:
        print(f"❌ Oups, petit souci : {e}")

# 3. LE BOUTON "ON"
lancer_analyse_globale('donnees.xlsx')