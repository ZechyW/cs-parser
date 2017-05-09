# Zechy Wong
# 8 May 2017
# Code-switching parser
# ---------------------
# Parser functions
# Tokenisation and lexical array construction are farmed out to the
# LexicalArray class

from app import LexicalArray


class Parser:
    def __init__(self):
        pass

    @staticmethod
    def parse_string(user_input):
        """
        Attempts to provide parses for some user-given string.
        Does not assume complete sentences.
        :param user_input: 
        :return: 
        """
        # The idea: By looking up the tokens in the lexica, create a list of all
        # the possible combinations of SOs that we will consider.
        # Then go through the list, making sure that every subcategorisation is
        # satisfied.
        # Present the parses that survived.

        # Start by getting the LexicalArray class to help us tokenise the input
        # and generate a list of all possible lexical arrays: Lists of
        # possible SO combinations.
        parse_combos = LexicalArray.enumerate_input(user_input)