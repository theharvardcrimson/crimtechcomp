import math

def say_hello():
    print("Hello, world!")

# Color: blue

def echo_me(msg):
    print(msg)

def append_msg(msg):
    print("Your message should have been: {}!".format(msg))

class QuickMaths():
    def add(self, x, y):
        return x + y

    def subtract(self, x, y):
        return x - y

    def multiply(self, x, y):
        return x * y

    def divide(self, x, y):
        return x / y

def increment_by_one(lst):
    new_lst = list()

    for x in lst:
        new_lst.append(x + 1)

    return new_lst

# We do not need a return statement here because Python passes the actual dictionary object to the function (not a copy) so the changes made in the function are preserved outside the function
def update_name(person, new_name):
    person["name"] = new_name

def challenge1(lst):
    ret_lst = []
    for word in lst:
        ret_lst.append(word[::-1])
    ret_lst.reverse()
    return ret_lst

def challenge2(n):
    factors = []
    for i in range(1, int(math.sqrt(n)) + 2):
        if (n % i) == 0:
            factors.append((i, n / i))
    return factors
