from utils import Strategy
import pandas as pd


class TopAuthorsStrategy(Strategy):
    @staticmethod
    def calculate(df: pd.DataFrame) -> dict:
        """Calculate and construct a tops of authours by their overall popularity"""

        authors_df = (df.copy()
                     .groupby('username')
                     .sum()
                     .reset_index()[['username', 'like_count', 'retweet_count']])

        authors_df['popularity'] = authors_df['like_count'] + 10 * authors_df['retweet_count']
        authors_df = authors_df.sort_values('popularity', ascending=False).head(20)

        return authors_df.to_dict(orient='records')


    @staticmethod
    def generate_html(data, output_file="top_users_popularity.html"):
        # TODO
        pass