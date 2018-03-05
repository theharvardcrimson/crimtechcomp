def say_hello():
    print("Hello, world!")

# Color: green

# TODO: implement
def echo_me(msg):
    print(msg)

# TODO: understand and remove
def string_or_not(d):
    exec(d)

# TODO: understand formatting - can you eliminate the redundancy here?
def append_msg(msg):
    print("Your message should have been: {}.".format(msg))

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
    return [x + 1 for x in lst]

# TODO: understand - do we need a return statement here? why?
# no - the actual dictionary object is changed, not just a copy
def update_name(person, new_name):
    person["name"] = new_name

# TODO: implement - these are still required, but are combinations of learned skills + some
def challenge1(lst):
    return [x [::-1] for x in lst][::-1]

# TODO: implement
def challenge2(n):
    lst = []
    limit = n
    i = 1
    while i < limit:
        if n % i == 0:
            div = n // i
            lst.append((i, div))
            limit = min(limit, div)
        i += 1
    return lst
