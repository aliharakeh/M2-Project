from Text_Mining.pre_processing import PreProcessing
from textblob import TextBlob

class TextProcessing:

    def __init__(self, df, text_column):
        self.df = df
        self.text_col = text_column
        # self.extract = PreProcessing(df, text_column)


    def n_grams(self):
        