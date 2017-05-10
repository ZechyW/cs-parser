# Zechy Wong
# 8 May 2017
# Code-switching parser
# ---------------------
# General configuration/initialisation options

# Print debugging output?  (Can be pretty verbose)
debug = True

# Phase boundaries:
# Lexicon switch is only allowed if the head belongs to one of these categories
# (i.e., the head can be in one language and the complement another)
# Phonologically null elements will remain indeterminate w.r.t. lexicon until
# a phase boundary is reached, at which time the complement SO hierarchy will
# be checked for consistency
phase_heads = ["v", "c"]

# Initialise lexica
import lexicon

lexica = [
    lexicon.SgE(),
    lexicon.Mandarin()
]
