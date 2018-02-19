from assignment import *

def say_hello():
    print("Hello, world!")

# Color: Aqua

# TODO: implement
def echo_me(msg):
    print (msg)
# TODO: understand and remove
def string_or_not(d):
    exec(d)

# TODO: understand formatting - can you eliminate the redundancy here?
def append_msg(msg):
    print("Your message was: {}.".format(msg))

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
    lst.reverse()
    newlist = []
    for i in range(len(lst)):
        rev = ""
        for j in range(len(lst[i]), 0, -1):
            rev = rev + lst[i][j - 1]
        newlist.append(rev)
    return newlist 

# TODO: implement
def challenge2(n):
    checked = set()
    lst = []

    for i in range(1, n):
        if n % i == 0 and (i, n/i) not in checked:
            lst.append((i, int(n/i)))
            checked.add((n/i, i))
    return lst

