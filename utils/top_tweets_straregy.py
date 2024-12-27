class TopTweetsStrategy:
    @staticmethod
    def calculate(df) -> dict:
        top_likes = df.copy().sort_values('like_count', ascending=False)
        top_likes = top_likes[0:20]

        top_retweets = df.copy().sort_values('retweet_count', ascending=False)
        top_retweets = top_retweets[0:20]

        top_general = df.copy()
        top_general['popularity'] = top_general['like_count'] + top_general['retweet_count']
        top_general.sort_values('popularity', ascending=False, inplace=True)
        top_general = top_general[0:20]

        return {'top_likes': top_likes, 'top_retweets': top_retweets, 'top_general': top_general}
