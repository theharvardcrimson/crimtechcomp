def say_hello():
    print("Hello, world!")

# Color: blue

# TODO: implement
def echo_me(msg):
    print(msg)

# TODO: understand and remove
def string_or_not(d):
    exec(d)

# TODO: understand formatting - can you eliminate the redundancy here?
def append_msg(msg):
    #print("Your message was: {}.".format(msg))
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
    for i in range(len(lst)):
        s = lst[i]
        lst[i] = s[::-1]
    return lst

# TODO: implement
def challenge2(n):
    new_lst = list()
    end = int(n** (.5))+1
    temp = 0
    for i in range(1, end):
        mod = n%i
        if (mod ==0):
            temp = n/i
            new_lst.append((i,temp))
    return new_lst
