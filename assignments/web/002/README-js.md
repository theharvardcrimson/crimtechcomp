### JavaScript

Yay! Everyone's favorite language. Except for some people, who don't like JavaScript at all! And if those two statements sounded contradictory and you liked it, then you'll LOVE JavaScript, the land where equality is confusing (#America) and who, what, where, and when may be partially all defined. 

We're mostly kidding. JavaScript is actually way easier to understand than the above gibberish, and we're pretty sure you'll start to like some of its power. However, it can be extremely frustrating to debug at times, so bear with us. If you want to run any willy-nilly JavaScript code, then you're welcome to open a browser of your choice, figure out how to pull up developer tools, and then use the JS console to try out JS commands to your heart's content. 

Let's begin.

-----

### Assignment Spec

1. We've given you an assignment.js file that has, like always, almost nothing in it. We've demonstrated how comments work and how you might define a function. Otherwise, we don't have much for you. However, please do replace the body of the function that begins at line 7 with something more reasonable for a function which should return the minimum of x and y, not just always x. 

2. JavaScript is built as a scripting language (shocker), in that when a JS file is executed, it will just run code that isn't wrapped in a function, closure, or some other block. This means that you can actually throw statements in just to have them execute any time the file executes. In fact, let's do that right now. Right below the comment corresponding to this part of the assignment, let's be stereotypical nerds and print "Hello, world!" to the console. The function that does this is ```console.log();```. Don't forget that statements in JS end in semicolons (the source of many an odd bug)!

3. Ok, so we don't usually want to just execute JS willy-nilly, so let's wait until the window (the webpage that we're including this JavaScript in) has actually loaded. You may want to Google, but it might look something like this: ```window.addEventListener("load", ...);```. What should we do with this fabulous function, you might ask, and we would switch languages so that you can't understand us and say "Oh, just put a callback function in there, preferably main." And then you would very reasonably cry and/or hate us for life. Luckily, we're not that mean, and we'll explain. Callback functions are a beautiful aspect of JS that allow functions to call other functions upon completion. For example, let's assume that there's some function _main()_ and we want to execute _main()_ once the window has loaded. If that's the case, then we can do something like this: ```winow.addEventListener("load", main);```. This tells the _window_ object to keep its ears open for an event called "load" that presumably happens. In fact, it's intended to happen once the window has been loaded (with a few caveats ofc), and once that has happened, the function that you so graciously provided will be called. 

4. BUT WAIT YOU NEVER DEFINED MAIN YOU FOOL - you would scream at us in righteous indignation. You're absolutely correct. Under the comment for 4, please define a function main that takes in no arguments and merely prints "I am here" to the console. (Note, #3 should be implemented under the comment for 3). 

5. Ok, so now that we've defined _main()_ and we've added a callback for when the window loads that calls _main()_, let's make _main()_ a little bit beefier (weird way of saying we want it to _do_ stuff). When you're using JS you have access to what we call the DOM - Document Object Model. What this means for us is that we can actually get JS versions of objects and manipulate them. Note: #5 and on will be indented to indicate that they should go within _main()_, don't be given a confuse. When we want to define variables in JS, we're given two constructs: ```let``` and ```var```. The difference can be roughly summarized with the term "scoping". What this means for us is that when we use ```var myvar = 42;```, _myvar_ is available all over the place, to the world, and to your parents (jk probably). When we use ```let mylet = 41;```, we only have access to _mylet_ in the appropriate scopes (so unless your parents live in the function where this occurs, they won't see it). If that doesn't make sense, don't worry about it too much for now, and default to ```let``` if you're unsure (this will cause your variables to behave similar to how they behave in other, more reasonable languages). With all that being said, please use ```let``` to give us access to the JS representation of the HTML body element. It might look something like this: ```let docBody = document.body;```

6. Then, right below, we're going to create a new section to add to our document. Go figure out how to create a new HTML element and set its properties (class and id might be important attributes here). Hint: ```document.createElement()```

7. Now that we've created this new element, let's create a new HTML form (essentially, we've gotten "access to" 3 HTML elements now). Don't forget to give it a unique id.

8. Next, let's create an input and a submit button. The input should have some placeholder text: "Your initials here", and the submit button should say "Submit". 

9. Now, we'll put it all together and make it display to the actual webpage. Using the ```.append()``` method of these objects, add the input and submit to the form. Then, add the form to the new section. Finally, add that new section to the body. 

10. Lastly, use ```setInterval()``` to change the text color of the h1 element on your webpage (essentially the title at the top of the page) between at least 3 colors every second. 

11. Hope this wasn't too terrible! Please submit!