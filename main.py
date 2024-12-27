import os

import dotenv
import pandas as pd

from utils import Context
from utils.productive_authors_strategy import ProductiveAuthorsStrategy
from utils.top_tweets_straregy import TopTweetsStrategy

if __name__ == "__main__":
    dotenv.load_dotenv()

    # pandas configuration
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)

    # create program context
    context = Context(pd.read_csv(os.getenv("DATA_PATH")))

    # execute all the strategies
    #ctx.execute(TopWordsStrategy())
    top_tweets = context.execute(TopTweetsStrategy())
    print(top_tweets['top_likes'])
    print(top_tweets['top_retweets'])
    print(top_tweets['top_general'])

    print(context.execute(ProductiveAuthorsStrategy()))
    #ctx.execute(...)
    #ctx.execute(...)
    #...

    print("program finished")
