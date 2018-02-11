def say_hello():
    print("Hello, world!")

# Color: purple and gold

# TODO: implement
def echo_me(msg):
    print(msg)


# TODO: understand formatting - can you eliminate the redundancy here?
def append_msg(msg):
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
        return float(x)/ float(y)

# TODO: implement - can you do this more efficiently?
def increment_by_one(lst):
    new_lst = list()

    for x in lst:
        new_lst.append(x + 1)

    return new_lst

# TODO: understand - do we need a return statement here? why?

# no, because in python we pass in by reference
def update_name(person, new_name):
    person["name"] = new_name

    return person

# TODO: implement - these are still required, but are combinations of learned skills + some
def challenge1(lst):
    for i in range(len(lst)):
        current = list(lst[i])
        current.reverse()
        current = "".join(current)
        lst[i] =current
    lst.reverse()
    return lst

# TODO: implement
def challenge2(n):
    results = []
    if n == 1 or n == 2 or n == 3:
        return [(1, float(n))]
    if n == 4:
        return [(1,4.0),(2,2.0)]
    for i in range(1, int(n/2)):
        if n % i == 0:
            results.append((i, float(n /i)))
    return results
