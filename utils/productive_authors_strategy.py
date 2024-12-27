import pandas as pd

from utils import Strategy


class ProductiveAuthorsStrategy(Strategy):
    @staticmethod
    def calculate(df: pd.DataFrame) -> dict:
        """Calculate and construct a top by post count of each author"""

        # construct the top simply applying group by username on data frame and sort it
        productivity_df = df.groupby('username').size().reset_index(name='post_count').sort_values('post_count', ascending=False)

        return productivity_df[0:30].to_dict(orient='records')