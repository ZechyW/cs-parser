# Zechy Wong
# 29 Apr 2017
# Code-switching parser
# ---------------------
# Class for dealing with individual syntactic objects


class SO:
    def __init__(self, category=None, label=None, features=None, subcat=None,
                 generate=None, children=None):
        # Syntactic category for the SO
        self.category = category

        # Will be printed as the display name for the SO
        self.label = label

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

        return ("SO({}, {}{}{}{}{})"
                "".format(self.category, self.label, features,
                          subcat, generate, children))
