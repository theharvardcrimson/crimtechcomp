def say_hello():
    print("Hello, world!")


# Color: Blue

# TODO: implement
def echo_me(msg):
	print(msg)



# TODO: understand formatting - can you eliminate the redundancy here?
def append_msg(msg):
    print("Your message should have been: " + msg + "!")

# TODO: understanding classes (an introduction)
class QuickMaths():
    def add(self, x, y):
        return None

    def subtract(self, x, y):
        return None

    def multiply(self, x, y):
        return None

    def divide(self, x, y):
        return None

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
    new_list = list()
    m = range(len(lst))
    l = len(lst) - 1
    for num in m:         #iterates thru each word in lst, starting with the last one
        word = lst[l]
        new_word = ""
        i = len(word) - 1
        for n in range(len(word)): #iterates thru each letter in word, starting with the last one
            new_word += word[i]
            i-= 1
        new_list.append(new_word)
        l -= 1
    print(new_list)


# TODO: implement
def challenge2(n):
    lst = list()
    lst2 = list()
    for x in range(1, n+1): #checks for all numbers that can divide n evenly
        if n % x == 0:
            lst.append((x, n/x))
    if len(lst)%2==0:       #if n is even, every entry is doublecounted so half the entries are thrown out
        for num in range(len(lst)/2):
            lst2.append(lst[num])
    elif len(lst)%2 !=0:   #if n is odd, half the entries -1 are thrown out
        for num in range(len(lst)/2 + 1):
            lst2.append(lst[num])
    print(lst2)

    

