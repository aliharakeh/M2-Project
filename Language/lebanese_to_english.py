from .language_utils import LanguageUtil
from .lebanese_to_arabic import LebaneseToArabic
from difflib import SequenceMatcher
import json
import os

DIR = os.path.dirname(__file__)


class LebaneseToEnglish:
    lb_en_dict = None
    lb_words = None

    def __init__(self, lang_util=None):
        self.lang_util = lang_util if lang_util else LanguageUtil()
        self.load_data()
        self.lb_ar = LebaneseToArabic(self.lang_util)

    @classmethod
    def load_data(cls):
        with open(f'{DIR}\\lb_en.json') as f:
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
