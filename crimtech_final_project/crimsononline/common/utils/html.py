import re

PARA_RE = re.compile(r'</(p|h\d)>\s*<(p|h\d)')


def para_list(s):
    """Split s on <p> and heading tags

    Keep the <p> and heading tags in the output.
    """
    # remove whitespace between adjacent tags, replace with sentinel value
    s = PARA_RE.sub(r'</\1>,,,<\2', s)
    # split by sentinel value
    return s.split(',,,')
