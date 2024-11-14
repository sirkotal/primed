import wordninja
import re


def split_midword_uppercase(word):
    i = 0
    while i < len(word):
        # For cases where the previous character is also uppercase I assume it's a sequence of initials
        # (don't break it)
        if word[i].isupper() and i - 1 >= 0 and word[i - 1] != ' ' and word[i - 1].islower(): 
            word = word[0:i] + ' ' + word[i:len(word)] 
        i += 1
    return word


def concat_with_punctuation(words):
    string = ""
    no_space_on_either_side = ['-', '/']
    no_space_on_right_side = ['[', '(', '{'] + no_space_on_either_side
    no_space_on_left_side = [']', ')', '}', ',', '.', ';', ':', '\'', '`', '!', '?'] + no_space_on_either_side
    for idx, word in enumerate(words):
        string += word
        if idx > 0 and idx + 1 < len(words) \
            and words[idx + 1] not in no_space_on_left_side \
            and words[idx] not in no_space_on_right_side:
            string += ' '
        elif idx == 0 and words[idx] not in no_space_on_right_side:
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
    return split_midword_uppercase(concat_with_punctuation(words))
