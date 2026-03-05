import pandas as pd


class FinancialStatement:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.data = self._load_csv()

    def _load_csv(self) -> pd.DataFrame:
        """
        Charge le fichier CSV et met 'Item' en index.
        """
        try:
            df = pd.read_csv(self.filepath, index_col="Item")
            return df
        except Exception as e:
            raise ValueError(f"Erreur lors du chargement du fichier : {e}")

    def __repr__(self):
        return f"FinancialStatement({self.filepath})"

    @property
    def years(self):
        return list(self.data.columns)

    @property
    def items(self):
        return list(self.data.index)

    def get(self, item: str, year: int):
        return self.data.loc[item, str(year)]