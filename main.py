import os

import dotenv
import pandas as pd

from utils import Context
from utils import ProductiveAuthorsStrategy
from utils import TopTweetsStrategy
from utils import TopWordsStrategy
from utils import TweetFrequencyStrategy

if __name__ == "__main__":
    dotenv.load_dotenv()

    # pandas configuration
    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", None)

    # create program context
    context = Context(pd.read_csv(os.getenv("DATA_PATH")))

    # Execute and generate HTML for Top Words Strategy
    top_words = context.execute(TopWordsStrategy())
    # print("Generated Top Words:", top_words)
    TopWordsStrategy.generate_html(top_words["inverted_index"], "top_words.html")

    # Execute and generate HTML for Top Tweets Strategy
    top_tweets = context.execute(TopTweetsStrategy())
    # print("Top Likes:", top_tweets["top_likes"])
    # print("Top Retweets:", top_tweets["top_retweets"])
    # print("Top General:", top_tweets["top_general"])
    TopTweetsStrategy.generate_html(context.df, "top_tweets.html")

    # Execute and generate HTML for Productive Authors Strategy
    productive_authors = context.execute(ProductiveAuthorsStrategy())
    # print("Productive Authors:", productive_authors)
    ProductiveAuthorsStrategy.generate_html(context.df, "top_users.html")

    # Execute and generate HTML for Tweet Frequency Strategy
    tweet_frequency = context.execute(TweetFrequencyStrategy())
    # print("Tweet Frequency:", tweet_frequency)
    TweetFrequencyStrategy.generate_html(context.df, "tweet_frequency.html")

    print("Program finished. HTML files generated.")
