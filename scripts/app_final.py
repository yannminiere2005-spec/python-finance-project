import streamlit as st
import pandas as pd
from utils import extraire_donnees_pdf, trouver_colonne_annee, obtenir_chiffre

# Configuration de la page (Mode large pour les colonnes de ratios)
st.set_page_config(page_title="Analyseur Financier", layout="wide")

st.title(" Analyseur de Bilans PDF")
st.write("Entrez l'exercice souhaité, déposez le PDF, et les ratios se calculeront automatiquement.")

# --- NOUVEL EMPLACEMENT : AU CENTRE ---
# L'utilisateur choisit l'année ici. Par défaut c'est 2024.
# S'il change pour 2025, 'trouver_colonne_annee' cherchera 2025 dans le PDF.
annee = st.text_input(" Année à analyser (ex: 2024, 2025...)", "2024")

# Zone d'importation du fichier
uploaded_file = st.file_uploader("Choisir un fichier PDF", type="pdf")

if uploaded_file is not None:
    df = extraire_donnees_pdf(uploaded_file)
    
    if df is not None:
        # On cherche dynamiquement la colonne qui contient l'année saisie au-dessus
        col_idx = trouver_colonne_annee(df, annee)
        
        if col_idx is not None:
            # Récupération des données selon l'année choisie
            assets = obtenir_chiffre(df, "Current assets", col_idx)
            liabs = obtenir_chiffre(df, "Current liabilities", col_idx)
            stocks = obtenir_chiffre(df, "Inventories", col_idx)
            cash = obtenir_chiffre(df, "Cash", col_idx)
            total_assets = obtenir_chiffre(df, "TOTAL ASSETS", col_idx)
            ca = obtenir_chiffre(df, "Revenue", col_idx)
            clients = obtenir_chiffre(df, "receivables", col_idx)

            # --- AFFICHAGE DES RATIOS ---
            st.header(f" Analyse des Ratios - {annee}")
            
            c1, c2, c3, c4 = st.columns(4)

            if assets and liabs:
                c1.metric("Liquidité Générale", f"{assets/liabs:.2f}")
                if stocks:
                    c2.metric("Quick Ratio", f"{(assets - stocks) / liabs:.2f}")
                if cash:
                    c3.metric("Cash Ratio", f"{cash / liabs:.2f}")
                c4.metric("FdR Net", f"{assets - liabs:,.0f} M€")
            
            # Seconde ligne de ratios (Gestion)
            st.divider()
            c5, c6, c7, c8 = st.columns(4)
            
            if ca:
                if stocks:
                    c5.metric("Rotation Stocks", f"{ca / stocks:.1f}x")
                if clients:
                    c6.metric("DSO (Délais clients)", f"{(clients / ca) * 365:.0f} j")
                if total_assets:
                    c7.metric("Rotation Actif", f"{ca / total_assets:.2f}x")
            
            if cash and total_assets:
                c8.metric("% Cash / Actif", f"{(cash / total_assets) * 100:.1f}%")

        else:
            # Message si l'année saisie n'est pas dans le fichier
            st.error(f"Impossible de trouver la colonne '{annee}' dans ce document.")
    else:
        st.error("Échec de la lecture du tableau dans le PDF.")