# coding=utf-8
# Zechy Wong
# 8 May 2017
# Code-switching parser
# ---------------------
# Parser functions
# - Tokenisation and lexical array construction are farmed out to the
#   LexicalArray class
# - Phase edge detection and lexicon switch handled in the merge() method

from __future__ import print_function

import pprint

import config
import app.lexical_array
from app.syntactic_object import SO


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
    parse_combos = app.lexical_array.enumerate_input(user_input)
    if not parse_combos:
        # Did not manage to enumerate the input
        return []

    # Attempt to parse recursively, SO-by-SO, keeping track of what's on
    # the left and right
    checked_parses = [check_parse(left=[], right=parse_combo)
                      for parse_combo in parse_combos]

    # Return any parses that survived the check
    return filter(None, checked_parses)


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
    if config.debug:
        print("SOs on the Left:")
        pprint.pprint(left)
        print()
        print("SOs on the Right:")
        pprint.pprint(right)

        if parse:
            print()
            print("Currently built-up parse:")
            print(parse.to_brackets())

        print(".,__,.-'~'-.,__,.-'~'-.,__,.-'~'-.,__,.-'~'-.,__,.-'~'-.,__"
              ",.-'~'-.,__,.")

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
            if criteria[0] == "right" and subcat_match(criteria[1],
                                                       consider_so):
                # A match. Pop last element from left array
                head = left.pop()
                parse = merge(head=head,
                              complement=consider_so,
                              head_direction="left",
                              new_subcat=head.subcat[1:])
                if not parse:
                    # Poopsy, merge failed
                    return False

                return check_parse(left, right, parse)

        if len(right) > 0 and len(right[0].subcat) > 0:
            # On the right
            criteria = right[0].subcat[0]
            if criteria[0] == "left" and subcat_match(criteria[1],
                                                      consider_so):
                # A match. Pop first element from right array
                head = right.pop(0)
                parse = merge(head=head,
                              complement=consider_so,
                              head_direction="right",
                              new_subcat=head.subcat[1:])
                if not parse:
                    # Poopsy, merge failed
                    return False

                return check_parse(left, right, parse)

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
        return check_parse(left, right, None, last_active + 1)
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
            return check_parse([], left + [consider_so], None)
        else:
            # Ah well
            return False


def subcat_match(criteria, candidate):
    """
    Check if so_2 meets the subcategorisation criteria in so_1 (i.e., 
    the two SOs can be unified, in some sense)
    Returns true/false
    :param criteria: 
    :param candidate: 
    :return: 
    """

    # Simple matching for categories and labels:
    # True if either one is None, or both SOs have the same value
    def simple_match(a, b):
        return a is None or b is None or a == b

    if not simple_match(criteria.category, candidate.category):
        return False

    if not simple_match(criteria.label, candidate.label):
        return False

    # Simple Feature matching:
    # True if so_2's features are a superset of so_1's features
    if not set(criteria.features) <= set(candidate.features):
        return False

    # Still here?
    return True


def merge(head, complement, head_direction, new_subcat):
    """
    Merges two SOs, a head an a complement together, keeping features on 
    the head as needed.
    
    Only allows lexicon shift at phase boundaries
    
    Returns a new SO that has the original head/complement as children
    Or False on failure
    :param head: 
    :param complement: 
    :param head_direction: (left|right) Which side is the head on? 
    :param new_subcat: List of subcats for the new SO 
    :return: 
    """
    parent = SO()

    # Category and label
    # (Label will be the category as well, for complex SOs)
    parent.category = head.category
    parent.label = head.category

    # Copy Features
    parent.features = head.features[:]

    # Save new subcat list
    parent.subcat = new_subcat

    # Check if lexicon switch has occurred
    head_lexicon = head.last_phase_lexicon()
    complement_lexicon = complement.last_phase_lexicon()

    lexicon_match = \
        head_lexicon == {None} or complement_lexicon == {None} or \
        head_lexicon == complement_lexicon

    if not lexicon_match:
        # Two possibilities:
        # 1) head is a phase_head, we let it slide
        # 2) 🔥 HCF 🔥 🚒🚒🚒
        if head.category not in config.phase_heads:
            return False

    # Insert children SOs
    assert head_direction == "left" or head_direction == "right"
    if head_direction == "left":
        parent.children = [head, complement]
    elif head_direction == "right":
        parent.children = [complement, head]

    return parent
