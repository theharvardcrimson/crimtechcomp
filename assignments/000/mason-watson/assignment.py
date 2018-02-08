def say_hello():
    print("Hello, world!\n")
# this is a singleline comment, PLEASE EDIT
#TODO: implement
def echo_me(msg):
    print(msg)

# TODO: understand and remove
def string_or_not(d):
    if type(d) == str:
        return True
    else:
        return False

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

# TODO: implement - these are still required, but are combinations of learned skills + some
def challenge1(lst):
    new_lst = list()

    for x in lst:
        new_lst.append(x[::-1])
    return list(reversed(new_lst))

# TODO: implement
def challenge2(n):
    if n == 0:
        return list()
    y = n - 1
    i = 2
    new_lst = list()
    new_lst.append((1, n))
    while i < y:
        if n % i == 0:
            y = int(n / i)
            new_lst.append((i, y))
        i += 1
    return new_lst
