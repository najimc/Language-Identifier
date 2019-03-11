# Language Identifier

Identifies the language of a given text and its confidence level using a traning set of 105 different language samples.

Can also be used to identify text of an individual compared to several sample texts of others. Just place the samples in the `languages` folder.

## Instructions

Put the desired text in `text.txt` then use the following command in the terminal ([Python 3](https://www.python.org/downloads/) or higher must be installed):

```bash
python identify_language.py
```

Optional arguments:

```bash
python identify_language.py [-h] [-t TOL] [-f FILE]
```

`-t TOL` sets the tolerance level to tune the results. Default tolerance is `3`.

`-f FILE` sets the text file to be used. Default file is `text.txt`.

`-h` shows the help message and further information.

## Author

- [Najim Islam](https://github.com/najimc)
