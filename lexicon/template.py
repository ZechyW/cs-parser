# coding=utf-8
# Zechy Wong
# 26 Apr 2017
# Code-switching parser
# ---------------------
# Class template for lexica

import copy


# Decorator
def warn_undefined(func):
    """
    Lets the user know that some lexicon module failed to re-define one of the
    core API functions
    """

    def wrapped(self, *args, **kwargs):
        print("Lexicon [{0}] did not define API method: {1}"
              .format(self.__class__.__name__,
                      func.__name__))
        return func(self, *args, **kwargs)

    return wrapped


class Lexicon:
    # Label for unpronounced items (e.g., functional heads)
    null_label = "∅"

    def __init__(self):
        # We expect all lexica to have a set of basic rules and a set of base
        # lexical items.
        # We assume that the basic rules operate on single lexical items (no
        # complex in-lexicon operations) -- Idioms and the like are handled
        # as multi-token items.
        # The functions that check items and run them through the various
        # necessary procedures are subclass-internal; only the general lookup
        # function is part of the API

        # Identifier string for the lexicon
        self.id = "Default"

        # Rule system
        self.rules = []

        # Base lexical items
        self.lexicon = {}

    @warn_undefined
    def apply_rules(self, token_parse_list):
        """
        Takes a list of parses, where each parse is a list of SOs.
        Run it through the rule system and return an enriched list of parses.

        This we leave to individual lexica to define.

        :param token_parse_list:
        :return:
        """
        return token_parse_list

    # .,__,.-'~'-.,__,.-'~'-.,__,.-'~'-.,__,.-'~'-.,__,.-'~'-.,__,.-'~'-.,__,.
    # Common utility functions

    def lookup_token(self, token):
        """
        Given some raw input string from the user, should attempt to return
        any exact matches for a *single* token after running it through the
        rule system (recursively if necessary) -- As a list of lists of SOs
        Or False if there are no applicable matches
        :param token:
        :return:
        """
        # In the lexicon, each token maps to a 1-d list of its possible base SO
        # representations.
        # When we return it, we want to expand this to a 2-d list:
        # A list of all possible parses, where each parse is a list of SOs
        # (including functional heads and the like which might be generated
        # from the base SO).

        # Get base SO
        if token in self.lexicon:

            token_parse_list = []

            # Create a copy of the lexical entry so that we don't accidentally
            # mess up the actual lexicon
            copied_entry = copy.deepcopy(self.lexicon[token])

            for base_so in copied_entry:
                token_parse_list.append([base_so])
        else:
            return False

        # Run through rule system, which might add 'generate' entries and the
        # like
        token_parse_list = self.apply_rules(token_parse_list)

        # Generate any needed SOs (viz., functional heads and the like)
        token_parse_list = self.generate_items(token_parse_list)

        # Mark every SO with the ID of this lexicon (unless it is
        # phonologically null)
        for token_parse in token_parse_list:
            for so in token_parse:
                if so.label != Lexicon.null_label:
                    so.lexicon = self.id

        return token_parse_list

    def generate_items(self, token_parse_list):
        """
        Takes a list of parses, where each parse is a list of SOs.
        Recursively generate sub-SOs that are specified in the base SOs
        :param token_parse_list:
        :return:
        """
        # Will return/recurse over this enriched list of parses
        enriched_parse_list = []
        # Will watch the things we generate -- If they contain 'generate'
        # attributes themselves, we will recurse
        generate_again = False

        for token_parse in token_parse_list:
            # Loop through the SOs of this parse, generating new entries where
            # specified
            enriched_parse = []
            for idx in range(len(token_parse)):
                # Check the 'generate' attribute of each SO in this parse
                if len(token_parse[idx].generate) > 0:
                    # Queue up things to be generated to the left and the right
                    generate_left = []
                    generate_right = []
                    for generate_params in token_parse[idx].generate:
                        if generate_params[0] == "left":
                            generate_left.append(generate_params[1])
                        elif generate_params[0] == "right":
                            generate_right.append(generate_params[1])

                        # Will we need to recurse?
                        if len(generate_params[1].generate) > 0:
                            generate_again = True

                    # Done queueing up generated elements. Fill in the SOs for
                    # this parse by extending the left/right queues in
                    enriched_parse += generate_left

                    token_parse[idx].generate = []
                    enriched_parse.append(token_parse[idx])

                    enriched_parse += generate_right
                else:
                    enriched_parse.append(token_parse[idx])

            # Put it on the final parse list
            enriched_parse_list.append(enriched_parse)

        # Do we need to recurse?
        if generate_again:
            return self.generate_items(enriched_parse_list)
        else:
            return enriched_parse_list
