from itertools import groupby
from googletrans import Translator

Arabic_LETTERS = ['ا', 'ب', 'ت', 'ث', 'ج', 'ح', 'خ', 'د', 'ذ', 'ر', 'ز', 'س', 'ش', 'ص', 'ض', 'ط', 'ظ', 'ع', 'غ',
                  'ف', 'ق', 'ك', 'ل', 'م', 'ن', 'ه', 'و', 'ي', 'ء']

SINGLES = {
    'a': ['ا'],
    'b': ['ب'],
    't': ['ت'],
    'g': ['ج'],
    'j': ['ج'],
    'd': ['د'],
    'z': ['ذ', 'ز'],
    'r': ['ر'],
    's': ['س'],
    'f': ['ف'],
    'k': ['ك', 'ق'],
    'l': ['ل'],
    'm': ['م'],
    'n': ['ن'],
    'h': ['ح', 'ه'],
    'o': ['و'],
    'w': ['و'],
    'y': ['ي'],
    'e': ['ي'],
    '2': ['ا', 'ء'],
    '3': ['ع'],
    '5': ['خ'],
    '7': ['ح'],
    '8': ['غ']
}

DOUBLES = {
    'aa': ['ع'],
    'th': ['ث'],
    'sh': ['ش'],
    'sa': ['ص'],
    'da': ['ض'],
    'ta': ['ط'],
    'ma': ['م'],
    'fa': ['ف'],
    '2e': ['ا', 'ء']
}


# TODO: Evolve The Lebanese Arabic Translation
class LebaneseToEnglish:
    translator = Translator()

    @staticmethod
    def remove_duplicate(string):
        return "".join([l[0] for l in list(groupby(string))])

    @staticmethod
    def get_lebanese(string):
        size = len(string)
        i = 0
        res = ''
        while i < size:
            double = string[i: i + 2]
            if double in DOUBLES:
                res += DOUBLES[double][0]
                i += 2
                continue
            if string[i] == ' ':
                res += ' '
            if string[i] in SINGLES:
                res += SINGLES[string[i]][0]
            i += 1
        return res

    @staticmethod
    def _parse_translation(translation_obj):
        correction = translation_obj.extra_data['possible-mistakes'][1] if translation_obj.extra_data['possible-mistakes'] else None
        return {
            'original': translation_obj.origin,
            'translated': translation_obj.text,
            'src_lang': translation_obj.src,
            'dest_lang': translation_obj.dest,
            'possible_correction': correction
        }

    @staticmethod
    def _translate(text, src_lang, dest_lang):
        return LebaneseToEnglish._parse_translation(LebaneseToEnglish.translator.translate(text, src=src_lang, dest=dest_lang))

    @staticmethod
    def translate(lebanese_text, src_lang='auto', dest_lang='en'):
        lebanese = LebaneseToEnglish.get_lebanese(lebanese_text)
        pre_translation = LebaneseToEnglish._translate(lebanese, src_lang, dest_lang)
        print(pre_translation['original'])
        print(pre_translation['translated'])
        if not pre_translation['possible_correction']:
            return pre_translation
        else:
            return LebaneseToEnglish._translate(pre_translation['possible_correction'], src_lang, dest_lang)

    @staticmethod
    def batch_translation(lebanese_texts, src_lang='auto', dest_lang='en'):
        res = []
        for text in lebanese_texts:
            res.append(LebaneseToEnglish.translate(text, src_lang, dest_lang))
        return res


if __name__ == '__main__':
    # string = 'sho 2estez kefak lyom nshalla mne7'
    # print(LebaneseToEnglish.translate(string))

    batch = [
        'mar7aba kefak',
        'sho 2estez kefak lyom nshalla mne7',
        'eh walla, mbere7 re7na'
    ]

    for b in batch:
        print(LebaneseToEnglish.get_lebanese(b))

    # res = LebaneseToEnglish.batch_translation(batch)
    # for r in res:
    #     print(r['original'])
    #     print(r['translated'])
    #     print(r['possible_correction'])
    #     print('--------------------------------')
