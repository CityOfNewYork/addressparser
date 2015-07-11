# -*- coding: utf-8 -*-
__author__ = "C. Sudama, Matthew Alhonte"
__license__ = "Apache License 2.0: http://www.apache.org/licenses/LICENSE-2.0"

# new mappings for historic districts to be added here

import re
queens = [
    '-(Jackson Heights)\s+Historic\s+District',
    '-(Douglaston)\s+Historic\s+District'
]
queens = [re.compile(i, re.IGNORECASE) for i in queens]

bk_nobackfill = [
    '-Fillmore\s+Place\s+Historic\s+District',
]
bk_nobackfill = [re.compile(i, re.IGNORECASE) for i in bk_nobackfill]

brooklyn = [
    '-(Fulton\s+Ferry)\s+Historic\s+District',
    '-(Fort\s+Greene)\s+Historic\s+District',
    '-(Boerum Hill)\s+Historic\s+District',
    '[\-\s]+(Brooklyn\s+Heights)\s+Historic\s+District',
    '-(Cobble Hill)\s+Historic\s+District',
    '-(Crown Heights)\s+North\s+Historic\s+District\s+II'
]
brooklyn = [re.compile(i, re.IGNORECASE) for i in brooklyn]

manhattan = [
    '-(Building)-Individual\s+Landmark',
    '-(Tribeca)\s+West\s+Historic\s+District',
    '-(SoHo)Cast\s+Iron\s+Historic\s+District',
    '-(NoHo)\s+Historic\s+District'
]
manhattan = [re.compile(i, re.IGNORECASE) for i in manhattan]


def preprocess(text):
    for rex in queens:
        # Remove the Historic district, leave the neighborhood to be
        # promoted to correct borough at the neighborhood-filter step
        #
        # Start:           37-18 79th Street-Jackson Heights Historic District
        # Strip Historic:  37-18 79th Street Jackson Heights, NY.
        # Promote Borough: 37-18 79th Street Queens, NY.

        text = rex.sub(', \\1, NY.\n', text)

    for rex in brooklyn:
        text = rex.sub(', \\1, Brooklyn, NY.\n', text)
    for rex in bk_nobackfill:
        text = rex.sub(', Brooklyn, NY.\n', text)

    for rex in manhattan:
        text = rex.sub(', \\1, Manhattan, NY.\n', text)
    return text
