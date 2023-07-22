"""
Main module of `lancini` with scripts to generate and store
palindromes in the Spanish language.
"""


import logging
import sys
from bz2 import BZ2Decompressor
from pathlib import Path
from typing import Final, Generator

import requests

from lancini.cli import Command, get_parser

SPANISH_WORD_CORPUS_URL: Final[
    str
] = "https://cs.famaf.unc.edu.ar/~ccardellino/SBWCE/SBW-vectors-300-min5.txt.bz2"
SPANISH_WORD_CORPUS_COMPRESSED_PATH: Final[Path] = Path("data/SBW-vectors-300-min5.txt")
SPANISH_WORD_CORPUS_PREPROCESSED_PATH: Final[Path] = Path(
    "data/SBW-vectors-300-min5.preprocessed.txt"
)
PALINDROMES_PATH: Final[Path] = Path("data/palindromes.csv")
MAX_PALINDROME_LENGTH: Final[int] = 10
PALINDROME_BUFFER: Final[int] = 20
VALID_CHARACTERS: Final[str] = "abcdefghijklmnñopqrstuvwxyzáéíóúü"

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


def is_palindrome(phrase: str) -> bool:
    """
    Checks if a phrase is a palindrome.
    """

    return phrase == phrase[::-1]


def load_existing_palindromes() -> set[str]:
    """
    Loads existing palindromes from the file system.
    """

    if PALINDROMES_PATH.exists() and PALINDROMES_PATH.is_file():
        with open(PALINDROMES_PATH, "r", encoding="utf-8") as palindromes_file:
            return {line.strip(",")[0] for line in palindromes_file.readlines()}
    else:
        return set()


def load_corpus() -> set[str]:
    """
    Loads preprocessed Spanish words from the file system.
    """

    if (
        SPANISH_WORD_CORPUS_PREPROCESSED_PATH.exists()
        and SPANISH_WORD_CORPUS_PREPROCESSED_PATH.is_file()
    ):
        with open(
            SPANISH_WORD_CORPUS_PREPROCESSED_PATH, "r", encoding="utf-8"
        ) as corpus_file:
            return {line.strip() for line in corpus_file.readlines()}
    else:
        return set()


def store_palindromes(palindromes: list[tuple[str, str]]) -> None:
    """
    Stores new palindromes to the file system.
    """

    with open(PALINDROMES_PATH, "a", encoding="utf-8") as palindromes_file:
        palindromes_file.writelines(
            [f"{palindrome[0]},{palindrome[1]}\n" for palindrome in palindromes]
        )


def generate_word(length: int) -> Generator[str, None, None]:
    """
    Generates all words of a given length.
    """

    if length == 1:
        for character in VALID_CHARACTERS:
            yield character
    else:
        for word in generate_word(length - 1):
            for character in VALID_CHARACTERS:
                yield word + character


def is_phrase(phrase: str, corpus: set[str]) -> str:
    """
    Checks if a phrase is made of words in the corpus and
    return the phrase.
    """

    for split_length in range(len(phrase), 0, -1):
        if (starting_phrase := phrase[:split_length]) in corpus:
            if starting_phrase == phrase:
                return phrase

            remainder = phrase[split_length:]
            if remainder_phrase := is_phrase(remainder, corpus):
                return f"{starting_phrase} {remainder_phrase}"

    return ""


def generate_palindromes() -> None:
    """
    Performs an exhaustive search to generate palindromes
    by brute force, and stores them to the file system.
    """

    logging.info("Loading corpus...")
    corpus: set[str] = load_corpus()

    if not corpus:
        logging.error("Corpus is empty!")
        sys.exit(1)

    logging.info("Loading existing palindromes...")
    existing_palindromes: set[str] = load_existing_palindromes()

    if existing_palindromes:
        logging.info("Loaded %d existing palindromes!", len(existing_palindromes))
        starting_length = max(len(palindrome) for palindrome in existing_palindromes)
    else:
        logging.info("No existing palindromes found!")
        starting_length = 3

    new_palindromes: list[tuple[str, str]] = []

    logging.info("Generating new palindromes...")
    try:
        for palindrome_length in range(starting_length, MAX_PALINDROME_LENGTH + 1):
            logger.info("Generating palindromes of length %d...", palindrome_length)

            for word in generate_word(palindrome_length):
                if is_palindrome(word):
                    logger.info(
                        "Palindrome found (%s), checking if part of existing palindromes",
                        word,
                    )

                    if word in existing_palindromes:
                        logger.info("Palindrome already stored, skipping...")
                        continue

                    logger.info(
                        "Palindrome (%s) is new, checking if part of corpus", word
                    )

                    if phrase := is_phrase(word, corpus):
                        logger.info("Palindrome (%s) is part of corpus!", word)
                        new_palindromes.append((word, phrase))

                if len(new_palindromes) >= PALINDROME_BUFFER:
                    logger.info("Storing palindromes generated to this point...")
                    store_palindromes(new_palindromes)
                    new_palindromes = []
    finally:
        logger.info("Storing remaining palindromes before exiting...")
        store_palindromes(new_palindromes)


def main() -> None:
    """
    Main function of the package.
    """

    parser = get_parser()
    args = parser.parse_args()
    command: Command = args.command

    match command:
        case Command.SETUP:
            download_corpus()
            preprocess_corpus()
        case Command.GENERATE:
            generate_palindromes()
        case _:
            logger.error("Command not supported!")
            sys.exit(1)


if __name__ == "__main__":
    main()
