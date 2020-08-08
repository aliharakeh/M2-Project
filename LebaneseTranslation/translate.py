from googletrans import Translator
import json
from difflib import SequenceMatcher
import os

SPACES = ' \t\n'
AR_LETTERS = 'ابتثجحخدذرزسشصضطظعغفقكلمنهويء'
EN_LETTERS = 'abcdefghijklmnopqrstuvwxyz'
LB_LETTERS = EN_LETTERS + '23578' + SPACES
LB_SINGLES = {
    'a': 'ا',
    'b': 'ب',
    't': 'ت',
    'g': 'ج',
    'j': 'ج',
    'd': 'د',
    'z': 'ز',
    'r': 'ر',
    's': 'س',
    'f': 'ف',
    'q': 'ق',
    'k': 'ك',
    'l': 'ل',
    'm': 'م',
    'n': 'ن',
    'h': 'ه',
    'o': 'و',
    'w': 'و',
    'y': 'ي',
    'e': 'ي',
    'i': 'ي',
    '2': 'ء',
    '3': 'ع',
    '5': 'خ',
    '7': 'ح',
    '8': 'غ'
}
LB_DOUBLES = {
    'aa': 'ع',
    'th': 'ث',
    'sh': 'ش',
    'sa': 'ص',
    'da': 'ض',
    'ta': 'ط',
    'fa': 'ف',
    '2e': 'ء',
    'eh': 'اي',
    'en': 'ين',
    'll': 'لا'
}
DIR = os.path.dirname(__file__)


class LanguageUtil:

    def __init__(self):
        self.translator = Translator()

    def detect_language(self, text):
        return self.translator.translate(text).src

    def quick_translation(self, text, src_lang='auto', dest_lang='en'):
        translation = self.translator.translate(text, src=src_lang, dest=dest_lang)
        correction = translation.extra_data['possible-mistakes'][1] if translation.extra_data['possible-mistakes'] else None
        return {
            'original': translation.origin,
            'translated': translation.text,
            'src_lang': translation.src,
            'dest_lang': translation.dest,
            'possible_correction': correction
        }

    def translate(self, text, src_lang='auto', dest_lang='en'):
        translation = self.quick_translation(text, src_lang, dest_lang)
        if translation['possible_correction']:
            translation = self.translator.translate(translation['possible_correction'], src=src_lang, dest=dest_lang)
        return {
            'original': translation.origin,
            'translated': translation.text,
            'src_lang': translation.src,
            'dest_lang': translation.dest
        }


def remove_non_letters(string):
    letters_only = []
    for char in string:
        if char in LB_LETTERS:
            letters_only.append(char)
    return ''.join(letters_only)


class LebaneseToArabic:

    def __init__(self, lang_util=None):
        self.lang_util = lang_util if lang_util else LanguageUtil()

    def __lb_to_ar(self, lb_text):
        lb_text = remove_non_letters(lb_text)
        size = len(lb_text)
        i = 0
        ar_text = ''
        while i < size:
            double = lb_text[i: i + 2]
            if double in LB_DOUBLES:
                ar_text += LB_DOUBLES[double]
                i += 2
                continue
            if lb_text[i] in LB_SINGLES:
                ar_text += LB_SINGLES[lb_text[i]]
            else:
                ar_text += lb_text[i]
            i += 1
        return ar_text

    def lb_to_ar(self, text):
        arabic = self.__lb_to_ar(text)
        correction = self.lang_util.quick_translation(arabic)['possible_correction']
        if correction:
            return correction
        return arabic


class LebaneseToEnglish:
    lb_en_dict = None
    lb_words = None

    def __init__(self, lang_util=None):
        self.lang_util = lang_util if lang_util else LanguageUtil()
        self.load_data()
        self.lb_ar = LebaneseToArabic(self.lang_util)

    @classmethod
    def load_data(cls):
        with open(f'{DIR}\\lb_en_v2.json') as f:
            data = json.loads(f.read())
        cls.lb_en_dict = data
        cls.lb_words = list(data.keys())

    @classmethod
    def search_word(cls, word, stop_ratio=0.8):
        word = word.lower()
        best_match = (word, 0.0)
        if word in cls.lb_en_dict:
            best_match = (word, 1.0)
        else:
            for lb_word in cls.lb_words:
                similarity = SequenceMatcher(None, lb_word, word).ratio()
                if not best_match[0] or similarity >= best_match[1]:
                    best_match = (lb_word, similarity)
                    if similarity >= stop_ratio:
                        break
        return {
            'searched': word,
            'matched_lb': best_match[0],
            'matched_en': cls.lb_en_dict[best_match[0]],
            'similarity': best_match[1]
        }

    def _ar_to_en(self, text):
        return self.lang_util.quick_translation(self.lb_ar.lb_to_ar(text))['translated']

    def lb_to_en(self, text, accepted_similarity=0.8):
        words = text.lower().split()
        res = ''
        for word in words:
            search = self.search_word(word)
            if search['similarity'] >= accepted_similarity:
                res += search['matched_en']
            else:
                res += self._ar_to_en(word)
            res += ' '
        return res[:-1]


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
