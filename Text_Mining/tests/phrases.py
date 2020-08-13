from Text_Mining.text_processing import TextProcessing
import pandas as pd

if __name__ == '__main__':
    df = pd.read_csv('..\\..\\Main_Data\\corona_tweets.csv')
    tp = TextProcessing(df, 'text')  # translated_text
    tp.pre_process.remove_non_alphabet()
    # tp.pre_process.remove_stop_words(['Corona', 'Corona_Lebanon', 'Lebanon', 'D9', 'D8', 'd8', 'd9', 'a7', 'A7'])
    # tp.pre_process.lemmatization()
    # tp.pre_process.remove_stop_words(
    #     ['من', 'في', 'و', 'ما', 'على', 'عم', 'كل', 'عن', 'لا', 'يا', 'بعد', 'مش', 'مع', 'بس', 'الله', 'الى', 'اليوم', 'شو', 'يلي', 'ب', 'إلى', 'أن',
    #      'شي', 'انو', 'رح', 'لبنان_ينتفض', 'ولا', 'او', 'اذا', 'ان', 'حتى', 'اللي', 'كان', 'بين', 'التي', 'يوم', 'هذه', 'هو', 'قبل', 'حدا', 'كيف',
    #      'الشعب', 'هذا', 'يعني', 'بفيروس', 'حالة', 'عدد', 'الناس', 'تسجيل', 'كورونا_الجديد', 'إصابات'])
    print(tp.most_frequent_n_grams(n=2, limit=50))

    # df = pd.read_csv('Main_Data\\health_tweets.csv')
    # tp = TextProcessing(df, 'translated_text')
    # tp.pre_process.remove_non_alphabet()
    # tp.pre_process.remove_stop_words()
    # tp.pre_process.lemmatization()
    # print(tp.most_frequent_n_grams(n=3, limit=50))

    # locations = df['location'].unique()[:5]
    # for location in locations:
    #     temp_df = df[df['location'] == location]
    #     tp.df = temp_df
    #     print('[Location]: ', location)
    #     print(list(tp.most_frequent_n_grams(n=2, limit=5).index))
    #     # print(tp.most_frequent_n_grams(n=3, limit=5))
    #     # print(tp.most_frequent_n_grams(n=4, limit=5))
    #     # print(tp.most_frequent_n_grams(n=5, limit=5))
    #     print('----------------------------------------------------')
