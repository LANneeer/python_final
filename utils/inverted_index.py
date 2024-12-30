import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
from utils import Strategy
import re
from collections import defaultdict
import plotly.express as px


class TopWordsStrategy(Strategy):
    @staticmethod
    def clean_text_column(df: pd.DataFrame, column: str) -> pd.DataFrame:
        """
        Clean and tokenize text column in the dataframe.
        Time complexity: O(n * m), where n is the number of rows in the DataFrame and m is the length of text in the column.
        Space complexity: O(n * m), for storing tokenized words in memory.
        """

        def clean_text(text):
            text = text.lower()  # Convert text to lowercase
            text = re.sub(r"http|s\S+|www\.\S+", "", text)  # Remove URLs
            text = "".join(
                ch if ch.isalnum() or ch.isspace() or ch == r"'" else " " for ch in text
            )  # Remove special characters
            tokens = text.split()  # Tokenize text by splitting on whitespace

            tokens = [word for word in tokens if word not in ENGLISH_STOP_WORDS]
            particles_and_articles = {
                "1",
                "2",
                "3",
                "4",
                "5",
                "just",
                "use",
                "t",
                "s",
                "it's",
                "u",
            }
            tokens = [word for word in tokens if word not in particles_and_articles]
            return tokens

        df[column] = df[column].fillna("").apply(clean_text)
        return df

    @staticmethod
    def calculate(df: pd.DataFrame) -> dict:
        """
        Calculate the top words in the 'content' column.
        Time complexity: O(n * m), where n is the number of rows, m is the average length of text.
        Space complexity: O(n * m), where n * m is for tokenized content.
        """
        if "content" not in df.columns:
            raise ValueError("The dataframe must contain a 'content' column.")

        # Clean and tokenize the content column
        df_copy = df.copy()
        TopWordsStrategy.clean_text_column(df_copy, "content")

        # Explode the tokens into a single DataFrame column
        exploded = df_copy.explode("content")

        # Group by tokens and count occurrences
        token_counts = exploded["content"].value_counts().to_dict()

        # Sort by frequency
        top_words = sorted(
            tuple(token_counts.items()), key=lambda x: x[1], reverse=True
        )

        # Add top 20 words as a list to the existing DataFrame
        top_20_words = [word for word, _ in top_words[:150]][:20]
        df["contains_top_words"] = df_copy["content"].apply(
            lambda tokens: [word for word in tokens if word in top_20_words]
        )

        return {"inverted_index": top_words}

    @staticmethod
    def generate_html(top_words: dict, output_file="top_words.html"):
        """Generate an HTML file for top words pie chart."""
        labels = [word for word, _ in top_words[:20]]
        values = [count for _, count in top_words[:20]]

        fig = px.pie(names=labels, values=values, title="Top Keywords in Tweets")
        fig.write_html(output_file)
        print(f"Top Words Pie Chart saved to {output_file}")
