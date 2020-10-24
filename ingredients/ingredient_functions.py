import spacy

# Clean ingredients from stop words
def _filter(token):
    if len(token) < 2:
        return False
    if token.is_stop:
        return False
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