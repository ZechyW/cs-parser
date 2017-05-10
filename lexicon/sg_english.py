# Zechy Wong
# 8 May 2017
# Code-switching parser
# ---------------------
# Singapore English Lexicon
# Includes both general rules and a list of base lexical items

import copy

from lexicon.template import Lexicon
import app.parser
from app.syntactic_object import SO


class SgE(Lexicon):
    def __init__(self):
        """
        Initialise the SgE specific lexicon object
        """
        Lexicon.__init__(self)

        self.id = "SgE"

        # Put all the data-heavy bits further down for readability
        self.rules = self.get_rules()
        self.lexicon = self.get_lexicon()

    def apply_rules(self, token_parse_list):
        """
        Takes a list of parses, where each parse is a list of SOs.
        Run it through the rule system and return an enriched list of parses.
        :param token_parse_list:
        :return:
        """
        enriched_parse_list = []

        # ----------------------------------
        def rule_match(criteria, candidate):
            """
            Checks that the lengths of the two arguments (lists) are the same.
            Then makes sure that every item in the criteria list subcat_matches 
            with every corresponding item in the candidate list.
            :param criteria: 
            :param candidate: 
            :return: (True|False) 
            """
            if len(criteria) != len(candidate):
                return False

            # Use idx to test corresponding items
            for idx in range(len(criteria)):
                if not app.parser.subcat_match(criteria[idx], candidate[idx]):
                    return False

            # Still here?
            return True

        # ----------------------------------

        # Run the rule system
        for token_parse in token_parse_list:
            for rule in self.rules:
                if rule_match(rule[0], token_parse):
                    copied_parse = copy.deepcopy(token_parse)
                    copied_parse = rule[1](copied_parse)
                    if copied_parse is not False:
                        enriched_parse_list.append(copied_parse)

            # Add the original parse
            enriched_parse_list.append(token_parse)

        return enriched_parse_list

    # .,__,.-'~'-.,__,.-'~'-.,__,.-'~'-.,__,.-'~'-.,__,.-'~'-.,__,.-'~'-.,__,.
    # Private data functions

    @staticmethod
    def get_rules():
        """
        Return a list of rules
        Each rule is a tuple: The 1st member is a list of SOs containing subcat 
        criteria, the 2nd is a function.
        If a token parse matches the 1st member, a copy is passed as an 
        argument to the 2nd.
        Specifically, the length of the 1st member is checked against the 
        length of the token parse (which can be > 1, since a single token 
        might theoretically base-generate more than one SO -- Although it 
        currently shouldn't)
        The rule function should return False for a no-op
        :return:
        """
        rule_list = []

        # Ns subcategorising for relative little-Cs to the right
        n_rel_c_subcat = [
            SO("N")
        ]

        def n_rel_c(copied_parse):
            # copied_parse is a list of length 1 -- containing the N SO
            # Check if it already subcategorises for a little-c/C
            for criteria in copied_parse[0].subcat + copied_parse[0].generate:
                if criteria[1].category == "c" or criteria[1].category == "C":
                    return False

            # If not, generate a little c to the right that subcategorises
            # for a Rel C to the right and a N to the left
            copied_parse[0].generate.append(
                ("right", SO("c", Lexicon.null_label,
                             features=["Rel"],
                             subcat=[
                                 ("left", SO("N")),
                                 ("right", SO("C", features=["Rel"]))
                             ]))
            )
            return copied_parse

        rule_list.append([n_rel_c_subcat, n_rel_c])

        return rule_list

    @staticmethod
    def get_lexicon():
        """
        Return a dictionary of base lexical items
        Parameters: category, label, features, subcat, generate, children
        :return:
        """
        return {
            # Determiners
            "the": [
                SO(category="D",
                   label="the",
                   subcat=[("right", SO("N"))]),
                # Determiners selecting relative clauses
                SO(category="D",
                   label="the",
                   subcat=[("right", SO("c"))])
            ],

            # Count nouns
            "man": [
                SO("N", "man", )
            ],

            # Mass nouns
            "rice": [
                SO("D", "rice"),
                SO("N", "rice")
            ],

            # Verbs
            "eat": [
                SO("V", "eat", ["inf"],
                   subcat=[("right", SO("D"))]),
                SO("V", "eat", ["inf"])
            ],
            "eats": [
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
            ],
            "ate": [
                SO("V", "eat",
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
                                 subcat=[
                                     ("right", SO("V")),
                                     ("left", SO("D"))
                                 ]))]
                   )
            ],

            "like": [
                # likes with complement CP
                SO("V", "like",
                   subcat=[
                       ("right", SO("T"))
                   ])
            ],

            "likes": [
                SO("V", "like",
                   generate=[
                       ("left",
                        SO("T", "-s",
                           subcat=[
                               ("right", SO("V")),
                               ("left", SO("D"))
                           ]))
                   ],
                   subcat=[
                       ("right", SO("T"))
                   ])
            ],

            # Inflections
            "-ed": [
                SO("T", "-ed",
                   subcat=[
                       ("left", SO("V"))
                   ])
            ],

            "to": [
                SO("T", "to",
                   subcat=[
                       ("right", SO("V"))
                   ])
            ]
        }
