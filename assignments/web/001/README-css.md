### CSS

Cascading Style Sheets! We're not sure why we're so excited about that, but oh well. Basically, CSS is a brilliant invention that helps (along with JS) web developers separate some of the functionality of what they do. This means that instead of having to do layout AND style all in one massive HTML document, they can put the style or the way that elements look into a separate file. These _.css_ files contain instructions for the browser on how big, what color, what fonts, and much more. 

This assignment assumes that you have access to the _assignment.html_ file from the corresponding HTML assignment. If you don't, then don't worry, but a lot of the references we make to "and see how your change is reflected here" won't make sense to you. 

As with previous things from us, enjoy, try to complete as much as you can, and let us know if you have any questions, comments, or tea.

-----

### Assignment Spec

1. Ok, so in the provided _assignment.css_ file, there isn't a whole lot to get you started. All we've included is a comment and your first property. The way that basic CSS properties work is by telling the browser which elements or groups of elements the following property definitions (enclosed in "{}") apply to. So in our example, ```html``` and ```body``` tags will have the provided font family. There are many, _many_ properties and attributes that are allowed in CSS, so to attempt to describe them all here would be insanity. However, we will get you comfortable with some common ones in the next few sections. For now, please just change the font family to something a bit more flavorful (not Times New Roman)!

2. In CSS (what we're about to say is also useful in JavaScript!), groups of elements are selected using selectors. For example, if I wanted to select all elements of the class _myclass_ then I would do so with ```.myclass {}``` The "." at the beginning means that this is a class name. You can read up on selectors on the Interwebs, but some common ones are here. "#" indicates an ID, no symbol indicates an element tag (i.e. "body" and "html"). We also can specify things using relative selectors "element1 element2" which will select all "element2"'s that are inside "element1". Given that knowledge, please write a CSS property that selects all "h1" inside of "div" and sets its font-size to greater than 32px. Oh! We forgot to mention that sizes in CSS are frequently em, px, vw, or vh. You should Google the units to understand what each of those means. 

3. Similar to the above, can you make all paragraph elements that are inside of divs have a font size of 24px?

4. We also would like to adjust the width and height of our displays so that they make sense. We are going to use vh and vw (viewer height and viewer width) to set each of our sections to cover the visible display. Can you think of a selector that selects all of our section divs? (it's a tricky selector involving "[???^=???]", so Google may come in handy). We will then set their height property to 100vh and their width property to 100vw. This should make our display very clean in size. 

5. Please also select a unique background color for each section (use the id selector). 

6. Ok, so you've set display rules, you've used selectors to change fonts, you've made things colorful. Now, what we want to get into, is adding some properties like padding and borders. These two properties allow us to put some space between things and add lines of varying styles around all items, respectively. Just for fun, add ```* { border: 2px blue solid; }``` to your CSS file in order to immediately add a 2px solid blue border to _every_ item in the HTML. This, or variants on this concept, can be extremely useful for debugging when you just can't seem to figure out where an item ends or begins. Now, let's make that a little bit more reasonable by changing the border to be 1px, black, and only have it apply to the picture-frame class, this way we modify those picture frames to actually have frames. We're also going to set padding on those picture frames, to give them some room. Set them to something reasonable, somewhere around 40px for the top and bottom, and 20px for the sides (the properties should look something like "padding-dimension"). 

7. Now, we're going to use those picture frames for something useful - set their height and width to reasonable values such that they would give us reasonable visibility into any image that's within (don't worry too much about what's "reasonable", just try not to have any enormous or tiny pictures). Then, set their overflow to hidden. This makes it such that they behave as windows into the pictures that they contain. This technique lets us standardize picture sizes. There is another technique that lets you always use the center of the picture, but we won't worry about that for now. 

8. Since we've made our images standard sizes, and we've updated the looks of our document quite a bit, you should make sure that you're checking how each of these items gets or doesn't get applied. Something that we won't have you implement, but that you should know how to use is the ```!important``` which can be added to the end of any CSS property to make it override other versions of that property. If that seems kinda scary and weirdly powerful to you, that's good, because it is indeed scary and weirdly powerful. In fact, we advise not using it unless you have a strong justification. 

9. You can do all sorts of cool and crazy things with CSS, and we've barely scratched the surface. However, if you'd like to see some other cool things that might be good to learn about, feel free to Google WebKit animations, CSS glitch effects, media queries (intensive on the browser!), and cool css tricks (there are tons). 

10. Otherwise, enjoy, and submit!