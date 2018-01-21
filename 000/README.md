# Intro - Python
So you think you can code (haha, we're so funny, sorry). In this repository, you'll find a file called _assignment.py_. That ".py" extension at the end tells the computer it's a Python file, which is useful for all sorts of things. This guide will assume you know very very little about computers, and if you want a gauge of where you're at, read the following list:

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

If < 3 of those terms make sense to you (and I mean immediately click, like you could explain it to us with examples), please read this whole doc.

If > 3 and < 10 of those make sense, please skim this entire doc.

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
Graphic Interface
Python
C
Assembly Language
1's and 0's
Hardware
```

then Hardware would be extremely "low-level" and the Graphic User Interface (GUI) would be very "high-level." That's all. No inherent positive or negative connotations. 

-----

### Instructions:
This code and very document you're reading is currently situated in a Github repo - specifically, ours. And we know you've done enough reading to choke a donkey, so let's get you going on coding. In an effort to teach you about coding and good practices, we're having your assignments done through Git, and using the web interface tool we provided, you can keep track of everything. 

Steps to submit an assignment; commands are listed below:

1. Fork this repository, the whole thing. You should fork to your own account, and get a nice little copy of this repository of assignments. 

2. On your own copy of this repository, clone it to your laptop to get access to work on it. On your Github page for this repository in the top right, there is a button that lets you copy the link to the repository. In your console you can then use 
```
    git clone link
```
where "link" is the link you copied to clone it to your computer. Then use 
```
    cd repo_name
``` 
You are now inside your repo. 

3. The structure is "repo_name/###/###-code/, where ### is the assignment number. You need to make a directory in "repo_name/###/" called "your-name" Assuming you're in the repo's root or highest level directory (you can type 
```
    pwd
``` 
to print your working directory and should see something like "blahblahblah/repo_name" or "~/repo_name" print to the console). Then, you can list the contents of this directory with
```
    ls
```
You should see each of the assignment numbers as well as "README.md" and "GET_STARTED.md". To make the required directory, go ahead and change your directory to be inside repo_name/###/ (do you remember how?), then use 
```
    cp -r ###-code your-name
```
On UNIX, "cp" is to copy, "-r" tells it to copy recursively (copies all files in a directory by recursively search through until it runs out of files to copy), and the first argument ("###-code") is the source name, the second ("your-name") is the destination name. 

4. Now that you have a copy of the assignment that can be attributed to you, go ahead and work on it, following the instructions within the assignment. If you want to check your assignment at any one time, please use the ```check ###``` command you installed at the beginning. This command assumes you are in the directory containing _assignment.py_ (do you know how to check that?) Once in that directory, running ```check ###``` (where "###" is the assignment number) should let you know how you're doing. Try to debug on your own at first, then try to Google stuff (StackOverflow, for example), then maybe try some Youtube tutorials. If you're stuck and frustrated, take a break, eat an apple, etc. then come back. After you've tried to help yourself, ask a friend, an Associate, or us (in any order), and someone will be able to help you. 

5. When you're done (you think), make sure you've added, committed, and pushed all of your changes (local -> Github). Now it's time to submit a pull request to merge this with the original repository. You can do this by going to the repository on Github, and at the top, clicking "open pull request." This will bring up some simple dialogs. Once you've completed that, you'll see the automated tests that get run against your code. If they all pass, you'll know. If they don't, you'll know. They're mostly there to make sure you didn't tinker with any of the other code there. 

6. When you've passed all the tests, and your request says something like "Can be automatically merged", please comment on the last edit/commit (at the bottom of the pull request page, there's a comment section). And copy/paste + fill out this template:

```
Difficulty: #
Best Part: blabbity blah
Worst Part: hoopity hoopla
Additional Comments: asd;fkjasd;lfkj;aslkdfj;askldjf
```

Note: please do not leave our placeholders there, we've already laughed at how fantastically funny they are and would like your actual input (seriously, answer at least the first three). 

Difficulty should be out of 10, where 9 and 10 were literally impossible for you to do, and 1 and 2 made you laugh. 

For example:

```
Difficulty: 6
Best Part: Learned how to use functions
Worst Part: Didn't understand recursion
Additional Comments: Y'all are awesome
```

7. Congrats!