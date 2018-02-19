def say_hello():
	print("Hello, world!")



# Color: green

# Prints user entered string
def echo_me(msg):
	print(msg)

# User inputs a string and function adds an exclamation point
def append_msg(msg):
    print("Your message should have been: {}!".format(msg))

# Class of the 4 arithmetic operations
class QuickMaths():
    def add(self, x, y):
        return x + y

    def subtract(self, x, y):
        return x - y

    def multiply(self, x, y):
        return x*y

    def divide(self, x, y):
        return x/y

# Takes each element in a list and adds one
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
	length = len(lst)
        i = 0
	new_lst = list()
	while i <= length - 1:
		new_lst.append(lst[i][::-1])
		i = i + 1
	final_lst = list()
	i = length - 1
	while i >= 0:
		final_lst.append(new_lst[i])
		i = i-1
	return final_lst


# yeet
def challenge2(n):
	n = int(n)
	lst = list()
	i = 1
	while i <= n:
		if n%i == 0:
			if (n/i,i) in lst:
				lst=lst
			else:
				lst.append((i,n/i))
		i = i + 1

	return lst
