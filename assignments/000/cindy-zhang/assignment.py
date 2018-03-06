import math

def say_hello():
    print("Hello, world!")

# Color: Blue

# TODO: implement
def echo_me(msg):
    print(msg)

# TODO: understand formatting - can you eliminate the redundancy here?
def append_msg(msg):
    print("Your message should have: {}!".format(msg))

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

qm = QuickMaths()
print(qm.divide(6, 3))

# TODO: implement - can you do this more efficiently?
def increment_by_one(lst):
    for x in range (len(lst)):
        lst[x] += 1
    return lst

a = [1, 2, 3, 4, 5]
print(increment_by_one(a))

# TODO: understand - do we need a return statement here? why
# You don't need to return person b/c it still updates, you just need to print(p1), etc. to see updates
def update_name(person, new_name):
    person["name"] = new_name

p1 = dict()
p1["name"] = "Klaus"
p1["height"] = "10'"
p2 = {"name": "Ricardo", "height": "72'"}
update_name(p1, "Nicholas")
update_name(p2, "Richard")
print(p1)
print(p2)

# TODO: implement - these are still required, but are combinations of learned skills + some
def challenge1(lst):
    lst.reverse()
    return lst

str_lst = ['hello', 'goodbye', 'level']
print(challenge1(str_lst))

# TODO: implement
def challenge2(n):
    lst = []
    for i in range (1, int(math.sqrt(n)) + 1):
        if n % i == 0:
            lst.append([i, int(n/i)])
    return lst

print(challenge2(1))
