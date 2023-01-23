import re

def natural_key(string_):
    """From: http://stackoverflow.com/a/3033342 """
    return [int(s) if s.isdigit() else s for s in re.split(r'(\d+)', string_)]

def remove_chars_iter(subj, chars):
    """From: http://stackoverflow.com/a/10017169 """
    sc = set(chars)
    return ''.join([c for c in subj if c not in sc])

def tokenize(text):
    tokenized = re.findall(pattern="\w+", string=text)
    return tokenized
