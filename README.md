# python-finance-project
Collaborative Python project focused on financial analysis and modeling.

## Module Diane

### Extraction de données
- **Script** : `scripts/extraction_generale.py`
- **Fonctionnement** : Sélection interactive du PDF via une fenêtre de dialogue, saisie du nom de l'entreprise et de l'année.
- [cite_start]**Sortie** : Génération automatique d'un CSV dans le dossier `data/` pour vérification visuelle.

### Analyse Financière
- **Script** : `scripts/liquidity_analysis.py`
- [cite_start]**Ratios de Liquidité** : Liquidité générale, Quick Ratio, Cash Ratio, Fonds de roulement net.
- [cite_start]**Ratios de Gestion** : DSO (Délai client), Rotation des stocks, Rotation de l'actif, DPO.
- [cite_start]**Robustesse** : Gestion des synonymes comptables (Revenue/Turnover) et messages d'alerte si une donnée est absente du PDF