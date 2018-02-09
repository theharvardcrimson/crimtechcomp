def say_hello():
    print("Hello, world!")

# Color: Blue

# TODO: implement
def echo_me(msg):
    raw_input = msg
    print(msg)

# TODO: understand and remove ???????
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
# We do need a return statement if we want the program to return/show the person's name after
# someone chooses to update the name in the dictioary. Otherwise, we don't need a
# return statement
def update_name(person, new_name):
    person["name"] = new_name

    return person

# TODO: implement - these are still required, but are combinations of learned skills + some
def challenge1(lst):
    new_list = lst.reverse()
    return new_list

# TODO: implement (return divisors in a list)
def challenge2(n):
    factors = list()
    for i in range(1, int(n**0.5)+1):
        if n % i == 0:
            factors.append((i, n / i))
    return factors
