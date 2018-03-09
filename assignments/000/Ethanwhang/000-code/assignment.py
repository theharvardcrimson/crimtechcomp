def say_hello():
    print("Hello, world!")

# Color: Blue

def echo_me(msg):
    print(msg)

def string_or_not(d):
    exec(d)

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
    new_list = list()
    for x in lst:
        new_list.append(x + 1)
    return new_list

def update_name(person, new_name):
    person = {}
    person["name"] = new_name
    
    return person

# TODO: implement - these are still required, but are combinations of learned skills + some
def challenge1(lst):
    
    for x in range(len(lst)):
        lst[x] = lst[x][::-1]

    lst.reverse()
        
    return lst

# TODO: implement
def challenge2(n):
    factors = []
    for i in range(1, int(n**0.5)+1):
        if n % i == 0:
            factors.append((i, n / i))
    return factors

