# Zechy Wong
# 10 May 2017
# Code-switching parser
# ---------------------
# Class for dealing with raw input and turning them into lexical items (i.e.,
# syntactic objects)

import itertools
import string

import config


def enumerate_input(user_input):
    """
    Given some input from the user, possibly an incomplete sentence, 
    attempt to tokenise and identify relevant lexical items from the 
    lexicons, then generate all possible combinations of the SOs retrieved
    :param user_input: 
    :return: 
    """
    # Start by tokenising
    tokens = tokenise(user_input)

    # Look up the tokens in the available lexica
    mapped_tokens = lookup_tokens(tokens)
    if not mapped_tokens:
        # Probably an OOV item
        return False

    # Generate combinations of possible parses
    raw_parse_arrays = [list(x) for x in itertools.product(*mapped_tokens)]

    # Each array in parse_arrays is currently 2D, where SOs are chunked
    # by how they were mapped to individual lexica.  Flatten it to a 1D
    # array of SOs.
    parse_arrays = []
    for raw_parse_array in raw_parse_arrays:
        this_array = []
        for chunked_array in raw_parse_array:
            # Flatten by extending `this_array`
            this_array += chunked_array

        parse_arrays.append(this_array)

    return parse_arrays


def tokenise(input_string):
    """
    Fairly simple tokenisation
    :param input_string: 
    :return: 
    """
    remove_punct = set(string.punctuation)
    # Hyphens needed for some tokens
    remove_punct.remove("-")
    remove_punct = ''.join(remove_punct)
    return input_string.lower().translate(None, remove_punct).split()


def lookup_tokens(tokens, mapped=None):
    """
    Recursively searches the available lexica for all the possible SOs 
    that we could map tokens to.
    Returns False on OOV items
    Elsewise returns a list of lists of SOs, where the top-level list 
    represents tokens and the lower-level list represents possible SOs for 
    each token
    :param tokens: 
    :param mapped: 
    :return: 
    """
    if mapped is None:
        mapped = []

    # Base case
    if not tokens:
        return mapped

    # Start by taking the longest possible remaining token string
    for length in reversed(range(len(tokens))):
        token = " ".join(tokens[:length + 1])

        possible_entries = []

        # Get the possible entries from each lexicon
        # TODO: Cases where one lexicon has a multi-word entry that
        # TODO: overlaps with single words of another lexicon
        for lexicon in config.lexica:
            entry = lexicon.lookup_token(token)
            if entry:
                # Lexicons already return lists of possible entries,
                # which are themselves lists of SOs. We can extend
                # `possible_entries` instead of appending to it
                possible_entries += entry

        if len(possible_entries) == 0:
            if length == 0:
                # OOV
                print("Out of Vocabulary: {}".format(token))
                return False
        else:
            mapped.append(possible_entries)
            return lookup_tokens(tokens[length + 1:], mapped)
