"""
Corpus module to store helper functions for corpus retrieval,
storage and preprocessing for lancini.
"""

import logging
import sys
from bz2 import BZ2Decompressor
from pathlib import Path
from typing import Final

import requests

SPANISH_WORD_CORPUS_URL: Final[
    str
] = "https://cs.famaf.unc.edu.ar/~ccardellino/SBWCE/SBW-vectors-300-min5.txt.bz2"
SPANISH_WORD_CORPUS_COMPRESSED_PATH: Final[Path] = Path("data/SBW-vectors-300-min5.txt")
SPANISH_WORD_CORPUS_PREPROCESSED_PATH: Final[Path] = Path(
    "data/SBW-vectors-300-min5.preprocessed.txt"
)

logger = logging.getLogger()


def download_corpus() -> None:
    """
    Download the Spanish corpus (Spanish Billion Word Corpus and Embeddings)
    if not already present.
    ref: https://crscardellino.ar/SBWCE/
    """

    if (
        SPANISH_WORD_CORPUS_COMPRESSED_PATH.exists()
        and SPANISH_WORD_CORPUS_COMPRESSED_PATH.is_file()
    ):
        logger.info("Spanish corpus already downloaded")
    else:
        logger.info("Downloading Spanish corpus...")
        try:
            response = requests.get(
                SPANISH_WORD_CORPUS_URL, allow_redirects=True, timeout=30
            )
        except requests.exceptions.HTTPError:
            logger.error("HTTP error while downloading Spanish corpus!")
            sys.exit(1)

        data = response.content
        decompressor = BZ2Decompressor()

        logger.info("Storing Spanish corpus to data directory...")
        with open(SPANISH_WORD_CORPUS_COMPRESSED_PATH, "wb") as corpus_file:
            corpus_file.write(decompressor.decompress(data))

        logger.info("Spanish corpus downloaded and stored successfully!")


def preprocess_corpus() -> None:
    """
    Extracts and deduplicates words from the Spanish corpus.
    """

    if (
        SPANISH_WORD_CORPUS_PREPROCESSED_PATH.exists()
        and SPANISH_WORD_CORPUS_PREPROCESSED_PATH.is_file()
    ):
        logger.info("Spanish corpus already preprocessed")
    else:
        logger.info("Preprocessing Spanish corpus...")

        with open(
            SPANISH_WORD_CORPUS_COMPRESSED_PATH, "r", encoding="utf-8"
        ) as corpus_file:
            lines = corpus_file.readlines()[1:]

        words: set[str] = {line.split()[0].lower().strip() for line in lines if line}
        words = {
            word
            for word in words
            if word.isascii() and word.isalpha() and not word.isnumeric()
        }

        logger.info("Storing preprocessed Spanish corpus to data directory...")
        with open(
            SPANISH_WORD_CORPUS_PREPROCESSED_PATH, "w", encoding="utf-8"
        ) as corpus_file:
            corpus_file.writelines([f"{word}\n" for word in sorted(words)])

        logger.info("Preprocessed Spanish corpus stored successfully!")


def load_corpus() -> set[str]:
    """
    Loads preprocessed Spanish words from the file system.
    """

    logging.info("Loading corpus...")

    if (
        SPANISH_WORD_CORPUS_PREPROCESSED_PATH.exists()
        and SPANISH_WORD_CORPUS_PREPROCESSED_PATH.is_file()
    ):
        with open(
            SPANISH_WORD_CORPUS_PREPROCESSED_PATH, "r", encoding="utf-8"
        ) as corpus_file:
            return {line.strip() for line in corpus_file.readlines()}
    else:
        logging.warning("No corpus (or empty corpus) found!")
        return set()
