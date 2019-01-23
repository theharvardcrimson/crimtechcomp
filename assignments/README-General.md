### Introduction

Ok, so maybe you took CS50, maybe you didn't. Maybe you think our comp meetings are lame, maybe you love our terrible jokes. We don't know how you're honestly feeling, and trust us, if we could be mind readers, we wouldn't be. We have plenty of our own thoughts to sort through. However, we are going to try and make this comp process as useful and educational to you as possible. Some of you may know more HTML or Python or Django than us, that's possible. Some of you may not know what a terminal is. It's whack. Regardless, we're here for you, and we're going to try to help larn you some things. Speaking of, here's a list of items:

- CLI
- REPL
- SSH
- Function
- Object
- Class
- Attribute
- Method
- Shell
- Script

If < 4 of those terms make sense to you (and I mean immediately click, like you could explain it to us with examples), please read this whole doc.

If > 4 and < 10 of those make sense, please skim this entire doc.

Otherwise, feel free to skip to the Instructions section if you are so inclined. 

-----

### Basics

Generally:
- CLI - Command Line Interface. Ever used Terminal or Command Prompt (from here on out these will be referred to as the "console")? If yes then congrats, you've at least seen this. 

- REPL - Read Evaluate Print Loop. This gives you access to a live-action Python interface, where you can type in Python commands and see their outputs. Ever typed ```python``` or ```python3``` into a console and then executed some commands (i.e. ```4 + 4```, ```print("Hello, world")```, etc.)? If yes, then sweet you know this too. Else, please go ahead and try that, it's cool (not to mention helpful for debugging, later). Note: REPL's can be in any language, they're not limited to Python. 

- SSH - Secure SHell. This lets you connect remotely to a machine, and then your console is for most intents and purposes, "on" that machine. For example, if I can ssh into your computer, I can control your computer (at least as much as the user I authenticated as). This will be explained a bit more later. 

- Function - A set of code that fulfills a specific purpose. Sometimes it can take arguments for use within the function. You've seen them already, and they can be varying levels of abstract. Some real-world functions could be ```drive_to_work()```, or maybe ```cook_eggs(num_eggs)``` (has an argument, "num_eggs")

- Object - A virtual representation of something for the purpose of use in code. In Python, we initialize Objects of certain classes (see below).

- Class - A broad specification for how a given object works and how to build it. For example, you could have ```class Animal():```. Classes can inherit from each other too, so you might also have ```class Lion(Animal):``` (what do you think that does?) And then we could build specific _Lion_ objects: ```pet_lion1 = Lion(); pet_lion2 = Lion()```

- Attribute - You can think of these as properties or _attributes_ of a given object. The broad class _Animal_ might have the attributes _name_, _species_, _height_, _weight_ that apply to all _Animal_s. The _Lion_ class might have specific attributes for lions only: _prideName_, _maneLength_

- Method - These are like the actions that a class can take. Sometimes they require arguments, sometimes they don't. Sometimes they return a value, sometimes they don't. They're functions that are built into classes. For the _Animal_ class, there might be the methods: _walk(direction)_, _sleep(time)_, _blink()_, and _makeNoise(msg)_. The _Lion_ class might then have its own methods in addition: _hunt()_, _migrate()_, and they might also override one of _Animal_'s methods in order to reimplement it: _makeNoise(msg)_ can be rewritten so that it roars instead of making a generic noise (which wouldn't be very lion-like).  

- Shell - Generally, an interactive interface for entering commands in a console that lets you make directories, read files, edit settings, and so much more. Often, you are using the ```bash``` shell on your console (for UNIX systems, like OSX and almost any Linux distro). There are many kinds of shell - ```zsh```, ```ash```, ```sh``` - to name a few. 

- Script - A file that specifies a set of instructions that can all be executed by only typing one command. In this case, we will show you shell scripts, which are scripts written to run commands in a specific shell, but there are many kinds, and they all refer to a somewhat general language for interacting with a computer. 

Note: in the above toy examples, we named our variables kinda funny - some looked like "my_variable_name" and other like "myVariableName." Both are okay to use, but be consistent. Do not mix them like we did (smh @ ourselves). 

An aside on "higher" versus "lower" level:
We do not mean skill or complexity here, we instead are referring to if you imagined a computer was kinda abstractly set up like so

```
Graphic User Interface
Python
C
Assembly Language
1's and 0's
Hardware
```

then Hardware would be extremely "low-level" and the Graphic User Interface (GUI) would be very "high-level." That's all. No inherent positive or negative connotations. 

We know that the above may be a lot to take in - there are tons and tons of terms in CS that sound like they were invented solely to confuse people. Over time, you get used to those terms and start to use them yourself, we promise. 

-----