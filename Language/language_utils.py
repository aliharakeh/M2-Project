from googletrans import Translator


class LanguageUtil:

    def __init__(self):
        self.translator = Translator()

    def quick_lang_detect(self, text):
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
