import spacy

@spacy.registry.callbacks("customize_language_data")
def create_callback():
    def customize_language_data(lang_cls):
        lang_cls.Defaults.infixes = lang_cls.Defaults.infixes + [r'[!&:,\(\)\.]']
        return lang_cls
    return customize_language_data