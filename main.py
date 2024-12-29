import os

import pandas as pd
import numpy as np
from utils import Context
from utils import ProductiveAuthorsStrategy
from utils import TopTweetsStrategy
from utils import TopWordsStrategy
from utils import TweetFrequencyStrategy
from utils.antitop_authors_strategy import AntiTopAuthorsStrategy
from utils.top_authors_strategy import TopAuthorsStrategy

if __name__ == "__main__":
    # pandas configuration
    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", None)

    # create program context
    context = Context(pd.read_csv("data/Twitter_Jan_Mar.csv"))

    # Execute and generate HTML for Top Words Strategy
    top_words = context.execute(TopWordsStrategy())
    # print("Generated Top Words:", top_words)
    TopWordsStrategy.generate_html(top_words["inverted_index"], "top_words.html")

    # Execute and generate HTML for Top Tweets Strategy
    top_tweets = context.execute(TopTweetsStrategy())
    # print("Top Likes:", top_tweets["top_likes"])
    # print("Top Retweets:", top_tweets["top_retweets"])
    # print("Top General:", top_tweets["top_general"])
    TopTweetsStrategy.generate_html(top_tweets, ("top_tweets_likes.html", "top_tweets_retweets.html", "top_tweets_popularity.html"))

    # Execute and generate HTML for Productive Authors Strategy
    productive_authors = context.execute(ProductiveAuthorsStrategy())
    # print("Productive Authors:", productive_authors)
    ProductiveAuthorsStrategy.generate_html(productive_authors, "top_users_posts.html")

    # Execute and generate HTML for Top Authors Strategy
    top_authors = context.execute(TopAuthorsStrategy())
    # TODO generate plotly HTML for such top

    # Execute and generate HTML for Anti-Top Authors Strategy
    anti_top_authors = context.execute(AntiTopAuthorsStrategy())
    AntiTopAuthorsStrategy.generate_html(anti_top_authors, "anti_top_users_popularity.html")

    # Execute and generate HTML for Tweet Frequency Strategy
    tweet_frequency = context.execute(TweetFrequencyStrategy())
    # print("Tweet Frequency:", tweet_frequency)
    TweetFrequencyStrategy.generate_html(tweet_frequency, "tweet_frequency.html")

    # Calculate statistics for Tweet Frequency
    tweet_counts = pd.Series([entry["post_count"] for entry in tweet_frequency])
    min_tweets = np.min(tweet_counts)
    max_tweets = np.max(tweet_counts)
    median_tweets = int(np.median(tweet_counts))

    # Generate HTML with Tweet Frequency Statistics
    stats_html = f"""
    <html>
    <head>
        <title>Tweet Frequency Statistics</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            table {{ border-collapse: collapse; width: 50%; margin: 20px auto; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: center; }}
            th {{ background-color: #1da1f2; color: white; }}
            caption {{ font-size: 1.5em; margin-bottom: 10px; }}
        </style>
    </head>
    <body>
        <table>
            <caption>Tweet Frequency Statistics</caption>
            <tr><th>Statistic</th><th>Value</th></tr>
            <tr><td>Min Tweets</td><td>{min_tweets}</td></tr>
            <tr><td>Max Tweets</td><td>{max_tweets}</td></tr>
            <tr><td>Median Tweets</td><td>{median_tweets}</td></tr>
        </table>
    </body>
    </html>
    """

    with open("tweet_frequency_stats.html", "w") as file:
        file.write(stats_html)

    print(f"Min Tweets: {min_tweets}")
    print(f"Max Tweets: {max_tweets}")
    print(f"Median Tweets: {median_tweets}")
    print("Tweet Frequency Statistics HTML saved to tweet_frequency_stats.html")

    print("Program finished. HTML files generated.")
