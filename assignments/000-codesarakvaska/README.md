## 000
Let's begin! (FINALLY!!)

------

### assignment.py - Intro
At first, this contains only a single line of executable code:
```python
print("Hello, world!")
```
The rest is between triple quotes, which is Python's way of denoting a multi-line comment (things that won't be executed). You can use "#" for single line comments, and we ask that you comment your code to help us understand what you're doing.

If you want to see what happens, go ahead and navigate into this directory (do you remember how?) and type ```python``` (you can verify the version by observing the numbers to the right of the word "Python" that get printed when the REPL opens)

Then, you can type the command

```python
    from assignment import *
```

This command tells the REPL to find the _module_ called "assignment" which has the filename "assignment.py" and for these purposes, must be in the same directory. If you receive the lovely

```python
ImportError: No module named assignment
```

Verify that you are in the correct directory and that you spelled everything correctly, we promise, it'll work. When it does work, it will import everything ("*") from the module "assignment" and since the command ```print("Hello, world")``` is chilling willy-nilly in the file, that code will be executed the moment you import the module. You can exit the REPL with
```
Ctrl-D or exit()
```
(and please do exit). Now let's say you don't want that code to automatically execute when you import (generally you indeed do not want automatic code execution like that). In "assignment.py," go ahead and replace the ```print``` statement (that means the entire line "print("Hello, world!")") with
```python
def say_hello():
    print("Hello, world!")
```
Any guesses as to what you've done? If you said "I built a function called 'say_hello' that takes no arguments and executes the command ```print('Hello, world!')```" then you are spot-on, nice job. Can you predict how we will use the command in the REPL? Go ahead and try it before we explain.

Explanation: go into your REPL (do you remember how?) in the correct directory (which one is that again? how can you verify you're in the correct directory?), and enter the same command we did before:
```python
from assignment import *
```
...and nothing happened...which is great！Now go ahead and enter the command
```python
say_hello()
```
That's a beautiful thing (it should have printed "Hello, world!"), if it did not, then please follow the above steps again and debug for a bit. You can also import just that command by using
```python
from assignment import say_hello
say_hello()

OR

from assignment import say_hello as greeting
greeting()

OR

import assignment as a
a.say_hello()
```
but these are slightly different, can you see how?

-----

### assignment.py - Specs
Here are the actual specifications for your assignment. These are meant to be somewhat rigid, and if you do not follow them precisely, tests will fail. Keep in mind that failing tests is A-Okay, don't get frustrated! This should be straightforward, but not inherently easy. Take your time and ask for help when needed:

Goals:
- Learn simple types and what can cause bugs in your code
  - Integers, strings, and more, galore!
- Learn simple syntaxes for some commands, including how to do elementary math
- Learn the basics of functions, objects, and classes (OH MY!)
- Have fun

Steps:

0. Please go ahead and remove the two triple quotes, one at the top of the file and one at the bottom. This should uncomment all of the functions we have for you.

1. Remove the print statement at the top that is not inside a function. Hint: (it tells you to remove it)

2. Replace the first comment in the file (the one telling you what a single line comment is) with a comment that has your favorite color in it, labeled with the key "Color:" (stick to relatively straightforward colors please @smartasseswholovethecolormauve). Ex. "# Color: green"

3. Ensure that the first function is as follows
    ```python
    def say_hello():
    ```
    and on execution, it only prints the statement "Hello, world!" and does nothing more, nothing less.

4. The echo_me function: the keyword ```pass``` makes sure Python knows code would go there, but doesn't actually do anything (needed because if it was blank, Python would want an indent afterward). Please implement the function so that when passed a message called "msg", it prints that message back out to console:
    ```python
    >>> echo_me("Hi, Nick")
    Hi, Nick
    >>> echo_me("Hey Richard!")
    Hey Richard!
    ```
    Hint: when a function has some variable as an argument (the variable here is "msg"), that variable takes on the value of whatever was passed in, but it only has this value _inside_ the function where it is being used (there are exceptions to this that we will discuss later). You can think of it like this: if I call ```echo_me("My custom message")``` then inside the "echo_me" function, "msg" has the value "My custom message" as a string.

5. The string_or_not function. It's a dangerous one in that it lets you execute CODE, which is not good...at least not if you don't know what you're doing. Play around with this function a bit to see some examples of what it means to be a string versus a string representation of code. For example, try running
    ```python
    >>> string_or_not("print(\"hello\")")
    ???
    >>> string_or_not("'print(\"hello\")'")
    ```
    These are very similar, but do different things, can you spot the difference? Note: generally " and ' are interchangeable, but they can be used to put strings within strings "'embedded string'". As with most things, feel free to generally use either, but be consistent.

6. The append_msg function. Can you see what it's doing? Play around with it until you understand what it does, then adjust it so that its usage is like so:
    ```python
    >>> append_msg("Hello!")
    Your message should have been: Hello!!
    >>> append_msg("no")
    Your message should have been: no!
    ```

7. Class time! We have the class QuickMaths (we know we're not funny, but c'mon, it's kinda funny, right?) with a bunch of methods. They're simple, and should be easy to implement, but what does this ```return``` statement do? And can you figure out how to test that they actually work? We'll leave this one mostly to you, without a usage example. Hint: remember you can instantiate and use an object of a class with
    ```python
    >>> qm = QuickMaths()
    >>> qm.subtract(1, 2)
    -1
    ```

8. The increment_by_one function. What it should do is iterate through a list of numbers, and return a list with each of them incremented by 1...except it doesn't. Please fix it.
    ```python
    >>> a = [1, 2, 3, 4, 5]
    >>> increment_by_one(a)
    [2, 3, 4, 5, 6]
    >>> b = [1.5, 2.5, 3.6, 4.7, 5.95]
    >>> increment_by_one(b)
    [2.5, 3.5, 4.6, 5.7, 6.95]
    ```

9. The update_name function. This should take in a dictionary representing a person and update the "name" key to have the value of the variable "new_name." Dictionaries are a new datatype, but they basically map values to a set of keys, so that you can access the values efficiently.
    ```python
    >>> p1 = dict()
    >>> p1["name"] = "Klaus"
    >>> p1["height"] = "10'"
    >>> p2 = {"name": "Ricardo", "height": "72'"}
    >>> `update_name(p1, "Nicholas")`
    {"name": "Nicholas", "height": "10'"}
    >>> update_name(p2, "Richard")
    {"name": "Richard", "height": "72'"}
    ```

10. The last set of functions (challenges 1 and 2), are required for the assignment; however, they are meant to be somewhat difficult (may require you to Google some syntax and some functions) but doable. Please note: Python is awesome and generally has the ability to do everything very conveniently - for example, to reverse a list, you can use ```my_list.reverse()```. So unless we tell you otherwise, please use these built-in functions.
    ```python
    >>> str_lst = ['hello', 'goodbye', 'level']
    >>> challenge1(str_lst)
    ['level', 'eybdoog', 'olleh']
    >>>
    >>>
    >>> challenge2(8)
    [(1, 8), (2, 4)]
    >>> challenge2(11)
    [(1, 11)]
    ```

11. Submit!

Best,

Your Comp Directors
