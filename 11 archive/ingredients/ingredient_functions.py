import spacy

# Clean ingredients from stop words
def _filter(token, only_nouns):
    if len(token) < 2:
        return False
    if token.is_stop:
        return False
    if only_nouns:
        if token.text[0].islower(): # Schmeisst alle kleingeschriebenen Wörter raus -- gut? Alternative?
            return False
    if token.is_digit:
        return False
    if token.like_num:
        return False
    return True


def _clean(text):
    text = text.replace("(", "")
    text = text.split("/")[0]
    return text


# def normalize(token, lowercase, lemma, remove_stopwords):
    # Make lowercase
    # if lowercase:
    #     token. 

    # Lemmatize
    # if lemma:
    
    # Remove puncts --> is it included in stop words?

    # return 