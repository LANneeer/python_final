import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
from utils import Strategy
import re
from collections import defaultdict


class TopWordsStrategy(Strategy):
    @staticmethod
    def clean_text_column(df: pd.DataFrame, column: str) -> pd.DataFrame:
        """Clean and tokenize text column in the dataframe."""

        def clean_text(text):
            text = text.lower()  # Convert text to lowercase
            text = re.sub(r"http\\S+|www\\.\\S+", "", text)  # Remove URLs
            text = "".join(
                ch if ch.isalnum() or ch.isspace() else " " for ch in text
            )  # Remove special characters
            tokens = text.split()  # Tokenize text by splitting on whitespace

            # Remove stop words using sklearn's ENGLISH_STOP_WORDS
            tokens = [word for word in tokens if word not in ENGLISH_STOP_WORDS]
            return tokens

        df[column] = df[column].fillna("").apply(clean_text)
        return df

    @staticmethod
    def calculate(df: pd.DataFrame) -> dict:
        """Calculate the top words in the content column."""
        if "content" not in df.columns:
            raise ValueError("The dataframe must contain a 'content' column.")

        # Clean and tokenize the content column
        df = TopWordsStrategy.clean_text_column(df, "content")

        # Explode the tokens into a single DataFrame column
        exploded = df.explode("content")

        # Group by tokens and document IDs and count occurrences
        token_counts = (
            exploded.groupby(["content", exploded.id]).size().reset_index(name="count")
        )

        # Organize the results in dictionary format
        detailed_counts = defaultdict(dict)
        for _, row in token_counts.iterrows():
            word, doc_id, count = row["content"], row["id"], row["count"]
            detailed_counts[word][doc_id] = count

        return {"detailed_counts": detailed_counts}
