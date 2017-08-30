"""Generate Markov text from text files."""

from random import choice
import sys


def open_and_read_file(file_path):
    """Take file path as string; return text as string.

    Takes a string that is a file path, opens the file, and turns
    the file's contents as one string of text.
    """

    with open(file_path) as text:
        return text.read()


def make_chains(text_string, n, chains):
    """Take input text as string; return dictionary of Markov chains.

    A chain will be a key that consists of a tuple of (word1, word2)
    and the value would be a list of the word(s) that follow those two
    words in the input text.

    For example:

        >>> chains = make_chains("hi there mary hi there juanita")

    Each bigram (except the last) will be a key in chains:

        >>> sorted(chains.keys())
        [('hi', 'there'), ('mary', 'hi'), ('there', 'mary')]

    Each item in chains is a list of all possible following words:

        >>> chains[('hi', 'there')]
        ['mary', 'juanita']

        >>> chains[('there','juanita')]
        [None]
    """

    # chains = {}

    words = text_string.split()

    for i in range(len(words) - n):
        n_gram = tuple(words[i:i+n])
        chains[n_gram] = chains.get(n_gram, []) + [words[i+n]]

    return chains


def make_text(chains, capital_words=True, new_lines=False):
    """Return text from chains."""

    words = []

    # Chooses a random n gram from n grams that start with capital letters.
    if capital_words:
        capital_words = [word_tuple for word_tuple in chains.keys() if
                         word_tuple[0] == word_tuple[0].capitalize()]
        starting_n_gram = choice(capital_words)
    else:
        starting_n_gram = choice(chains.keys())

    total = 0
    while True:
        try:
            # Chooses next word from words that follow n gram
            next_word = choice(chains[starting_n_gram])
        except KeyError:
            words += list(starting_n_gram)
            break

        # Adds first word in tuple to list of words
        if new_lines:
            if (starting_n_gram[0] == starting_n_gram[0].capitalize() and
                starting_n_gram[0][0] != "I"):
                    words += "\n"
        words += [starting_n_gram[0]]

        #only adds words if the length is less than 140 characters
        if total + len(starting_n_gram[0]) + 1 > 140:
            break
        else:
            total += len(starting_n_gram[0]) + 1

        # Updates n gram
        starting_n_gram = starting_n_gram[1:] + (next_word,)

        # #added in to stop infinite loops
        # if len(words) > 1000:
        #     break

    return " ".join(words)


def markov():
    chains = {}
    input_text = ""
    for arg in sys.argv[2:]:
        input_path = arg

        # Open the file and turn it into one long string
        input_text = open_and_read_file(input_path)

        # Get a Markov chain
        chains = make_chains(input_text, int(sys.argv[1]), chains)

    # Produce random text
    random_text = make_text(chains, capital_words=False)

    print random_text

# markov()
