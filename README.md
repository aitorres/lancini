# Lancini

Let's find all Spanish palindromes!

Lancini is a set of Python scripts to generate and store palindromes in the Spanish language, currently in development.

## Installation

Clone this repository with the recursive flag (to fetch submodules) and use [poetry](https://python-poetry.org/)[^1] to install the package:

```bash
git clone --recursive https://github.com/aitorres/lancini.git
cd lancini
poetry install
```

[^1]: You need __poetry__ to find palindromes, isn't it beautiful? By the way, this project is inspired by (and name after) Darío Lancini, a Venezuelan writer famous for his work exploring palindromes in fiction and poetry.

## Usage

You can use the `lancini` script as the entry point. `lancini` currently supports two commands: `setup` to download and preprocess the Spanish corpus (publicly-available) and `generate` to generate palindromes.

```bash
lancini setup
lancini generate
```

It's useful to note that:

- The `setup` process only needs to be done once
- All data (corpus and output) will be stored to a `data` folder inside the project
- `lancini generate` can be interrupted and run again as it stores all found palindromes continuously (in batches), and will not store any duplicate palindromes on re-runs.
- Palindromes will be stored within a `csv` file with two columns: the generated "palindrome" (no space between words) and the corresponding phrase in Spanish as it was matched in the corpus.
- Note that it's plausible that a generated palindrome has more than one associated phrase, but the tool only generates the longest one. Try to break down palindrome phrases if you suspect it's possible ;-)

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

This project is licensed under the [GNU Affero General Public License v3.0](https://github.com/aitorres/lancini/blob/main/LICENSE).
