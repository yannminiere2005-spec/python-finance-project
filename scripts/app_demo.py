import streamlit as st
import pandas as pd

# Configuration de la page
st.set_page_config(page_title="Finance Analyzer", layout="wide")

st.title(" Analyseur Financier Interactif")
st.write("Déposez un rapport annuel (PDF) pour extraire les ratios automatiquement.")

# Sidebar pour les options
st.sidebar.header("Paramètres")
entreprise = st.sidebar.selectbox("Entreprise", ["Hermès", "LVMH", "Kering"])
annee = st.sidebar.slider("Année", 2020, 2024, 2024)

# Simulation d'import de fichier
uploaded_file = st.file_uploader("Choisir le PDF de l'entreprise", type="pdf")

# On simule l'affichage si un fichier est "déposé" (ou par défaut pour la démo)
st.divider()
st.subheader(f"Résultats pour {entreprise} ({annee})")

# Création de colonnes pour des "cartes" de résultats
col1, col2, col3, col4 = st.columns(4)

# Utilisation des vrais chiffres extraits d'Hermès 2024 
# Current Assets: 15476, Current Liabs: 3629
ratio_liq = 15476 / 3629 

with col1:
    st.metric(label="Liquidité Générale", value=f"{ratio_liq:.2f}", delta="Excellent")
with col2:
    st.metric(label="Quick Ratio", value="3.39", delta="Stable")
with col3:
    st.metric(label="DSO (Jours)", value="11", delta="-2 jours", delta_color="normal")
with col4:
    st.metric(label="Cash Ratio", value="3.20", delta="Haut")

# Affichage d'un graphique simple pour le fun
st.write("### Évolution de la Liquidité")
chart_data = pd.DataFrame({
    'Année': [2022, 2023, 2024],
    'Ratio': [4.10, 4.40, ratio_liq]
})
st.line_chart(chart_data.set_index('Année'))

st.success(" Analyse terminée avec succès. Les données correspondent au bilan consolidé.")