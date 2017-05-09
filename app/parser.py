# Zechy Wong
# 8 May 2017
# Code-switching parser
# ---------------------
# Parser functions
# Tokenisation and lexical array construction are farmed out to the
# LexicalArray class

import pprint

from app.lexical_array import LexicalArray
from app.syntactic_object import SO


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

        # Attempt to parse recursively, SO-by-SO, keeping track of what's on
        # the left and right
        checked_parses = [Parser.check_parse(left=[], right=parse_combo)
                          for parse_combo in parse_combos]

        # Return any parses that survived the check
        return filter(None, checked_parses)

    @staticmethod
    def check_parse(left, right, parse=None, last_active=0):
        """
        Parse the given array of SOs recursively
        Make sure the subcategorisations are satisfied, or return False
        Also try to detect when repeating the parse attempt will go nowhere
        :param left: 
        :param right: 
        :param parse: 
        :param last_active: 
        :return: 
        """
        pprint.pprint(left)
        pprint.pprint(right)
        if parse:
            print(parse.to_brackets())
        print("\n")

        # Base case:
        if len(left) == 0 and len(right) == 0:
            # We made it
            return parse

        # We go from left to right; if any subcategorisations are not fulfilled,
        # we move another step and try again
        if parse is None:
            consider_so = right.pop(0)
        else:
            consider_so = parse

        if len(consider_so.subcat) == 0:
            # This SO does not subcategorise.  Is anything on the sides looking
            # for something?
            if len(left) > 0 and len(left[-1].subcat) > 0:
                # Look at the closest thing on the left
                criteria = left[-1].subcat[0]
                if criteria[0] == "right" and Parser.subcat_match(criteria[1],
                                                                  consider_so):
                    # A match.
                    head = left.pop()
                    parse = SO(category=head.category, label=head.category,
                               subcat=head.subcat[1:],
                               children=[head, consider_so])
                    return Parser.check_parse(left, right, parse)

            if len(right) > 0 and len(right[0].subcat) > 0:
                # On the right
                criteria = right[0].subcat[0]
                if criteria[0] == "left" and Parser.subcat_match(criteria[1],
                                                                 consider_so):
                    # A match.
                    head = right.pop(0)
                    parse = SO(category=head.category, label=head.category,
                               subcat=head.subcat[1:],
                               children=[consider_so, head])
                    return Parser.check_parse(left, right, parse)

            # Still here? We haven't found anything close (because we want to
            # respect the ordering of subcats) -- Move on for now by falling
            # through to the high-level checks
            pass

        # ----

        # The current SO subcategorises, or we need to build up more of the
        # parse
        #  first. Try moving a step to the right.
        if len(right) > 0:
            left.append(consider_so)
            return Parser.check_parse(left, right, None, last_active + 1)
        else:
            # Got to the end, no good.
            # Last chance: Give it another run-through if there are items in
            # left
            # that don't subcat
            found_non_subcat = False
            for check_subcat in left:
                if len(check_subcat.subcat) == 0:
                    found_non_subcat = True

            # Make sure that the last real parse we did was not too many
            # iterations ago
            if found_non_subcat and last_active < len(left):
                # One more time
                return Parser.check_parse([], left + [consider_so], None)
            else:
                return False

    @staticmethod
    def subcat_match(so_1, so_2):
        """
        Check if so_2 meets the subcategorisation criteria in so_1 (i.e., 
        the two SOs can be unified, in some sense)
        Returns true/false
        :param so_1: 
        :param so_2: 
        :return: 
        """

        # Simple matching for categories and labels:
        # True if either one is None, or both SOs have the same value
        def simple_match(a, b):
            return a is None or b is None or a == b

        if not simple_match(so_1.category, so_2.category):
            return False

        if not simple_match(so_1.label, so_2.label):
            return False

        # TODO: Feature matching, phase level lexicon switch, etc.

        # Still here?
        return True
