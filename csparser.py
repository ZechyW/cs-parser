# Zechy Wong
# 26 Apr 2017
# Code-switching parser

from __future__ import print_function, division

import importlib

# For editing history and the like
try:
    import readline
except ImportError:
    pass

import sys

import app.parser
import config

# .,__,.-'~'-.,__,.-'~'-.,__,.-'~'-.,__,.-'~'-.,__,.-'~'-.,__,.-'~'-.,__,.
# Top-level: Figure out what the user wants
help_text = ("'parse <sentence>' to parse, 'reload' to reload application, "
             "'exit' to exit")


def main():
    # Preamble
    print("Code-switching Parser")
    print(help_text)
    # Main IO loop
    exit_flag = False
    while not exit_flag:
        user_input = raw_input("> ")
        if user_input == "":
            continue
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
            ################################################
            # Here is the actual call to the Parser module #
            ################################################
            app.parser.parse_string(" ".join(words[1:]))
        )
    elif words[0] == "reload":
        # Trash the application modules and re-import them; that should work
        current_modules = list(sys.modules.keys())
        for mod_name in current_modules:
            if mod_name.startswith("app.") or mod_name.startswith("lexicon.") \
                    or mod_name == "app" or mod_name == "lexicon" \
                    or mod_name == "config":
                del sys.modules[mod_name]

        return Result(
            "reload",
            "Reloaded application modules. "
            "(Except not really -- May be buggy)"
        )
    elif words[0] == "help":
        print(help_text)
        return Result(True, True)
    else:
        # Invalid input
        return Result(False, False)


# Do whatever we need to do to the return values and show them to the user
def display_result(result):
    if result.command is False:
        print("Invalid command.")
    elif result.command is True:
        # No output
        return
    elif result.command == "parse":
        # Pretty-print a bracket representation of the returned parses
        if result.value:
            print()
            print("Valid parses found:")
            for parse in result.value:
                print("-----")
                print(parse.to_brackets())
                if config.debug:
                    print(parse)
        else:
            print("No valid parses.")
    else:
        # Generic result handling
        print("{}: {}".format(result.command, result.value))


if __name__ == "__main__":
    main()
