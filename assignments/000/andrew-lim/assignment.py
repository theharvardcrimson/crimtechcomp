from math import *

print("Hello, world!")

# Color: blue

def say_hello():
	print("Hello, world!")

# TODO: implement
def echo_me(msg):
	print(msg)

# TODO: understand formatting - can you eliminate the redundancy here?
def append_msg(msg):
    print("Your message should have been: " + msg + "!")

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
    return list(map(lambda x: x + 1, lst))

# TODO: understand - do we need a return statement here? why?
# Yes - to return the updated list.
def update_name(person, new_name):
    person["name"] = new_name

    return person

# TODO: implement - these are still required, but are combinations of learned skills + some
def challenge1(lst):
    return list(map(lambda str: str[::-1], lst))[::-1]

# TODO: implement
def challenge2(n):
    return [(i, n / i) for i in range(1, int(floor(sqrt(n))) + 1) if not n % i]
