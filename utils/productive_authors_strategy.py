class ProductiveAuthorsStrategy:
    @staticmethod
    def calculate(df) -> dict:
        productivity_df = df.groupby('username').size().reset_index(name='post_count').sort_values('post_count', ascending=False)

        return productivity_df[0:30]