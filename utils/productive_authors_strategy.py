import pandas as pd
import plotly.express as px
from utils import Strategy


class ProductiveAuthorsStrategy(Strategy):
    @staticmethod
    def calculate(df: pd.DataFrame) -> dict:
        """Calculate and construct a top by post count of each author"""

        # construct the top simply applying group by username on data frame and sort it
        productivity_df = (
            df.groupby("username")
            .size()
            .reset_index(name="post_count")
            .sort_values("post_count", ascending=False)
        )

        return productivity_df[0:30].to_dict(orient="records")

    @staticmethod
    def generate_html(df: pd.DataFrame, output_file="top_users.html"):
        top_users = (
            df.groupby("username")["like_count"]
            .sum()
            .sort_values(ascending=False)
            .head(10)
        )
        fig = px.bar(
            x=top_users.index,
            y=top_users.values,
            title="Top Users by Likes",
            labels={"x": "Username", "y": "Total Likes"},
        )
        fig.write_html(output_file)
        print(f"Top Users Bar Chart saved to {output_file}")

