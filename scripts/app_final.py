import streamlit as st
import pandas as pd
from utils import extraire_donnees_pdf, trouver_colonne_annee, obtenir_chiffre

# Configuration de la page
st.set_page_config(page_title="Analyseur Financier", layout="wide")

st.title(" Analyseur de Bilans PDF")
st.write("Entrez l'exercice souhaité, déposez le PDF, et les ratios se calculeront automatiquement.")

# --- AJOUT : NOM DE L'ENTREPRISE ---
nom_entreprise = st.text_input("Nom de l'entreprise", "Mon Entreprise")

# Saisie de l'année au centre
annee = st.text_input(" Année à analyser (ex : 2024", "2024")

# --- MESSAGE D'AVERTISSEMENT ---
with st.expander(" Conseils pour un bon fonctionnement"):
    st.write("""
    Pour garantir la précision des calculs, assurez-vous que votre PDF respecte ces critères :
    * **Colonnes distinctes** : Chaque année doit avoir sa propre colonne (évitez les années empilées dans une même case).
    * **Format Tableau** : Les données doivent être présentées sous forme de tableau clair (bilan consolidé).
    * **Texte lisible** : Le PDF ne doit pas être un scan (image), mais un document avec du texte sélectionnable.
    """)

# Zone d'importation du fichier
uploaded_file = st.file_uploader("Choisir un fichier PDF", type="pdf")

if uploaded_file is not None:
    df = extraire_donnees_pdf(uploaded_file)
    if df is not None:
        col_idx = trouver_colonne_annee(df, annee)
        
        if col_idx is not None:
            # Récupération des données via utils.py
            assets = obtenir_chiffre(df, "Current assets", col_idx)
            liabs = obtenir_chiffre(df, "Current liabilities", col_idx)
            stocks = obtenir_chiffre(df, "Inventories", col_idx)
            cash = obtenir_chiffre(df, "Cash", col_idx)
            total_assets = obtenir_chiffre(df, "TOTAL ASSETS", col_idx)
            ca = obtenir_chiffre(df, "Revenue", col_idx)
            clients = obtenir_chiffre(df, "receivables", col_idx)
            equity = obtenir_chiffre(df, ["Equity", "owners"], col_idx)
            debt_lt = obtenir_chiffre(df, ["borrowings", "more than one year"], col_idx)
            debt_st = obtenir_chiffre(df, ["borrowings", "less than one year"], col_idx)
            
            debt = 0
            if debt_lt is not None: debt += debt_lt
            if debt_st is not None: debt += debt_st
            if debt == 0: debt = None
            
            non_current_liabs = obtenir_chiffre(df, ["Non-current liabilities"], col_idx)
            non_current_assets = obtenir_chiffre(df, ["Non-current assets"], col_idx)

            # --- AJOUT : MESSAGE DE SUCCÈS PERSONNALISÉ ---
            st.success(f" Voici les ratios de l'entreprise **{nom_entreprise}** pour l'exercice **{annee}**")

            # --- AFFICHAGE ---
            st.header(f" Analyse des Ratios - {annee}")
            
            # Rangée 1 : Liquidité
            c1, c2, c3, c4 = st.columns(4)
            
            if assets and liabs:
                c1.metric("Liquidité Générale", f"{assets/liabs:.2f}")
            else:
                c1.metric("Liquidité Générale", "N/A")
                
            if total_assets and stocks and liabs:
                c2.metric("Quick Ratio", f"{(total_assets - stocks) / liabs:.2f}")
            else:
                c2.metric("Quick Ratio", "N/A")
                
            if cash and liabs:
                c3.metric("Cash Ratio", f"{cash / liabs:.2f}")
            else:
                c3.metric("Cash Ratio", "N/A")
                
            if assets and liabs:
                c4.metric("FdR Net", f"{assets - liabs:,.0f} M€")
            else:
                c4.metric("FdR Net", "N/A")

            # Rangée 2 : Gestion
            st.divider()
            c5, c6, c7, c8 = st.columns(4)
            
            if ca and stocks:
                c5.metric("Rotation Stocks", f"{ca / stocks:.1f}x")
            if ca and clients:
                c6.metric("DSO (Délais clients)", f"{(clients / ca) * 365:.0f} j")
            if ca and total_assets:
                c7.metric("Rotation Actif", f"{ca / total_assets:.2f}x")
            if cash and total_assets:
                c8.metric("% Cash / Actif", f"{(cash / total_assets) * 100:.1f}%")

            # Rangée 3 : Solvabilité
            st.divider()
            c9, c10, c11 = st.columns(3)
            
            if equity and total_assets:
                c9.metric("Autonomie Financière", f"{equity / total_assets:.2f}")
            if debt and equity:
                c10.metric("Gearing", f"{debt / equity:.2f}")
            if equity and non_current_liabs and non_current_assets:
                val = (equity + non_current_liabs) / non_current_assets
                c11.metric("Couverture emplois stables", f"{val:.2f}")

            # Rangée 4 : Extras
            st.divider()
            c12, c13, c14, c15 = st.columns(4)
            
            if debt and total_assets:
                c12.metric("Debt / Assets", f"{debt / total_assets:.2f}")
            if total_assets and equity:
                c13.metric("Leverage", f"{total_assets / equity:.2f}")
            if debt and cash:
                c14.metric("Net Debt", f"{debt - cash:,.0f} M€")
            if assets and liabs and total_assets:
                c15.metric("WC / Assets", f"{(assets - liabs) / total_assets:.2f}")

        else:
            st.error(f"Impossible de trouver l'année '{annee}' dans le document.")
    else:
        st.error("Échec de la lecture du PDF.")