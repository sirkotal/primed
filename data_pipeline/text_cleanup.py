import wordninja
import re


def concat_with_punctuation(words):
    string = ""
    punctuation = [',', '.', ';', ':', '\'', '`', '!', '?']
    for idx, word in enumerate(words):
        string += word
        if idx > 0 and idx + 1 < len(words) and words[idx + 1] not in punctuation:
            string += ' '
    return string


def remove_references(string):
    return re.sub(r'\[\d+\]', '', string)


def remove_newlines_and_extra_spaces(string):
    return re.sub(r'\s+', ' ', string).strip()


def repair_string(string):
    string = remove_references(string)
    string = remove_newlines_and_extra_spaces(string)
    words = wordninja.split(string)
    words = list(filter(lambda ch: ch != ' ', words))
    return concat_with_punctuation(words)
