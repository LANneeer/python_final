from utils import Strategy
import pandas as pd
import plotly.express as px


class AntiTopAuthorsStrategy(Strategy):
    @staticmethod
    def calculate(df: pd.DataFrame) -> dict:
        """
        Calculate and construct a tops of authours by their overall popularity.
        Time complexity: O(n + m), where n is the number of rows in the DataFrame, and m is the number of unique usernames.
        Space complexity: O(n + m), where n is for the copy of the DataFrame and m is for storing grouped data.
        """

        authors_df = (
            df.copy()
            .groupby("username")
            .sum()
            .reset_index()[["username", "like_count", "retweet_count"]]
        )

        authors_df["popularity"] = (
            authors_df["like_count"] + 10 * authors_df["retweet_count"]
        )
        authors_df = (
            authors_df.sort_values("popularity", ascending=False)[
                authors_df["popularity"] >= 1
            ]
            .drop_duplicates(subset=["popularity"])
            .tail(20)
        )

        return authors_df.to_dict(orient="records")

    @staticmethod
    def generate_html(data, output_file="anti_top_users_popularity.html"):
        df = pd.DataFrame.from_dict(data)

        fig = px.bar(
            df,
            x="username",
            y="popularity",
            title="Anti-Top Users by Popularity",
            labels={"x": "Username", "y": "Popularity"},
        )
        fig.write_html(output_file)
        print(f"Anti-Top Users By Popularity saved to {output_file}")

