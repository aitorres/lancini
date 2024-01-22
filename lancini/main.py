"""
Main module of `lancini` with scripts to generate and store
palindromes in the Spanish language.
"""


import logging
import sys
from os import makedirs
from pathlib import Path
from typing import Final, Generator

from lancini.cli import Command, get_parser
from lancini.corpus import load_corpus
from lancini.zaloma import generate_zaloma

PALINDROMES_PATH: Final[Path] = Path("data/palindromes.csv")
MAX_PALINDROME_LENGTH: Final[int] = 10
PALINDROME_BUFFER: Final[int] = 20
VALID_CHARACTERS: Final[str] = "abcdefghijklmnñopqrstuvwxyzáéíóúü"

logger = logging.getLogger()


def is_palindrome(phrase: str) -> bool:
    """
    Checks if a phrase is a palindrome.
    """

    return phrase == phrase[::-1]


def load_existing_palindromes() -> set[str]:
    """
    Loads existing palindromes from the file system.
    """

    makedirs(PALINDROMES_PATH.parent, exist_ok=True)

    if PALINDROMES_PATH.exists() and PALINDROMES_PATH.is_file():
        with open(PALINDROMES_PATH, "r", encoding="utf-8") as palindromes_file:
            return {line.strip(",")[0] for line in palindromes_file.readlines()}
    else:
        return set()


def store_palindromes(palindromes: list[tuple[str, str]]) -> None:
    """
    Stores new palindromes to the file system.
    """

    with open(PALINDROMES_PATH, "a+", encoding="utf-8") as palindromes_file:
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


def is_relevant_phrase(phrase: str, corpus: set[str]) -> str:
    """
    Checks if a phrase is made of words in the corpus and
    is interesting, and return the phrase.
    """

    phrase = is_phrase(phrase, corpus)

    if phrase:
        if len(phrase.split()) == len("".join(phrase.split())):
            logger.info(
                "Palindrome made out of single letters "
                "or one letter words, skipping..."
            )
            return ""

    return phrase


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


def generate_palindromes(corpus: set[str]) -> None:
    """
    Performs an exhaustive search to generate palindromes
    by brute force, and stores them to the file system.
    """

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

                    if phrase := is_relevant_phrase(word, corpus):
                        logger.info(
                            "Palindrome (%s) is part of corpus with phrase (%s)!",
                            word,
                            phrase,
                        )

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
        case Command.GENERATE:
            corpus: set[str] = load_corpus()
            generate_palindromes(corpus)
        case Command.ZALOMA:
            generate_zaloma()
        case _:
            logger.error("Command not supported!")
            sys.exit(1)


if __name__ == "__main__":
    main()
