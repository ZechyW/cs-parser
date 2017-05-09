# Zechy Wong
# 26 Apr 2017
# Code-switching parser

from __future__ import print_function, division

import pprint
import readline  # For editing history and the like
import string

from app import LexicalArray, SO, Parser
import config


# .,__,.-'~'-.,__,.-'~'-.,__,.-'~'-.,__,.-'~'-.,__,.-'~'-.,__,.-'~'-.,__,.
# Top-level: Figure out what the user wants
def main():
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
            ################################################
            # Here is the actual call to the Parser module #
            ################################################
            Parser.parse_string(" ".join(words[1:]))
        )
    else:
        # Invalid input
        return Result(False, False)


# Do whatever we need to do to the return values and show them to the user
def display_result(result):
    if result.command == "parse":
        if result.value:
            for parse in result.value:
                print(parse.to_brackets())
    else:
        print("Invalid command.")


if __name__ == "__main__":
    main()
