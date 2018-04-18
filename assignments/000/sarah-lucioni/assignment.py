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
# Instead of creating a new list and copying each element + 1 to the new list, simply add
# one to each element of the current list.
def increment_by_one(lst):
    for x in range(len(lst)):
        lst[x] = lst[x] + 1

    return lst

# TODO: understand - do we need a return statement here? why?
# We don't need the return statement, but it helps us check in a REPL and make sure the function
# actually worked correctly.
def update_name(person, new_name):
    person["name"] = new_name

    return person

# TODO: implement - these are still required, but are combinations of learned skills + some
def challenge1(lst):
    # loops through every element of a string list and reverses the string by using a slice with a step of -1
    for x in range(len(lst)):
        lst[x] = lst[x][::-1]

    lst.reverse()
    return lst

# TODO: implement
def challenge2(n):
    # create an empty list
    factors = []
    # loop through the possible factors of n (only need to look at one half)
    for i in range(1, int((n + 1) / 2)):
        # if i is a factor of n, append the tuple (i, n/i) to the factors list
        if n % i == 0:
            factors.append((int(i), int(n/i)))

    return factors
