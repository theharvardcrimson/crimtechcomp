### HTML

HyperText Markup Language! It's one of those things that you've almost certainly heard about. You probably understand a lot about how it works. It's the code that computer scientists write in in order to tell our web browsers how to arrange, color, and style everything that a user will see when they go on our website. Admittedly, nowadays we separate the styling into CSS or Cascading Style Sheets, and we make everything dynamic with JavaScript, but you can do a lot with pure HTML!

This assignment is much shorter than the Python assignment, but it should give you a solid foundation for your HTML knowledge. If it helps, just think of HTML as the way that we, as coders, lay out webpages for our beloved users. 

Note: we love freedom and all that, but if we ask for a certain id or something, then we mean it, simply because that's how our autograder works...sorry to cramp your style.

-----

### Assignment Spec

1. Ok, so tbh, our provided assignment file is kinda not that large. We haven't provided nearly as many function defs or their equivalents as in the Python assignment. We have, however, started you off with the most basic thing you need, which is the declaration that this is in fact an html document. We've additionally given you some basic divs and html elements that are common, like body and head. HTML works entirely on a container-style structure. Everything has a parent or a child/ren. For example, in our skeleton code, the ```<html>``` element has two children, ```<head>```, which is where information about the page goes, and ```<body>```, which is where a lot of your content goes. There's no actionable part to this, we just want you to start to know what's going on with HTML.

2. Now it's time for you to start writing some things into our HTML doc. We're somewhat sorry, but a lot of what we ask in the next few sections will require you to do some Googling. You may shout "but YOU'RE supposed to TEACH us." And you're 100% correct. But also if you combine all that we have ever seen in our lives about HTML, you would only fill a small book (if we're being generous). So we'll direct you to Google for some specifics, and we'll reference some things that you would have no idea about, and we don't expect you to know about a priori. With that being said, please set the language of this HTML page to English in the ```<DOCTYPE! html>```tag.

3. Simple enough, right? Now we also want to set some meta data about our page. Please set the page language to english, add an author, note down some keywords, and write a brief description. Also, give your page a title!

4. Ok, so we've set up some basic meta data, now let's start making the content of this page. A good page usually has all sorts of things on it, but we're trying to teach you basics, not show you how to make the next Lyft homepage (it's really pretty, we think). Our webpage after this will look probably quite ugly, but you'll understand a lot about how HTML works. For example, please add a ```<div></div>``` to the body of this document. Let's give this div an id attribute (Google!), set this div's id to "section-1". Then create 2 more divs, with id's "section-2" and "section-3". Id's are really useful for...identifying things. You should make sure to give elements unique ids if you decide to give them an ID (otherwise, isn't it confusing?). 

5. Let's add some content to our sections. In section 1 let's add a title and a subtitle for our page. To do that, we'll add an ```h1``` or header 1 tag (that'll be your title), and a ```p``` or paragraph tag (there's your subtitle)! Feel free to make them whatever you want.

6. In section 2, please add two paragraphs of text. Thus, there should be two ```<p>``` tags. Don't forget to close the tags. Feel free to throw whatever content you'd like to these paragraphs, but give them id's -> "paragraph-1" and "paragraph-2".

7. We're going to talk a little bit about styling that text. In paragraph 1, please make some of the text emphasized by using the ```<strong>``` tags. In paragraph 2, please link some of the text to the Wikipedia page of your choice using the ```<a>``` tag. 

8. Ok cool, so you have a title, some text. Now we want to add some pictures and cool stuff to the third section. Add an image that links to one of the images from the Wikipedia page of your choice from the previous section. (You shouldn't download the image, just set the "src" attribute of the image tag). Now do it again. You should have two images. One of the images should be given the id "image-1", and the other should have id "image-2".

9. Now, we want to add some cooler, better structuring to our document. It won't look any better, at least not necessarily, but it will set us up to do better with it via the CSS assignment. Please wrap all of the content of each section in a new div. This div will have the id "row-#" where "#" corresponds to the section number that the div resides in. Then, give each of these divs the class "row". You may be wondering, "what the hell is a class? i already have an id, why do i need a class". Classes play a similar role to that in Python; they allow us to give styling attributes to a broad group of things all at once. 

10. Once we've added everything to a row, let's take the content of sections 2 and 3, and put each part into its own column. This means that within our new row divs (divs with the class "row"), we should wrap each individual content piece (a single paragraph or a single image) within a div with the class "col", which stands for column. Each of these columns' ids should be of the form "col-1a" where that would represent a column in section 1, first item of content (your title). That's a lot of words with no examples, so here. Your section 2 should have a div with the class row called "row-2". Inside this row should be a div with class col with id "col-2a" that contains paragraph 1. Also inside this row should be a div with class col with id "col-2b" that contains paragraph 2. If that makes perfect sense, but you still don't like having to do it, then excellent!

11. Finally, we're going to wrap our images each in their own div with a class "picture-frame". Give them ids "picture-frame-1" and "picture-frame-2", respectively. 

12. You may be wondering why on Earth we just gave out a series of somewhat meaningless instructions with all sorts of specificity. We ask that you take a moment to view the webpage you just created in a browser (the URL will start with "file://" instead of your fav "https://") and mess around with the structure of what we did. The CSS assignment will help you add style to this new webpage (so don't throw it out!) and then the JS assignment will add some basic functionality!

13. Submit! Thank you! Hopefully this assignment wasn't nearly as awfully long as the previous one!