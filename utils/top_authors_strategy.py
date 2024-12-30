from utils import Strategy
import pandas as pd
import plotly.express as px


class TopAuthorsStrategy(Strategy):
    @staticmethod
    def calculate(df: pd.DataFrame) -> dict:
        """Calculate and construct a tops of authours by their overall popularity"""

        authors_df = (
            df.copy()
            .groupby("username")
            .sum()
            .reset_index()[["username", "like_count", "retweet_count"]]
        )

        authors_df["popularity"] = (
            authors_df["like_count"] + 10 * authors_df["retweet_count"]
        )
        authors_df = authors_df.sort_values("popularity", ascending=False).head(20)

        return authors_df.to_dict(orient="records")

    @staticmethod
    def generate_html(data, output_file="top_users_popularity.html"):
        """Generate an HTML file with a bar chart for top authors by popularity"""
        usernames = [entry["username"] for entry in data]
        popularities = [entry["popularity"] for entry in data]

        fig = px.bar(
            x=usernames,
            y=popularities,
            title="Top Authors by Popularity",
            labels={"x": "Username", "y": "Popularity"},
            text=popularities,
        )
        fig.update_traces(texttemplate="%{text}", textposition="outside")
        fig.update_layout(uniformtext_minsize=8, uniformtext_mode="hide")

        fig.write_html(output_file)
        print(f"Top Authors Bar Chart saved to {output_file}")
