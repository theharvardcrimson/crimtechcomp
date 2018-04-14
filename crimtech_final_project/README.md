# Crimson Tech Comp Final Project
Here's your final project! You get to view The Crimson the way associates see it for a couple weeks.

A lot of people have poured countless hours into The Crimson - as with all big projects, it is not easy to navigate.

... and as with all big projects, it will _inevitably contain bugs that need to be fixed_. The Crimson delivers content via the web to millions of readers per year. It is our duty to make sure that information is available and accessible to anyone.

Thankfully, Nick (nicholas.wong@thecrimson.com) and Richard (richard.m.wang@thecrimson.com) are here to help you, by introducing several bugs to a working version of The Crimson's website that you will need to fix.

In order to begin, you will need to set up a virtual environment and download the working database of The Crimson. A lot of this information is contained in `/docs/howto/local-server.rst`.

After you've done up to step 7, before continuing to step 8 you should copy `crimsononline/sample_local_settings.py` to `crimsononline/local_settings.py`. You can do this by `cd crimsononline; cp sample_local_settings.py local_settings.py`.

Please note that while you complete the tasks below, you will want to create a 'README-FINALPROJECT.md' similar to the markdown documents you've seen up to this point. We want you to document every fix you make - specifically, you should include three parts for each task - 1) how and when did you find the bug? 2) define the bug, and why it's important that you fix it (i.e. what is the bug's scope?) 3) your solution to the bug, ideally with a comment/argument as to why your solution is optimal, extensible, and robust. In summary, each bug fix requires a brief explanation that you could present to non-technical people who want to understand what exactly you've been up to, but is also useful to the technical people who follow in your footsteps. 

Along the lines of the above, this is not CS51. Your code is easier to comprehend if it has a concise comment explaining what the code you modify or add does. Please comment appropriately. 

# Task 1: Is it local_setttings or settings? No I mean settings?! IDK man. 
To get started, we should get the server working. I'm sure you remember the command to do it (rhymes with 'punserver'), so go ahead and try it out. I'll give you a hint, it has to do with settings.py. "Which one?" you may ask. Great question. We wonder that often when messing with our codebase. Welcome. Better hint, one of our associates accidentally "uninstalled" something we kinda need. 

# Task 2: Give me a 'U', give me an 'R', give me a 'Loved'!
What does that spell? URL! Sorry we're lame. Anyway, please fix the fact that literally everything is currently not accessible (try it out, I promise I'm not lying). Once you've fixed that, riddle me this: where is Flyby? This cascading of problems appears frequently with the Crimson's code...welcome pt. 2

# Task 3: MVTMVTMVTMVTMVTMVT
Seriously, if these three letters haven't been drilled into you by now, are you even comping Crimson Tech? Unfortunately, as a side effect of some associate's efforts to add new features (this really happens sometimes, by the way), some of our models have been broken. I can no longer add my favorite type of Newsletter, the 'Special Report' (look carefully). And even worse, I can't add subtitles to my content, WTF?!  

# Task 4: Look at Me!
Related to the above issues, there has been a recent issue with one of the views. In fact, I recommend that you visit [here](localhost:8000/section/opinion/ "View Bug"). Using your knowledge of URLs/views, can you please make these work again?
 
# Task 5: Serious Journalism
This task is simple, but you should realize its consequences. If you've noticed, someone at The Crimson has flexed their artistic muscles and replaced the font of the entire website with `Comic Sans MS`.

You should use the capabilities of your file editor to search through all the files for certain words that might help you find this malicious bit of code. Delete the offending edit.

Wait - why did this code even work? We learned that if a CSS rule is more specific, it should override the less specific rules that affect the same attribute. The reason is because this particular somebody added the snippet `!important`, which overrides even rules that target more specific elements. This has had a bad effect, and unfortunately is present in many places in The Crimson's codebase. Lesson 1: Take the time to modularize your divs and spans and the rules surrounding them, and do not go for the lazy "fix" of `!important`.

# Task 6: Adblock++
The Crimson heavily relies on ads in order to generate revenue. Unfortunately, unscrupulous users (such as yours truly) use Adblock in order to see less ads on Bitcoin, hot singles in your area, whatever.

The tech team has already created a basic form of anti-Adblock. Remember that command from Task 1? You'll want to use it again to find the Javascript file where this logic is located.

Your task is to implement a "better" version of anti-Adblock. This interpretation is up to you, and there are many ways to go about it. We've all seen different kinds of anti-Adblock: The New York Times has a "you have X remaining articles this month"; Forbes has a "we won't let you even look at the page until you disable Adblock".

Be creative! It's up to you how obnoxious or elaborate you want to be, although it should be clear you've put a reasonable amount of effort into this task.

Here are some ideas:

- You could look into Javascript's `window.location` property to redirect Adblock users. Or you could capture all click events and disable them!
- You could see how cookies are used in the current Adblock scheme; maybe extend this functionality to count down the number of remaining articles this month?
- You could create an HTML `div` and use CSS to create an opaque overlay that blurs the content on the page.

# Task 7: Sticky bar
This is another constructive task. The idea is simple: if you scroll far enough down the page, the navigation bar will "stick" to the top of the page, allowing easy access to different sections in The Crimson.

This feature is implemented on both the New York Times and the Wall Street Journal websites - take a look to get some inspiration!

Here, you'll want to be careful with your CSS rules - make sure you correctly identify the `div` surrounding the navigation bar in the right HTML file. Take a look at `index.html` and `_base.html` to find what you need. Maybe you'll also need to write some Javascript to detect when you've scrolled far enough down the page.

# Task 8: No task too small
It is up to you what you'd like to do for this task. There are plenty of technical bugs, design flaws, features waiting to be implemented - this is your chance to right what you think is wrong. No task is too small!

Here is some inspiration:

- If you scroll to the bottom of the home page, the section headers (sections; more; resources) are too far to the left.
- In the Flyby section on the home page, the titles of the articles are a bit hard to read if the background is light. Maybe add a `div` that adds a shade over the images?
- There's a lot of potential work you can do in order to improve response and load times on the webpage - be very careful though. This is a rabbit hole, and is sometimes very tricky to improve.
- Whatever you want! As long as you record the process you went through to fix the issue, you'll be fine!
