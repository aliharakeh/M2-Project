from googletrans import Translator
import json
from difflib import SequenceMatcher

SPACES = ' \t\n'
ARABIC_LETTERS = 'ابتثجحخدذرزسشصضطظعغفقكلمنهويء'
ENGLISH_LETTERS = 'abcdefghijklmnopqrstuvwxyz'
LEBANESE_LETTERS = ENGLISH_LETTERS + '23578' + SPACES
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


class LebaneseToArabic:
    lang_util = LanguageUtil()

    @staticmethod
    def remove_non_letters(string):
        letters_only = []
        for char in string:
            if char in LEBANESE_LETTERS:
                letters_only.append(char)
        return ''.join(letters_only)

    @classmethod
    def lb_to_ar(cls, lb_text):
        lb_text = cls.remove_non_letters(lb_text)
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

    @classmethod
    def translate(cls, text):
        arabic = cls.lb_to_ar(text)
        correction = cls.lang_util.quick_translation(arabic)['possible_correction']
        if correction:
            return correction
        return arabic


class LebaneseToEnglish:
    lang_util = LanguageUtil()

    @staticmethod
    def remove_non_letters(string):
        string = string.lower()
        letters_only = []
        for char in string:
            if char in LEBANESE_LETTERS:
                letters_only.append(char)
        return ''.join(letters_only)

    @classmethod
    def lb_to_en(cls, text):
        pass

    @classmethod
    def translate(cls, text):
        pass


class LebaneseLanguage:

    def __init__(self):
        self.lb_en_dict = None
        self.lb_words = None
        self.lang_util = LanguageUtil()
        self.load_data()

    def load_data(self):
        with open('lb_en.json') as f:
            data = json.loads(f.read())
        self.lb_en_dict = data
        self.lb_words = list(data.keys())

    def search_word(self, word):
        word = word.lower()
        best_match = (None, None)
        for lb_word in self.lb_words:
            if lb_word.lower() == word:
                best_match = (lb_word, 1.0)
                break
            similarity = SequenceMatcher(None, lb_word, word).ratio()
            if not best_match[0] or similarity >= best_match[1]:
                best_match = (lb_word, similarity)
        return {
            'searched': word,
            'matched_lb': best_match[0],
            'matched_en': self.lb_en_dict[best_match[0]],
            'similarity': best_match[1]
        }

    def pre_process_text(self, text):
        pass

    def lebanese_to_arabic(self, text):
        text = self.pre_process_text(text)
        return LebaneseToArabic.translate(text)

    def lebanese_to_english(self, text):
        text = self.pre_process_text(text)
        return LebaneseToEnglish.translate(text)


if __name__ == '__main__':
    texts = [
        'mar7aba',
        'salam kefak',
        'eh walla knt honek bas ma sar shi'
    ]
    for text in texts:
        print(LebaneseToArabic.translate(text))
