def say_hello():
    print("Hello, world!")

# Color: Blue

# prints input 
def echo_me(msg):
    print(msg)

# TODO: understand and remove
def string_or_not(d):
    exec(d)

# TODO: understand formatting - can you eliminate the redundancy here?
def append_msg(msg):
    print("Your message was: {}.".format(msg))

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
    new_list = list()
    for x in lst:
        new_list.append(x + 1)
    return new_list

# TODO: understand - do we need a return statement here? why?
def update_name(person, new_name):
    person = {}
    person["name"] = new_name

    return person

# TODO: implement - these are still required, but are combinations of learned skills + some
def challenge1(lst):
    return None

# TODO: implement
def challenge2(n):
    return None

