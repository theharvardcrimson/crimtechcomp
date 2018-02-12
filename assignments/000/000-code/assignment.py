import math

def say_hello():
    print("Hello, world!")

# Color: red


# TODO: implement
def echo_me(msg):
    print(msg)

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
# def increment_by_one(lst):
#     new_lst = list()

#     for x in lst:
#         new_lst.append(x + 1)

#     return new_lst

def increment_by_one(lst):

    for i in range(len(lst)):
        lst[i] += 1
    return lst

# TODO: understand - do we need a return statement here? why?
# yes, we need a return statement, so we can receive the updated person dictionary
def update_name(person, new_name):
    person["name"] = new_name
    return person

# TODO: implement - these are still required, but are combinations of learned skills + some
def challenge1(lst):
    for i in range(len(lst)):
        lst[i] = lst[i][::-1]
    lst.reverse()
    return lst

# TODO: implement
def challenge2(n):
    lst = []
    for i in range(1, int(math.floor(math.sqrt(n))) + 1, 1):
        if n % i == 0:
            lst.append((i, n/i))
    return lst


