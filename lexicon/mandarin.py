# coding=utf-8
# Zechy Wong
# 10 May 2017
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
            # Pronouns
            "ta1": [
                SO(category="D",
                   label="他")
            ],

            # Common nouns
            "ji1 fan4": [
                SO(category="N",
                   label="鸡饭"),
                SO(category="D",
                   label="鸡饭")
            ],

            # Verbs
            "chi1": [
                SO(category="V",
                   label="吃",
                   subcat=[
                       ("right", SO("D"))
                   ],
                   generate=[
                       ("left", SO("v", Lexicon.null_label,
                                   subcat=[
                                       ("right", SO("V"))
                                   ]))
                   ])
            ],

            # Tense/Aspect
            "le4": [
                SO(category="T",
                   label="了",
                   subcat=[
                       ("left", SO("v")),
                       ("left", SO("D"))  # Subject
                   ]),
                SO(category="T",
                   label="了",
                   subcat=[
                       ("left", SO("v"))
                   ])
            ],

            # Relative clause
            "de4": [
                SO(category="D",
                   label="的",
                   features=["Rel"],
                   generate=[
                       # Null T selecting a v to the left
                       ("left", SO("T", Lexicon.null_label,
                                   subcat=[
                                       ("left", SO("v"))
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
