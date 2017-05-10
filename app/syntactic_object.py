# Zechy Wong
# 9 May 2017
# Code-switching parser
# ---------------------
# Class for dealing with individual syntactic objects

import config
import lexicon


class SO:
    def __init__(self, category=None, label=None, lexicon=None, features=None,
                 subcat=None, generate=None, children=None):
        # Syntactic category for the SO
        self.category = category

        # Will be printed as the display name for the SO
        self.label = label

        # Keep track of (roughly) which lexicon this SO came from
        self.lexicon = lexicon

        # Various features (agreement, etc.)
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
        # For generating a readable representation for debugging
        if len(self.features) > 0:
            features = ", features={}".format(self.features)
        else:
            features = ""

        if len(self.subcat) > 0:
            subcat = ", subcat={}".format(self.subcat)
        else:
            subcat = ""

        if len(self.generate) > 0:
            generate = ", generate={}".format(self.generate)
        else:
            generate = ""

        if len(self.children) > 0:
            children = ", children={}".format(self.children)
        else:
            children = ""

        return ("SO({}, {}, <{}>{}{}{}{})"
                "".format(self.category, self.label, self.lexicon,
                          features, subcat, generate, children))

    def to_brackets(self):
        """
        Returns a prettified/simplified representation of this SO (in bracket 
        notation)
        :return: 
        """
        if len(self.children) == 0:
            return "[{} {}]".format(self.category, self.label)
        else:
            return ("[{} {}]"
                    "".format(self.label,
                              " ".join(
                                  [x.to_brackets() for x in self.children])))

    def last_phase_lexicon(self):
        """
        Searches through the SO's hierarchy to determine which lexica the 
        last phase (as determined by config.phase_heads) is matched with.
        Returns a set of the relevant lexica 
        Will contain None if the last phase was not marked (i.e., it consisted 
        completely of phonologically null elements)
        :return: 
        """
        # Base cases
        # 1) No children
        if len(self.children) == 0:
            return {self.lexicon}

        # 2) Is a phase head
        if self.category in config.phase_heads:
            return {self.lexicon}

        # Recursive cases
        return_set = set()
        for child in self.children:
            return_set.update(child.last_phase_lexicon())

        # Trim None out if there is *any* lexicon-marked item in the current
        # phase
        if len(return_set) > 1 and None in return_set:
            return_set.remove(None)

        return return_set
