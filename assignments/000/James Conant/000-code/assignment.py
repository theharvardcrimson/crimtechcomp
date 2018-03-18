# James Conant 

def say_hello():
    print("Hello, world!")

# Color: Purple

# TODO: implement
def echo_me(msg):
    print(msg)

# TODO: understand and remove

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
    for x in range(0,len(lst)):
        lst[x] += 1

    return lst

# TODO: understand - do we need a return statement here? why?
def update_name(person, new_name):
    person["name"] = new_name

    return person

# TODO: implement - these are still required, but are combinations of learned skills + some
def challenge1(lst):
    new_lst = list()

    for x in lst:
        new_lst.append(x[::-1])

    return new_lst


# TODO: implement
def challenge2(n):
    lst = []

    for x in range(1,int(n / 2)):
        if n % x == 0:
            lst.append((x,int(n / x)))

    return lst

