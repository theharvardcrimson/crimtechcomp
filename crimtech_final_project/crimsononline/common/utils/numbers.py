def gcd(x, y):
    while y:
        x, y = y, x % y
    return x


def reduce_fraction(num, denom):
    x = gcd(num, denom)
    return (num / x, denom / x)
