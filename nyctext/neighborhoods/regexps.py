import re
def make_neighorbood_regex(lHoods):

    # neighborhood name:
    #    begins with a whitespace
    #    ends with a comma, or whitespace
    lst = [r'\s%s[\s,]' % n for n in lHoods]
    lst = '|'.join(lst)

    # Don't match if neighborhood is followed
    # by a thoroughfare name
    lst = '(%s)(?!(Avenue|Street|Parkway))' % lst
    return  re.compile(lst, re.I)
