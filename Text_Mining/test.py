from Text_Mining.info_extraction import InfoExtraction
import pandas as pd
from googletransx import Translator

if __name__ == '__main__':
    # df = pd.read_csv('..\Data\sentimental_analysis\dummy_locations\corona_tweets.csv', header=0)
    # info = InfoExtraction(df, 'translated_text')

    # print(info.word_count())
    # print(info.char_count())
    # print(info.average_word_length())
    # print(info.stopwords_count())
    # print(info.special_chars_count())
    # print(info.numeric_count())
    # print(info.most_frequent_words(limit=20))
    # print(info.most_rare_words(limit=20))

    t = Translator()
    print(t.translate('mar7aba kefk').text)
