from googletrans import Translator
from Scrapping.chrome import ChromeManager
import time


class ChromeTranslate:

    def __init__(self):
        self._cm = ChromeManager()
        self._cm.load_page('https://translate.google.com/', '#source')

    def translate(self, text):
        self._cm.set_value('#source', text)
        time.sleep(3)
        return self._cm.get_value('span.tlid-translation.translation')

    def close(self):
        self._cm.close()


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

    def chrome_translate(self, text):
        t = ChromeTranslate()
        try:
            return {
                'original': text,
                'translated': t.translate(text),
                'src_lang': 'auto-detect',
                'dest_lang': 'en'
            }
        except:
            return {
                'original': text,
                'translated': None,
                'src_lang': None,
                'dest_lang': None
            }
