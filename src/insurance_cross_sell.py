import joblib
import pandas as pd
from src.sanitizer import sanitizer

class InsuranceCrossSell:
    def __init__(self, pipeline_path="webapp/models/full_pipeline.joblib"):
        # Load trained pipeline(sanitize + pre-process + model)
        self.pipeline = joblib.load(pipeline_path)

    def create_dataframe(self, payload):
        # 1) Must be a list and not empty
        if not isinstance(payload, list) or not payload:
            raise ValueError('Formato inválido ou lista vazia: envie uma LISTA (array) de clientes em JSON.')
        # 2) Every item must be a dictionary
        if not all(isinstance(x, dict) for x in payload):
            raise ValueError('Formato inválido: envie uma LISTA (array) de clientes em JSON.')
        
        # Build dataframe
        df_original = pd.DataFrame(payload)
        return df_original
        
    def predict_proba(self, df_original):
        df_pred = df_original.copy()
        # Predict score
        proba = self.pipeline.predict_proba(df_pred)
        return proba

    def sort_by_rank(self, df_original, proba):
        # Rank original dataframe by score of the positive class 1(response: yes)
        df_original['Score'] = proba[:, 1]
        df_original = df_original.sort_values('Score', ascending=False)

        return df_original.to_json( orient='records', date_format='iso' )