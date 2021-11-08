#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Directional characters
LRI: str = "\u2066"
RLI: str = "\u2067"
FSI: str = "\u2068"
LRE: str = "\u202A"
RLE: str = "\u202B"
LRO: str = "\u202D"
RLO: str = "\u202E"

# Closing markers
PDF: str = "\u202C"
PDI: str = "\u2069"

def insert_markers(
    text: str,
    rtl: str = RLO, end: str = PDF,
    markers: str = "{}") -> str:
    """
    Reverse specified text using RLO `\u202e`. The text to be reversed
    should be placed inside {brackets}.

    Example:
    >>> format_text("python is amazing")
    'python \\u202eis\\u202c amazing'

    :param text: the text with strings to be reversed
    :param markers: a 2-character string with the 
    :return: a string with the text enclosed by {markers} reversed

    NOTE: The RLO character does not work when placed at the very
          beginning of a string. There must be at least one visible 
          character before the RLO character (i.e. a zero-width space
          will not suffice, and the text will still print left-to-right)
    """
    m1: str = markers[0]
    m2: str = markers[1]
    return re.sub(f"{m1}(.*?){m2}", f"{rtl}\\1{end}", text)

if __name__ == "__main__":
    import re
    import os
    import sys

    # vars
    text: str
    prog_name: str

    # get data from a pipe if it exists
    if not os.isatty(0):
        text = sys.stdin.read()
    else:
        # piped input will have a newline most of the time,
        # so add a newline to text pass as arguments as well
        text = " ".join(sys.argv[1:]) + "\n"

    # print help message if no text provided
    if not text:
        prog_name = sys.argv[0].split(os.path.sep)[-1]
        print(f"usage: {prog_name} text")
        print()
        print("you must specify text to be reversed! the text to be")
        print("reversed should be enclosed in {brackets}, e.g.:")
        print()
        print(f"$ {prog_name}" + " hello {world}")
        sys.exit(1)
    
    print(insert_markers(text), end="")
    
