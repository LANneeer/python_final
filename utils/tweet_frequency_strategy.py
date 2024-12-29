import time

import plotly.express as px
import pandas as pd

from utils import Strategy


class TweetFrequencyStrategy(Strategy):
    @staticmethod
    def calculate(df: pd.DataFrame) -> dict:
        df_copy = df.copy()

        df_copy["date"] = pd.to_datetime(df_copy["date"], errors="coerce")
        df_copy["date"] = df_copy["date"].dt.date
        df_copy = (
            df_copy.groupby("date")
            .size()
            .reset_index(name="post_count")
            .sort_values("date", ascending=True)
        )

        return df_copy.to_dict(orient="records")

    @staticmethod
    def generate_html(df: pd.DataFrame, output_file="tweet_frequency.html"):
        """Generate HTML for tweet frequency over time."""
        df["date"] = pd.to_datetime(
            df["date"], errors="coerce"
        ).dt.date  # Coerce invalid dates to NaT
        df = df.dropna(subset=["date"])  # Drop rows with invalid dates
        daily_tweet_count = df.groupby("date").size()
        fig = px.line(
            x=daily_tweet_count.index,
            y=daily_tweet_count.values,
            title="Tweet Frequency Over Time",
            labels={"x": "Date", "y": "Number of Tweets"},
        )
        fig.write_html(output_file)
        print(f"Tweet Frequency Line Chart saved to {output_file}")
