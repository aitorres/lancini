"""
Zaloma es una palabra de 6 letras que tiene la propiedad de que si se le
quitan las dos primeras letras y se las ponen al final, se obtiene otra
palabra de 6 letras, y además, si se le quitan las cuatro primeras letras
y se las ponen al final, se obtiene otra palabra de 6 letras.

Zaloma is a word of 6 letters that has the property that if you remove the
first two letters and put them at the end, you get another word of 6 letters,
and also, if you remove the first four letters and put them at the end, you
get another word of 6 letters.
"""

import logging

from lancini.corpus import load_corpus

logger = logging.getLogger()


def generate_zaloma() -> None:
    """
    Generates all zalomas.
    """

    words: set[str] = load_corpus()
    words_len_6 = [word for word in words if len(word) == 6]

    for i, word_1 in enumerate(words_len_6):
        for j, word_2 in enumerate(words_len_6[i:], i):
            for word_3 in words_len_6[j:]:
                if (
                    word_1[2:4] == word_2[:2]
                    and word_1[4:] == word_3[:2]
                    and word_2[4:] == word_3[2:4]
                ):
                    logger.info(
                        "Zaloma found:\n\t%s\n\t%s\n\t%s", word_1, word_2, word_3
                    )
