# Zechy Wong
# 8 May 2017
# Code-switching parser
# ---------------------
# Singapore English Lexicon
# Includes both general rules and a list of base lexical items

from lexicon.template import Lexicon
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
        return token_parse_list

    # .,__,.-'~'-.,__,.-'~'-.,__,.-'~'-.,__,.-'~'-.,__,.-'~'-.,__,.-'~'-.,__,.
    # Private data functions

    @staticmethod
    def get_rules():
        """
        Return a list of rules
        :return:
        """
        # TODO: Ns can subcategorise for relative Cs
        # # Ns that can take relative clauses subcategorise for Cs
        # SO("N", "man",
        #    subcat=[("right", SO("C", features=["iRel"]))])

        return []

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
                   subcat=[("right", SO("N"))])
            ],

            # Count nouns
            "man": [
                SO("N", "man")
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
                                 subcat=[("right", SO("V")),
                                         ("left", SO("D"))
                                         ]))]
                   )
            ]
        }
