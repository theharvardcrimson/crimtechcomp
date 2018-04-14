def uniquify(seq):
    """Returns a unique list.  This preserves order"""
    seen = set()
    result = []
    for item in seq:
        if item in seen:
            continue
        seen.add(item)
        result.append(item)
    return result


def first_or_none(seq):
    """Returns the first element of a sequence, or None, if len == 0."""
    if len(seq) == 0:
        return None
    return seq[0]
