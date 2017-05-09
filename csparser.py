# Zechy Wong
# 26 Apr 2017
# Code-switching parser

from __future__ import print_function, division
import itertools
import pprint
import string


# .,__,.-'~'-.,__,.-'~'-.,__,.-'~'-.,__,.-'~'-.,__,.-'~'-.,__,.-'~'-.,__,.
# Top-level: Figure out what the user wants
def main():
    # Prepare the application
    import config


    # Preamble
    print("Code-switching Parser")
    print("'parse <sentence>' to parse, 'exit' to exit")
    # Main IO loop
    exit_flag = False
    while not exit_flag:
        user_input = raw_input("> ")
        result = command_parse(user_input)
        if result.command == "exit":
            exit_flag = True
        else:
            display_result(result)


# Result of executing user's command -- Value need not be a String
class Result:
    def __init__(self, command, value):
        self.command = command
        self.value = value


# Simple command parser: Get the first word and hand-off accordingly
def command_parse(user_input):
    words = user_input.lower().split()
    if words[0] == "exit":
        return Result("exit", "")
    elif words[0] == "parse":
        # Put the spaces back into the sentence so that the parsing section can
        # handle tokenisation
        return Result(
            "parse",
            process_sentence(" ".join(words[1:]))
        )
    else:
        # Invalid input
        return Result(False, False)


# Do whatever we need to do to the return values and show them to the user
def display_result(result):
    if result.command == "parse":
        if result.value:
            for parse in result.value:
                print(so2brackets(parse))
    else:
        print("Invalid command.")


# Pretty-print a parse
def so2brackets(parse):
    if parse is None:
        return "None"

    if len(parse.children) == 0:
        return "[{} {}]".format(parse.category, parse.label)
    else:
        return ("[{} {}]"
                "".format(parse.label,
                          " ".join([so2brackets(x) for x in parse.children])))


# .,__,.-'~'-.,__,.-'~'-.,__,.-'~'-.,__,.-'~'-.,__,.-'~'-.,__,.-'~'-.,__,. --
# Actual parser
def process_sentence(sentence):
    tokens = tokenise(sentence)

    # The idea: By looking up the tokens in the lexica, create a list of all
    # the possible combinations of SOs that we will consider.
    # Then go through the list, making sure that every subcategorisation is
    # satisfied.
    # Present the parses that survived.

    mapped_tokens = lookup_tokens(tokens)
    if not mapped_tokens:
        return False

    raw_arrays = [list(x) for x in itertools.product(*mapped_tokens)]

    # Generate functional categories if necessary
    all_arrays = []
    for array in raw_arrays:
        this_array = []
        for idx in range(len(array)):
            # Go over each token, checking the 'generate' attribute
            if len(array[idx].generate) > 0:
                for gen_params in array[idx].generate:
                    if gen_params[0] == "left":
                        this_array.append(gen_params[1])
                        this_array.append(array[idx])
                    elif gen_params[0] == "right":
                        this_array.append(array[idx])
                        this_array.append(gen_params[1])
            else:
                this_array.append(array[idx])

        all_arrays.append(this_array)

    # Attempt to parse recursively, keeping track of what's on the left and
    # right
    parse_list = [parse_array(left=[], right=array)
                  for array in all_arrays]

    return filter(None, parse_list)


# Simple tokenisation
def tokenise(sentence):
    return sentence.lower().translate(None, string.punctuation).split()


# Parse the given array of SOs recursively
# Make sure the subcategorisations are satisfied, or return False
# Also try to detect when repeating the parse attempt will go nowhere
def parse_array(left, right, parse=None, last_active=0):
    pprint.pprint(left)
    pprint.pprint(right)
    print(so2brackets(parse))
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
            if criteria[0] == "right" and subcat_match(criteria[1],
                                                       consider_so):
                # A match.
                head = left.pop()
                parse = SO(category=head.category, label=head.category,
                           subcat=head.subcat[1:],
                           children=[head, consider_so])
                return parse_array(left, right, parse)

        if len(right) > 0 and len(right[0].subcat) > 0:
            # On the right
            criteria = right[0].subcat[0]
            if criteria[0] == "left" and subcat_match(criteria[1],
                                                      consider_so):
                # A match.
                head = right.pop(0)
                parse = SO(category=head.category, label=head.category,
                           subcat=head.subcat[1:],
                           children=[consider_so, head])
                return parse_array(left, right, parse)

        # Still here? We haven't found anything close (because we want to
        # respect the ordering of subcats) -- Move on for now by falling
        # through to the high-level checks
        pass

    # ----

    # The current SO subcategorises, or we need to build up more of the parse
    #  first. Try moving a step to the right.
    if len(right) > 0:
        left.append(consider_so)
        return parse_array(left, right, None, last_active + 1)
    else:
        # Got to the end, no good.
        # Last chance: Give it another run-through if there are items in left
        # that don't subcat
        found_non_subcat = False
        for check_subcat in left:
            if len(check_subcat.subcat) == 0:
                found_non_subcat = True

        # Make sure that the last real parse we did was not too long ago
        if found_non_subcat and last_active < len(left):
            # One more time
            return parse_array([], left + [consider_so], None)
        else:
            return False


# See if the elements of two SOs are compatible
# TODO: Add stuff
def subcat_match(so_1, so_2):
    return not_none_match(so_1.category, so_2.category) and \
           not_none_match(so_1.label, so_2.label)


# Utility function
def not_none_match(a, b):
    return a is None or b is None or a == b


# .,__,.-'~'-.,__,.-'~'-.,__,.-'~'-.,__,.-'~'-.,__,.-'~'-.,__,.-'~'-.,__,. --
# Lexica

# Class for handling heads and other syntactic objects
class SO:
    def __init__(self, category=None, label=None, features=None, subcat=None,
                 children=None, generate=None):
        # Syntactic category for the SO
        self.category = category

        # Will be printed as the display name for the SO
        self.label = label

        self.features = features
        if features is None:
            self.features = []

        # List of SOs that need to be adjacent to the current SO.
        # Tuples: First element specifies linear direction of subcategorisation
        self.subcat = subcat
        if subcat is None:
            self.subcat = []

        # List of children under this SO (expected to be <= 2)
        self.children = children
        if children is None:
            self.children = []

        # Functional categories to generate to the left or right of this SO
        self.generate = generate
        if generate is None:
            self.generate = []

    def __repr__(self):
        return ("SO({}, {}, {}, {}, {}, {})"
                "".format(self.category, self.label, self.features,
                          self.subcat, self.children, self.generate))


def lookup_tokens(tokens, mapped=None):
    # Recursively searches both the English and Chinese lexica for all the
    # possible SOs that we could map tokens to.
    # Also handles OOV items

    if mapped is None:
        mapped = []

    # Base case
    if tokens == []:
        return mapped

    # Start by taking the longest possible remaining token string
    for length in reversed(range(len(tokens))):
        token = " ".join(tokens[:length + 1])

        return_list = []
        if token in lexicon_eng:
            return_list += lexicon_eng[token]
        if token in lexicon_chi:
            return_list += lexicon_chi[token]

        if len(return_list) == 0:
            if len(token) == 0:
                # OOV
                print("Out of Vocabulary: {}".format(token))
                return False
        else:
            mapped.append(return_list)
            return lookup_tokens(tokens[length + 1:], mapped)


# Possible features:
# Syntactic:
# iRel: interpretable Relative feature
# Agreement:
# inf: Infinitival forms

# Each lexical entry is a list of possible SOs that the word might correspond
# to.
# TODO: Handle nonce borrowings and proper names etc.
lexicon_eng = {}
lexicon_eng["the"] = [SO("D", "the",
                         subcat=[("right", SO("N"))])]

lexicon_eng["man"] = [
    # Simple Ns don't subcategorise
    SO("N", "man"),
    # Ns that can take relative clauses subcategorise for Cs
    SO("N", "man",
       subcat=[("right", SO("C", features=["iRel"]))])
]

lexicon_eng["eat"] = [SO("V", "eat", ["inf"],
                         subcat=[("right", SO("D"))]),
                      SO("V", "eat", ["inf"])
                      ]

lexicon_eng["eats"] = [
    # Transitive
    SO("V", "eat",
       subcat=[("right", SO("D"))],
       generate=[("left",
                  SO("T", "-s",
                     subcat=[("right", SO("V")),
                             ("left", SO("D"))
                             ]))]
       ),
    # Intransitive
    SO("V", "eat",
       generate=[("left",
                  SO("T", "-s",
                     subcat=[("right", SO("V")),
                             ("left", SO("D"))
                             ]))]
       )
]

lexicon_eng["ate"] = [SO("V", "eat",
                         subcat=[("right", SO("D"))],
                         generate=[("left",
                                    SO("T", "-ed",
                                       subcat=[("right", SO("V")),
                                               ("left", SO("D"))
                                               ]))]
                         ),
                      SO("V", "eat",
                         generate=[("left",
                                    SO("T", "-ed",
                                       subcat=[("right", SO("V")),
                                               ("left", SO("D"))
                                               ]))]
                         )
                      ]

lexicon_eng["rice"] = [SO("D", "rice"),
                       SO("N", "rice")]

lexicon_chi = {}
lexicon_chi["le"] = [SO("T", "le",
                        subcat=[("left", SO("V")),
                                ("left", SO("D"))])]

lexicon_chi["li si"] = [SO("D", "li si")]

if __name__ == "__main__":
    main()
