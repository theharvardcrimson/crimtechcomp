def urlname(fullname):
    return fullname.lower().replace(' ', '-')


def fullname(model, field, urlname):
    """
    Takes a `model' and matches the `urlname' to an actual `field' name
    and returns the correctly formatted value.
    """
    full = urlname.replace('-', ' ')
    try:
        a = model.objects.get(**{(field + '__iexact'): full})
        return getattr(a, field)
    except:
        return full
