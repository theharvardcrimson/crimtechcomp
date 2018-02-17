def say_hello():
	print("Hello, world!")
	
#say_hello()

# I'm gonna do some code!
#print("I am not executed when in the triple quotes, but once you remove them...PLS REMOVE ME K THX BAI")

# TODO: implement
def echo_me(msg):
    if type(msg)==type("dog"):
        print(msg)
    else:
        return None
#echo_me("Echooo")

# TODO: understand and remove
def string_or_not(d):
    if type(d)==type("dog"):
        return exec(d)
        return True
    else:
       return False

# TODO: understand formatting - can you eliminate the redundancy here?
#def append_msg(msg):
 #       if type(msg)==type("dog"):
            
    #print("Your message was: {}.".format(msg))
 #               msgx=msg+'!'
                
 #               print("Your message should have been: ", msgx)
 #       else:
 #               return None
def append_msg(msg):           
    #print("Your message was: {}.".format(msg))
 #               msgx=msg+'!'
        msgx="Your message should have been: "+msg+'!'
        print(msgx)
        #print("Your message should have been: ",msgx)

# TODO: understanding classes (an introduction)
class QuickMaths():
    def add(self, x, y):
        return x+y
        #return None

    def subtract(self, x, y):
        return x-y
        #return None

    def multiply(self, x, y):
        return x*y
        #return None

    def divide(self, x, y):
        return x/y
        #return None

# TODO: implement - can you do this more efficiently?
#def increment_by_one(lst):
#    new_lst = list()

 #   for x in lst:
 #       new_lst.append(x - 1)

   # return new_lst

def increment_by_one(lst):
    new_lst = list()

    for x in lst:
        new_lst.append(x + 1)

    return new_lst

# TODO: understand - do we need a return statement here? why?
def update_name(person, new_name):
    person["name"] = new_name

    return person
# The return statement is necessary for functions-- it makes sure the function gives back a useful value and ends the function's use

# TODO: implement - these are still required, but are combinations of learned skills + some
def challenge1(lst):
    new_lst=list()
    for i in range(len(lst)):
        word=lst[-1*i-1]
        new_word=''
        for k in word:
                        new_word=k+new_word
        new_lst.append(new_word)

    return new_lst
    #return None

# TODO: implement

def challenge2(n):
        lst=list()
        #indicator= True
        if n==0:
                lst=list()
        elif n==1 or n==2:
                x=(1,n/1)
                lst.append(x)
        else:
            #check for prime
            #def isPrime(n):
                for i in range(2,n):
                    print("i=",i)
                    print("n mod i=",n%i)
                    if (n % i)==0:
                        #print(n%i)
                        indicator="composite"
                        factor=i
                        print(factor)
                        break
                        #return indicator
                    else:
                        #print(i)
                        #print(n%i)
                        indicator="prime"
                        #return indicator
                #return indicator
            #indicator=isPrime(n)
                if indicator=="composite":
                    x=(1,n/1)
                    y=(factor,n/factor)
                    lst.append(x)
                    lst.append(y)
                elif indicator=="prime":
                    x=(1,n/1)
                    lst.append(x)
        return lst                               
                                
                
















