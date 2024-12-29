import pandas as pd

import plotly.express as px
from utils import Strategy


class TopTweetsStrategy(Strategy):
    @staticmethod
    def calculate(df: pd.DataFrame) -> dict:
        """Calculate and construct a tops of tweets: by likes, by retweets and by popularity (general top)"""

        top_likes = df.copy().sort_values("like_count", ascending=False).head(20)
        top_likes = top_likes[0:20]

        top_retweets = df.copy().sort_values("retweet_count", ascending=False).head(20)

        # while calculating popularity values, like weights 1 point and retweet weights 10 points
        top_general = df.copy()
        top_general["popularity"] = top_general["like_count"] + 10 * top_general["retweet_count"]
        top_general = top_general.sort_values("popularity", ascending=False).head(20)

        return {
            "top_likes": top_likes.to_dict(orient="records"),
            "top_retweets": top_retweets.to_dict(orient="records"),
            "top_general": top_general.to_dict(orient="records"),
        }

    @staticmethod
    def generate_html(data, output_files=("top_tweets_likes.html", "top_tweets_retweets.html", "top_tweets_populatiry.html")):
        """Generate an HTML file for top tweets by likes and retweets."""

        html_content = f"""
        <html>
        <head>
            <title>Top Popular Tweets by Likes</title>
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
                <caption>Top Popular Tweets by Likes</caption>
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
        for tweet in data['top_likes']:
            html_content += f"""
                    <tr>
                        <td>{tweet['date']}</td>
                        <td>{tweet['id']}</td>
                        <td>{tweet['content']}</td>
                        <td>{tweet['username']}</td>
                        <td>{tweet['like_count']}</td>
                        <td>{tweet['retweet_count']}</td>
                    </tr>
            """
        html_content += """
                </tbody>
            </table>
        </body>
        </html>
        """

        with open(output_files[0], "w") as file:
            file.write(html_content)
        print(f"Top Tweets Table saved to {output_files[0]}")

        html_content = f"""
                <html>
                <head>
                    <title>Top Popular Tweets by Retweets</title>
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
                        <caption>Top Popular Tweets by Retweets</caption>
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
        for tweet in data['top_retweets']:
            html_content += f"""
                            <tr>
                                <td>{tweet['date']}</td>
                                <td>{tweet['id']}</td>
                                <td>{tweet['content']}</td>
                                <td>{tweet['username']}</td>
                                <td>{tweet['like_count']}</td>
                                <td>{tweet['retweet_count']}</td>
                            </tr>
                    """
        html_content += """
                        </tbody>
                    </table>
                </body>
                </html>
                """

        with open(output_files[1], "w") as file:
            file.write(html_content)
        print(f"Top Tweets Table saved to {output_files[1]}")

        html_content = f"""
                <html>
                <head>
                    <title>Top Popular Tweets by Popularity</title>
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
                        <caption>Top Popular Tweets by Popularity</caption>
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
        for tweet in data['top_retweets']:
            html_content += f"""
                            <tr>
                                <td>{tweet['date']}</td>
                                <td>{tweet['id']}</td>
                                <td>{tweet['content']}</td>
                                <td>{tweet['username']}</td>
                                <td>{tweet['like_count']}</td>
                                <td>{tweet['retweet_count']}</td>
                            </tr>
                            """
        html_content += """
                        </tbody>
                    </table>
                </body>
                </html>
                """

        with open(output_files[2], "w") as file:
            file.write(html_content)
        print(f"Top Tweets Table saved to {output_files[2]}")
