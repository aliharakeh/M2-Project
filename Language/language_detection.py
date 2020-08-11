from Language.Detect_English.detect_english import EnglishDetection
from Language.language_config import AR_REGEX, PROBLEM_CHARS, LB_LETTERS
import re


class BaseLang:
    def __init__(self, text):
        self.text = self.__clean(text)
        self.words = text.split()
        self.word_count = len(self.words)
        self.indexes = []

    def __clean(self, text):
        res = ''
        for ch in text:
            if ch not in PROBLEM_CHARS:
                res += ch
        return res

    def word_percentage(self):
        return 0

    def detect(self):
        return self.word_percentage() >= 80


class AR(BaseLang):

    def __init__(self, text):
        super().__init__(text)
        self.ar_detect = re.compile(AR_REGEX)

    def is_arabic(self, word):
        return re.search(self.ar_detect, word) is not None

    def word_percentage(self):
        ar_count = 0
        for index, word in enumerate(self.words):
            if self.is_arabic(word):
                ar_count += 1
                self.indexes.append(index)
        return (ar_count / self.word_count) * 100


class EN(BaseLang):

    def __init__(self, text):
        super().__init__(text)
        self.en_detect = EnglishDetection()

    def is_english(self, word):
        return word.upper() in self.en_detect.ENGLISH_WORDS

    def word_percentage(self):
        percent, indexes = self.en_detect.get_english_count(self.text)
        self.indexes = indexes
        return percent * 100


class LB(BaseLang):

    def __init__(self, text, ar=None, en=None):
        super().__init__(text)
        self.ar = ar if ar else AR(text)
        self.en = en if en else EN(text)

    def is_lebanese(self, word):
        word = word.lower()
        if not self.ar.is_arabic(word) and not self.en.is_english(word):
            for ch in word:
                if ch not in LB_LETTERS:
                    return False
            return True
        return False

    def word_percentage(self):
        lb_count = 0
        for index, word in enumerate(self.words):
            if self.is_lebanese(word):
                lb_count += 1
                self.indexes.append(index)
        return (lb_count / self.word_count) * 100


class LangDetector:
    def __init__(self, text):
        text = text.lower()
        self.ar = AR(text)
        self.en = EN(text)
        self.lb = LB(text, ar=self.ar, en=self.en)
        self.langs = [
            {'name': 'AR', 'class': self.ar},
            {'name': 'EN', 'class': self.en},
            {'name': 'LB', 'class': self.lb},
        ]

    def detect(self):
        for lang in self.langs:
            detected = lang['class'].detect()
            if detected:
                return lang['name']
        return None

    def lang_percentage(self):
        res = {}
        for lang in self.langs:
            res[lang['name']] = lang['class'].word_percentage()
        return res

    def lang_distribution(self):
        res = {}
        for lang in self.langs:
            res[lang['name']] = {
                'percentage': lang['class'].word_percentage(),
                'indexes': lang['class'].indexes
            }
        return res


if __name__ == '__main__':
    l = LangDetector('Hello Kefak')
    print(l.lang_distribution())
    print(l.lang_percentage())
