### The Shell

This is something so enigmatic that it's become emblematic of the hacker, the computer scientist, and the tech nerd, all at once. If you see someone pull out their laptop and whip open a Command Prompt or a Terminal, you know that they fall into at least one of the aforementioned groups, and that they now know all of your bank information. LOL, that's not at all true, but it can be a little tricky getting started with The Shell, so we're here to help!

-----

### Terminology and Definitions

Sometimes you'll hear people say that it's The Shell, or maybe a terminal, a console, bash, etc. What do these terms even mean? Weirdly, they all technically describe different things, and yet we can use them roughly interchangeably. If that sounds annoyingly ambiguous, it kinda is, but you'll live. 

Regardless of the term used, when someone says "commandline" or "console" or "bash," they usually mean that they're interfacing with their computer in such a way that they can type out text commands to control the computer and receive text output based on those commands. In order to see what we mean, please snag a bash shell on your terminal of choice (sounds silly or complex depending on how arrogant you are, right?). We simply mean that if you're on OSX you should open up Terminal and if you're on a Linux distribution...do the same thing. If you're on Windows, please don't. Jk, you should just use Bash on Ubuntu on Windows 10 or use a virtual machine. Regardless, somehow get access to a shell where you can type in commands, and we will be descibing commands that work well in particular in bash.

-----

### Basics - Navigation

Ok, so let's imagine that you have the ability to walk vertically down an inverted tree. At each place in the tree, leaves can grow willy nilly, and the tree can branch however many times it would like. Thus, the root of the tree is at the top, the highest point actually, and it grows downward indefinitely. In Linux distributions, the root of our tree, or the place where everything starts filesystem-wise, is ```/```, it is the highest directory, and it contains all. Nothing can go higher in the tree structure than ```/```.

You've presumably just opened up a Terminal, so you may be asking, how do I know which directory I'm in? Usually, you'll start in your home directory, which is often denoted as ```~```. To check the actual path name for your current directory, we can type the command ```pwd``` or "print working directory." This will print the directory you're currently in to your console/terminal window. Normally, you don't want to work all in your home directory, so we should also know how to Change Directory, or ```cd```. This command takes an argument in order to know where you'd like to go (if you don't give it an argument, it takes you to your home directory...go figure). But you probably don't know any directory paths off the top of your head (or maybe you do, you weirdo). In the case that you don't, you can LiSt out the current items in your current directory with the command ```ls```. You'll likely see some directories below your current directory. Maybe you have a directory called ```Desktop/```, for example. In order to navigate into it, you can type ```cd Desktop```, then type ```pwd``` to double check that you did what you think you did. 

We can also go up a directory by typing ```cd ..```, which means "change directory to the enclosing directory." tl;dr; go up a directory. If we wanted to go up 2 directories, we could type ```cd ../..```. All of these commands up till now have used what we call _relative paths_. You can also navigate directly to a path using ```cd /my/absolute/path```. Note that this type of path starts with ```/```, which was our root directory, container of all things. The reason for this is because we start with the highest directory's name, then list out all of the other things below. 

Navigation can be a little tricky to start with, so we recommend practicing. Alternatively, you can ignore our advice. Up to you.

-----

### Basics - Documents

Ok, so you've learned to navigate a bit, and now we're going to talk about how documents work in this type of system. We can look at what's inside a file with the command ```cat``` - ```cat myfile.txt``` will print the contents of _myfile.txt_ to the console. If you want to create a new file, you can use ```touch newfile.txt``` in order to create it. You can also make new directories with ```mkdir newdirectory```. If you want to edit a file via the commandline, you can use your text editor of choice - common ones are ```vi```, ```nano```, and ```vim```. Though there are more. 

Note, documents might not be immediately visible if you type ```ls``` if their name starts with "." since this means that they are hidden files and directories. 

-----

### Basics - Options and Flags

Many of the commands you've seen before have options and flags that can be passed to the command in order to change the command's behavior. For example, ```ls -a -l -h``` will list out all of the contents of the current directory ("-a"), including hidden files and directories. It will also print the long form ("-l") in human-readable form ("-h"). 

-----

### Ending Notes

Sorry, we don't want to overwhelm you with knowledge, but there are hundred and hundreds of other things to learn about the shell and commandline. There's so much complexity that whole books have been written on it. However, the above should get you somewhat familiar with how things work. If you have further questions, please always feel free to ask us!
