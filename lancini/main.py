"""
Main module of `lancini` with scripts to generate and store
palindromes in the Spanish language.
"""

import argparse
import logging
import sys
from bz2 import BZ2Decompressor
from enum import Enum
from pathlib import Path
from typing import Final

import requests


class Command(Enum):
    """
    Enumerates all possible commands to be used with lancini's CLI
    """

    SETUP = "setup"


AVAILABLE_COMMANDS: Final[list[Command]] = list(Command)
SPANISH_WORD_CORPUS_URL: Final[
    str
] = "https://cs.famaf.unc.edu.ar/~ccardellino/SBWCE/SBW-vectors-300-min5.txt.bz2"
SPANISH_WORD_CORPUS_COMPRESSED_PATH: Final[Path] = Path("data/SBW-vectors-300-min5.txt")
SPANISH_WORD_CORPUS_PREPROCESSED_PATH: Final[Path] = Path(
    "data/SBW-vectors-300-min5.preprocessed.txt"
)

logger = logging.getLogger()


def get_parser() -> argparse.ArgumentParser:
    """
    Generate and return a parser for the CLI tool
    """

    parser = argparse.ArgumentParser(
        prog="lancini",
        description=(
            "A CLI tool to generate and store palindromes in the Spanish language."
        ),
        epilog="¡Yo sonoro no soy! :-)",
    )
    parser.add_argument(
        "command",
        metavar="COMMAND",
        type=Command,
        choices=AVAILABLE_COMMANDS,
        help=(
            "Command to use. "
            f"Supported values are {', '.join(str(AVAILABLE_COMMANDS))}."
        ),
    )
    return parser


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
        case _:
            logger.error("Command not supported!")
            sys.exit(1)


if __name__ == "__main__":
    main()
