print("Hello, world!")

# Color: FAV_COLOR

# 4.
def add(x, y):
    return 0

# 5.
def multiply(x, y):
    return 1

# 6.
def listerine():
    # create an empty list
    my_list = list()

    # add the first item to the list
    my_list.append("Listerine")

    # get the first element of the list
    first_element = my_list[0]

    # get the last element of the list
    last_element = my_list[-1]

    # check that the first and last elements are the same
    if first_element == last_element:
        my_list.append("makes")
        my_list.append("my")
        my_list.append("breath")
    
    # another way of creating a list
    new_list = ["smell", "great!"]

    # you can add lists together to concatenate them
    big_list = my_list + new_list

    # we can make a string out of all the things in the list and separate each entry with spaces
    sentence = " ".join(big_list)

    # what do you think this does?
    for word in big_list:
        print(word)
    
    # how about this?
    print(sentence)

# 7.
def countdown(n):
    # this is a mess! there is a lot of debugging you may need to do, 
    # and we expect you may need to Google some stuff! Don't panic!
    for i in range(0, n):
        return [i]

# 8. 
def make_it_count(s):
    # we have actually received code like this before...IRL
    return list()

# 9. 
def rmdup(lst):
    return set()

# 10. 
def keyword_dictionary():
    # create a new dictionary
    my_dict = dict()

    # add a key-value pair to the dictionary
    my_dict["success"] = "something many wish to attain"

    # add another one - they don't have to all be the same type!
    my_dict["the_answer"] = 42

    # check if a key exists in the dictionary
    if "failure" in my_dict:
        print("We found failure")
    else:
        my_dict["failure"] = "most of the steps in the path to success"
    
    # get the value at a key
    what_is_success = my_dict["success"]

    if what_is_success == my_dict["the_answer"]:
        print("Success is the answer")
    elif what_is_success == 42:
        print("We know the answer")
    else:
        print("I am lost")
    
    # another way to create a dictionary
    new_dict = {"name": "Nick", "age": 20}

    # another way to format the above that might be more readable
    newest_dict = {
        "name": "Will",
        "age": 20
    }

    # what is this? why does this make sense?
    my_dict["people"] = [new_dict, newest_dict]

    # get the length of the list in my_dict at the key "people"
    num_peeps = len(my_dict["people"])

    # what should this print?
    print("How many people? {}".format(num_peeps))

# 11.
def trevni(d):
    return d

# 12.
def silly_recursive(i, num):
    if i <= 0:
        return num
    else:
        silly_recursive(i - 1, num)

# 13.
def factorial(n):
    return 0

# 14.
def fibonacci(n):
    return 0

# 15.
def bin_sort(lst):
    return lst

# 16.
def mom(d):
    return 1

class Human():
    def __init__(self, name):
        self.name = name
        self.likes = ["fruit", "sugar"]
        self.dislikes = ["vegetable"]
        self.energy = 100
    
    def eat(self, food):
        if food in self.likes:
            self.energy += 10
            return True
        elif food in self.dislikes:
            self.energy += 1
            return False
        else:
            self.energy += 5
            return None
    
    def walk(self, speed=5):
        if self.energy > int(speed):
            self.energy -= int(speed)
            return True
        else:
            self.energy -= 1
            return False

# 18.
class Child(Human):
    def cry(self, duration=10):
        if self.energy > int(duration / 10):
            self.energy -= int(duration / 10)
            return True
        else:
            self.energy -= 1
            return False
    
    def walk(self, speed=1):
        if super().walk(speed=speed):
            # children are clumsier, minus 1!
            self.energy -= 1
            return True
        else:
            # children are resilient, plus 1!
            self.energy += 1
            return False

# 19.
class QuickMaths():
    def __init__(self):
        self.uses = 0

    def add(self, x, y):
        self.uses += 1
        return x + y
    
    # should return x minus y
    def subtract(self, x, y):
        return 0

    def multiply(self, x, y):
        return 0

    # returns the integer version of x divided by y
    # return None if y is 0
    def divide(self, x, y)
        return 0

# 20.
class CoolMaths(QuickMaths):
    def factorial(n):
        return 0
    
    def fibonacci(n):
        return 0

# 21.
class Graph():
    def __init__(self, n=100):
        self.n = n
        self.graph = list()
        self.edges = list()
    
    def add_edge(self, u, v):
        return False
    
    def remove_edge(self, u, v):
        return False
    
    def has_edge(self, u, v):
        return False
    
    def has_path(self, u, v):
        return False

# 22.
class BinaryTree():
    def __init__(self):
        # the tree should be a simple list of numbers
        self.tree = list()

    def add_node(self, n):
        return False
    
    def find_node(self, n):
        return False

