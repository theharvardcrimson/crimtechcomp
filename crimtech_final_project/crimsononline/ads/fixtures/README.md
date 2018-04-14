start.json includes all ad unit tags corresponding to Google DoubleClick for Publishers and the ad zones units for different layouts. The ad zones are referenced by their name in content/views.py.

As of Dec 1, 2017, all ad units in views.py changed to content ad zone, this causes all ad tags to be TheCrimson_AllArticles_..., which disallows differentiation of ad units on different section pages or landing pages or articles pages. Jessica Wang and Nathan Lee
