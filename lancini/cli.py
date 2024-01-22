"""
Command line interface module to store helper functions
for lancini's CLI
"""

import argparse
from enum import Enum
from typing import Final


class Command(Enum):
    """
    Enumerates all possible commands to be used with lancini's CLI
    """

    GENERATE = "generate"


AVAILABLE_COMMANDS: Final[list[Command]] = list(Command)


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
