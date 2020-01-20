# Intro - HTML/CSS/JS

You've gotten this far! Now we're going to get started on some basic web programming. No, we're not going to learn React Native or how to create the latest and greatest responsive website. What we're going to do is get in a time machine and go back to the 90's, when all you had was barebones HTML and CSS.

### What the heck is HTML?
HTML stands for "hypertext markup language". Essentially, if a website sends information that is deemed to be an HTML document, this HTML document is parsed as if each HTML element was an individual building block of a webpage. So you can sort of think about HTML as a language you can use that has some predefined building blocks you can use to build a webpage. Of course, you can customize these building blocks, which we call "elements" in the HTML world!

Here's a barebones HTML website, which displays "Hello world!" with a title of "This is my webpage!":

```html
<!DOCTYPE HTML>
<html>
  <!-- This is an HTML comment -->
  <!-- This <head> contains data about the document itself -->
  <head>
    <title>This is my webpage!</title>
  </head>
  <!-- This <body> contains data that is displayed on the webpage -->
  <body>
    <p>Hello world!</p>
  </body>
</html>
```

Notice that we've made use of several predefined "tags", such as <html>, <head>, <body>. Each of these tags is opened (<html>) and closed (</html>). This way, our parser knows exactly where our "building blocks" begin and end, and what goes in between or around them.

To try it for yourself, save that HTML into a file like "page.html" and open with your favorite modern web browser.

This is just a (very small) taste of what's to come. Of course, the reality of this is that creating webpages is much more complicated, but our goal is to walk you through it!

### What the heck is CSS?
CSS stands for "cascading style sheets". As you might guess from "style sheets", CSS files typically describe things like the color of backgrounds, the size and font of text, and other, even more complicated things (like basic animations and transitions)!

For example, if I'd like to change all paragraph text elements to be red, I would do:

```css
p {
  color: red;
}
```

At this point, we encourage you to open your favorite modern web browser, and begin playing around with "inspect element". Right click on a line of text on whatever webpage (for example, you could [right click and inspect element on the word "Example" here](https://www.w3schools.com/html/default.asp)). You should see a mini window pop up that has all of this HTML! Cool stuff. In particular, the element you selected should be highlighted. If you inspected "Example" as in the above, you might see something like <h3>Example</h3>. Go ahead and double click until just the text is selected, then type in whatever you'd like (or right click and "Edit Text"), and type in whatever you'd like. Click away or press enter to see your changes!

See that you can do this for whatever element you'd like - you'll probably also see a style section in this mini window, where you can edit the style of certain elements! But wait - we haven't quite talked about styles yet.

HTML elements inherently come with certain attributes. For example, unless it's styled properly, raw text starts out black; links show up blue. We say that these style properties of an element - color, font-size, width, height - are part of the attributes of the element itself. We'll figure out ways to get around these boring styles in the assignment.

### What the heck is JS?
JS is JavaScript, a programming language. It is similar in syntax to the C-style languages. It's commonly used in conjunction with HTML and CSS, because it has the power to create HTML elements and add them to a webpage, and even update attributes of an element. Of course, it can also do the things your favorite programming language can do (evaluation-wise, even though the syntax might be different).

For example, I could do the following in Python:

```python
for i in range(10):
  print("Hello world")
```

But I could do the same in JavaScript:

```javascript
for(var i = 0; i < 10; i++) {
  console.log("Hello world")
}
```

Where we've printed to the console (the thing we in fact opened earlier, when we were inspecting HTML elements). We'll play around with creating elements, changing their styles, and whatnot in the assignment!
