from .lebanese_to_arabic import LebaneseToArabic
from .lebanese_to_english import LebaneseToEnglish

if __name__ == '__main__':
    texts = [
        'mar7aba',
        'salam kefak',
        'eh walla knt honek bas ma sar shi',
        'wasfi men edoctoor'
    ]
    lb_en = LebaneseToEnglish()
    for text in texts:
        print(text, ' ==> ', lb_en.lb_to_en(text))
