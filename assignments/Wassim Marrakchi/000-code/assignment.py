# Color: Crimson

def say_hello():
    print("Hello, world!")

# Prints message back out to console
def echo_me(msg):
    print(msg)

def string_or_not(d):
    exec(d)

def append_msg(msg):
    print("Your message should have been: {}!".format(msg))

# TODO: understanding classes (an introduction)
class QuickMaths():

    def add(self, x, y):
        return x+y

    def subtract(self, x, y):
        return x-y

    def multiply(self, x, y):
        return x*y

    def divide(self, x, y):
        return x/y

# TODO: implement - can you do this more efficiently?

def increment_by_one(lst):
    for x in range(len(lst)):
        lst[x] = lst[x] + 1
    return lst

# TODO: understand - do we need a return statement here? why?
def update_name(person, new_name):
    person["name"] = new_name

# TODO: implement - these are still required, but are combinations of learned skills + some
def challenge1(lst):
    lst.reverse()
    new_lst = []
    for x in lst:
        string = ""
        for y in range(len(x)):
            string = x[y] + string
        new_lst.append(string)
    return new_lst


# TODO: implement
def challenge2(n):
    return None
