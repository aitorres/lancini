"""
Corpus module to store helper functions for corpus retrieval,
storage and preprocessing for lancini.
"""

import logging
from pathlib import Path
from typing import Final

SPANISH_WORD_LIST_PATH: Final[Path] = Path(
    "diccionario-espanol-txt/0_palabras_todas.txt"
)
UNWANTED_WORDS: set[str] = {
    "b",
    "c",
    "d",
    "f",
    "g",
    "h",
    "i",
    "j",
    "k",
    "l",
    "m",
    "n",
    "ñ",
    "p",
    "q",
    "r",
    "s",
    "t",
    "v",
    "w",
    "x",
    "z",
}

logger = logging.getLogger()


def preprocess_corpus(corpus: set[str]) -> set[str]:
    """
    Cleans up and deduplicates words from the Spanish corpus.
    """

    logger.info("Preprocessing Spanish corpus...")

    words: set[str] = {
        word
        for word in corpus
        if word.isascii() and word.isalpha() and not word.isnumeric()
    }

    logger.info("Preprocessed Spanish corpus stored successfully!")
    return words - UNWANTED_WORDS


def load_corpus() -> set[str]:
    """
    Loads preprocessed Spanish words from the file system.
    """

    logging.info("Loading corpus...")

    if SPANISH_WORD_LIST_PATH.exists() and SPANISH_WORD_LIST_PATH.is_file():
        with open(SPANISH_WORD_LIST_PATH, "r", encoding="utf-8") as word_list_file:
            return preprocess_corpus(
                {line.strip() for line in word_list_file.readlines()}
            )
    else:
        logging.warning("No corpus (or empty corpus) found!")
        return set()
