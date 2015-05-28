# new mappings for historic districts to be added here

import re
queens = [
    '(Jacksons+Heights)\s+Historic\s+District',
    '(Douglaston)\s+Historic\s+District'
]
queens = [re.compile(i, re.IGNORECASE) for i in queens]

brooklyn = [
    '(Fillmore\s+Place)\s+Historic\s+District',
    '(Fulton\s+Ferry)\s+Historic\s+District',
    '(Fort\s+Greene)\s+Historic\s+District',
    '(Boerum Hill)\s+Historic\s+District',
    '(Brooklyn Heights)\s+Historic\s+District',
    '(Cobble Hill)\s+Historic\s+District',
    '(Crown Heights)\s+North\s+Historic\s+District\s+II'
]
brooklyn = [re.compile(i, re.IGNORECASE) for i in brooklyn]

manhattan = [
    '(Building)-Individual\s+Landmark',
    '(Tribeca)\s+West\s+Historic\s+District',
    '(SoHo)Cast\s+Iron\s+Historic\s+District',
    '(NoHo)\s+Historic\s+District'
]
manhattan = [re.compile(i, re.IGNORECASE) for i in manhattan]


def preprocess(text):
    for rex in queens:
        text = rex.sub('\\1 Queens, NY', text)

    for rex in brooklyn:
        text = rex.sub('\\1 Brooklyn, NY', text)

    for rex in manhattan:
        text = rex.sub('\\1 NY, NY', text)

    return text
