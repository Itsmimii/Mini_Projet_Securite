import string

ALPHABET = string.ascii_uppercase

def clean_text(text):
    return ''.join(c for c in text.upper() if c in ALPHABET or c == ' ')

def saveSpacesIndex(text):
    return [i for i, c in enumerate(text) if c == ' ']

def restore_spaces(text, spaces):
    for i in spaces:
        text = text[:i] + ' ' + text[i:]
    return text
