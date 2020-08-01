from googletrans import Translator
from Detect_English.detect_english import EnglishDetection
from textblob import Word


class LebaneseToEnglish:
    translator = Translator()
    Arabic_LETTERS = ['ا', 'ب', 'ت', 'ث', 'ج', 'ح', 'خ', 'د', 'ذ', 'ر', 'ز', 'س', 'ش', 'ص', 'ض', 'ط', 'ظ', 'ع', 'غ',
                      'ف', 'ق', 'ك', 'ل', 'م', 'ن', 'ه', 'و', 'ي', 'ء']
    SINGLES = {
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
        '2': 'ء',
        '3': 'ع',
        '5': 'خ',
        '7': 'ح',
        '8': 'غ'
    }
    DOUBLES = {
        'aa': 'ع',
        'th': 'ث',
        'sh': 'ش',
        'sa': 'ص',
        'da': 'ض',
        'ta': 'ط',
        'ma': 'م',
        'fa': 'ف',
        '2e': 'ء',
        'en': 'ين'
    }

    @classmethod
    def en_lb_to_ar_lb(cls, text):
        size = len(text)
        i = 0
        res = ''
        while i < size:
            double = text[i: i + 2]
            if double in cls.DOUBLES:
                res += cls.DOUBLES[double]
                i += 2
                continue
            if text[i] == ' ':
                res += ' '
            if text[i] in cls.SINGLES:
                res += cls.SINGLES[text[i]]
            i += 1
        return res

    @classmethod
    def split_mixed_langs(cls, text):
        words = text.split()
        english = []
        arabic = []
        for word in words:
            if len(word) < 3 and EnglishDetection.detect_english(word):
                english.append(word)
                continue
            if len(word) >= 3 and Word(word).detect_language() == 'en':
                english.append(word)
            else:
                arabic.append(cls.en_lb_to_ar_lb(word))
        return " ".join(english), " ".join(arabic)

    @classmethod
    def _translate(cls, text, src_lang, dest_lang):
        translation = cls.translator.translate(text, src=src_lang, dest=dest_lang)
        correction = translation.extra_data['possible-mistakes'][1] if translation.extra_data['possible-mistakes'] else None
        return {
            'original': translation.origin,
            'translated': translation.text,
            'src_lang': translation.src,
            'dest_lang': translation.dest,
            'possible_correction': correction
        }

    @classmethod
    def translate(cls, text, src_lang='auto', dest_lang='en'):
        english, arabic = cls.split_mixed_langs(text)
        if arabic:
            arabic = cls._translate(arabic, src_lang, dest_lang)
            if arabic['possible_correction']:
                print(arabic['possible_correction'])
                arabic = cls._translate(arabic['possible_correction'], src_lang, dest_lang)['translated']
        res = []
        if english:
            res.append(english)
        if arabic:
            res.append(arabic)
        return " ".join(res)

    @classmethod
    def batch_translation(cls, lebanese_texts, src_lang='auto', dest_lang='en'):
        res = []
        for text in lebanese_texts:
            t = cls._translate(text, src_lang, dest_lang)
            if t['possible_correction']:
                res.append(cls._translate(t['possible_correction'], src_lang, dest_lang))
            else:
                res.append(t)
        return res


if __name__ == '__main__':
    # string = 'sho 2estez kefak lyom nshalla mne7'
    # print(LebaneseToEnglish.translate(string))

    # batch = [
    #     'mar7aba kefak',
    #     'sho 2estez kefak lyom nshalla mne7',
    #     'eh walla, mbere7 re7na'
    # ]
    #
    # for b in batch:
    #     print(LebaneseToEnglish.en_lb_to_ar_lb(b))

    # res = LebaneseToEnglish.batch_translation(batch)
    # for r in res:
    #     print(r['original'])
    #     print(r['translated'])
    #     print(r['possible_correction'])
    #     print('--------------------------------')

    text = 'This is not acceptable 3ashen ken fe y2ol 2nno howe msh hon'
    # print(LebaneseToEnglish.split_mixed_langs(text))
    # print(LebaneseToEnglish.translate(text))
    en, ar = LebaneseToEnglish.split_mixed_langs(text)
    print(ar)
    # ts = LebaneseToEnglish.translate(ar)
    # res = []
    # for t in ts:
    #     print(t)
    #     res.append(t['translated'])
    # print(" ".join(res))
    # print(EnglishDetection.get_english_count('is'))
    # print(EnglishDetection.get_english_count('3ashen'))
    # print(EnglishDetection.get_english_count('ken'))
    # print(EnglishDetection.get_english_count('howe'))

    # from textblob import Word
    # w = Word('hello')
    # l = w.detect_language()
    # print(l == 'en')
    # print(type(l))