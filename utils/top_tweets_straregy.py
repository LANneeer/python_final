import pandas as pd

import plotly.express as px
from utils import Strategy


class TopTweetsStrategy(Strategy):
    @staticmethod
    def calculate(df: pd.DataFrame) -> dict:
        """Calculate and construct a tops of tweets: by likes, by retweets and by popularity (general top)"""

        top_likes = df.copy().sort_values("like_count", ascending=False)
        top_likes = top_likes[0:20]

        top_retweets = df.copy().sort_values("retweet_count", ascending=False)
        top_retweets = top_retweets[0:20]

        # while calculating popularity values, like weights 1 point and retweet weights 10 points
        top_general = df.copy()
        top_general["popularity"] = (
            top_general["like_count"] + 10 * top_general["retweet_count"]
        )
        top_general.sort_values("popularity", ascending=False, inplace=True)
        top_general = top_general[0:20]

        return {
            "top_likes": top_likes.to_dict(orient="records"),
            "top_retweets": top_retweets.to_dict(orient="records"),
            "top_general": top_general.to_dict(orient="records"),
        }

    @staticmethod
    def generate_html(df: pd.DataFrame, output_file="top_tweets.html"):
        """Generate an HTML file for top tweets by likes and retweets."""
        df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        top_tweets = df.nlargest(10, ["like_count", "retweet_count"])

        html_content = f"""
        <html>
        <head>
            <title>Top Popular Tweets by Likes and Retweets</title>
            <style>
                body {{ font-family: Arial, sans-serif; background-color: #f9f9f9; margin: 0; padding: 0; }}
                table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #1da1f2; color: white; }}
                tr:nth-child(even) {{ background-color: #f2f2f2; }}
                tr:hover {{ background-color: #ddd; }}
                caption {{ caption-side: top; font-size: 1.5em; margin: 10px 0; }}
            </style>
        </head>
        <body>
            <table>
                <caption>Top Popular Tweets by Likes and Retweets</caption>
                <thead>
                    <tr>
                        <th>date</th>
                        <th>id</th>
                        <th>content</th>
                        <th>username</th>
                        <th>like_count</th>
                        <th>retweet_count</th>
                    </tr>
                </thead>
                <tbody>
        """
        for _, row in top_tweets.iterrows():
            html_content += f"""
            <tr>
                <td>{row['date']}</td>
                <td>{row['id']}</td>
                <td>{row['content']}</td>
                <td>{row['username']}</td>
                <td>{row['like_count']}</td>
                <td>{row['retweet_count']}</td>
            </tr>
            """
        html_content += """
                </tbody>
            </table>
        </body>
        </html>
        """

        with open(output_file, "w") as file:
            file.write(html_content)
        print(f"Top Tweets Table saved to {output_file}")
