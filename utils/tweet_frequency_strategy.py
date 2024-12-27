import time

import pandas as pd

from utils import Strategy


class TweetFrequencyStrategy(Strategy):
    @staticmethod
    def calculate(df: pd.DataFrame) -> dict:
        df_copy = df.copy()

        df_copy['date'] = pd.to_datetime(df_copy['date'], errors='coerce')
        df_copy['date'] = df_copy['date'].dt.date
        df_copy = df_copy.groupby('date').size().reset_index(name='post_count').sort_values('date', ascending=True)

        return df_copy.to_dict(orient='records')

