def say_hello():
    print("Hello, world!")


# Color: blue

# TODO: implement
def echo_me(msg):
    print(msg)

# TODO: understand and remove
def string_or_not(d):
    exec(d)

# TODO: understand formatting - can you eliminate the redundancy here?
def append_msg(msg):
    print("Your message should have been: {}!".format(msg))

# TODO: understanding classes (an introduction)
class QuickMaths():
    def add(self, x, y):
        return x + y

    def subtract(self, x, y):
        return x - y

    def multiply(self, x, y):
        return x * y

    def divide(self, x, y):
        return x / y

# TODO: implement - can you do this more efficiently?
def increment_by_one(lst):
    new_lst = list()

    for x in lst:
        new_lst.append(x + 1)

    return new_lst

# TODO: understand - do we need a return statement here? why?
def update_name(person, new_name):
    person["name"] = new_name

    return person

# TODO: implement - these are still required, but are combinations of learned skills + some
def challenge1(lst):
    # create empty list
    new = list()
    # reverse strings in list and append to new list
    for x in lst:
        new.append(x [:: -1])
    # reverse order of strings
    new.reverse()
    return new

# TODO: implement
def challenge2(n):
    # create an empty list
    factors = []
    # iterate from 1 to n + 1 and get factors
    for x in range(1, n+1):
        if n % x == 0:
            factors.append(x)
    # split list of factors by half
    f1 = factors[:len(factors)//2]
    f2 = factors[len(factors)//2:]
    # make a list of tuples of pairs of factors
    result = list(zip(f1,f2))

    return result
