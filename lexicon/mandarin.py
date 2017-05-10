# coding=utf-8
# Zechy Wong
# 8 May 2017
# Code-switching parser
# ---------------------
# (Singapore) Mandarin Lexicon
# Includes both general rules and a list of base lexical items

from lexicon.template import Lexicon
from app.syntactic_object import SO


class Mandarin(Lexicon):
    def __init__(self):
        """
        Initialise the lexicon object
        """
        Lexicon.__init__(self)

        self.id = "Mandarin"

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
            # Common nouns
            "dian4 nao3": [
                SO(category="N",
                   label="电脑"),
                SO(category="D",
                   label="电脑")
            ],

            # Verbs
            "wan2": [
                SO(category="V",
                   label="玩",
                   subcat=[
                       ("right", SO("D"))
                   ])
            ],

            # Tense/Aspect
            "le4": [
                SO(category="T",
                   label="了",
                   subcat=[
                       ("left", SO("V")),
                       ("left", SO("D"))  # Subject
                   ])
            ],

            # Relative clause
            "de4": [
                SO(category="D",
                   label="的",
                   features=["Rel"],
                   generate=[
                       # Null T selecting a V to the left
                       ("left", SO("T", Lexicon.null_label,
                                   subcat=[
                                       ("left", SO("V"))
                                   ])),
                       ("left", SO("C", Lexicon.null_label,
                                   features=["Rel"],
                                   subcat=[
                                       ("left", SO("T")),
                                       # Looks for relative D on its right
                                       ("right", SO("D", features=["Rel"]))
                                   ]))
                   ])
            ]
        }
