import pandas as pd

from utils import Strategy


class TopTweetsStrategy(Strategy):
    @staticmethod
    def calculate(df: pd.DataFrame) -> dict:
        """Calculate and construct a tops of tweets: by likes, by retweets and by popularity (general top)"""

        top_likes = df.copy().sort_values('like_count', ascending=False)
        top_likes = top_likes[0:20]

        top_retweets = df.copy().sort_values('retweet_count', ascending=False)
        top_retweets = top_retweets[0:20]

        # while calculating popularity values, like weights 1 point and retweet weights 10 points
        top_general = df.copy()
        top_general['popularity'] = top_general['like_count'] + 10 * top_general['retweet_count']
        top_general.sort_values('popularity', ascending=False, inplace=True)
        top_general = top_general[0:20]

        return {
            'top_likes': top_likes.to_dict(orient='records'),
            'top_retweets': top_retweets.to_dict(orient='records'),
            'top_general': top_general.to_dict(orient='records')
        }
