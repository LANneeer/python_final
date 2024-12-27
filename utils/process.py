from abc import ABC, abstractmethod
import pandas as pd


class Strategy(ABC):
    @abstractmethod
    def calculate(df: pd.DataFrame) -> dict:
        raise NotImplementedError


class Context:
    def __init__(self, df) -> None:
        self.df = df

    def execute(self, strategy: Strategy):
        return strategy.calculate(self.df)

