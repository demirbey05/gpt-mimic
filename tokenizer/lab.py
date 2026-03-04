# ETHOS Tokenization Implementation for Lab Events

import pandas as pd


class LabTokenizer:

    def __init__(self):
        self.vocabulary = {}
        self._itemid_to_token = {}

    def build_vocabulary(self, d_labitems: pd.DataFrame) -> dict:
        self._fit(d_labitems)
        self.vocabulary = {token: idx for idx, token in enumerate(sorted(self._itemid_to_token.values()))}
        return self.vocabulary

    def tokenize(self, labevents: pd.DataFrame) -> pd.DataFrame:
        labevents = labevents.copy()
        labevents['tokenized_version'] = labevents['itemid'].map(self._itemid_to_token)
        return labevents

    def _fit(self, d_labitems: pd.DataFrame) -> None:
        # Token format: LAB_{label}
        # Examples:
        #   "Glucose"           → "LAB_Glucose"
        #   "White Blood Cells" → "LAB_White Blood Cells"

        def normalize(label) -> str | None:
            if pd.isna(label):
                return None
            return 'LAB_' + str(label).strip()

        self._itemid_to_token = (
            d_labitems.set_index('itemid')['label']
            .map(normalize)
            .dropna()
            .to_dict()
        )
