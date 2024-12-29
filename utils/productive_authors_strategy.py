import pandas as pd
import plotly.express as px
from utils import Strategy


class ProductiveAuthorsStrategy(Strategy):
    @staticmethod
    def calculate(df: pd.DataFrame) -> dict:
        """Calculate and construct a top by post count of each author"""

        # construct the top simply applying group by username on data frame and sort it
        productivity_df = (df.groupby("username")
            .size()
            .reset_index(name="post_count")
            .sort_values("post_count", ascending=False)
        )

        return productivity_df[0:30].to_dict(orient="records")

    @staticmethod
    def generate_html(data, output_file="top_users_posts.html"):
        df = pd.DataFrame.from_dict(data)

        fig = px.bar(
            df,
            x="username",
            y="post_count",
            title="Top Users by Posts count",
            labels={"x": "Username", "y": "Total Posts"},
        )
        fig.write_html(output_file)
        print(f"Top Posts Users Bar Chart saved to {output_file}")

