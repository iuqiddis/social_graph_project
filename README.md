The goal of this project was to get familar with web scraping, data cleaning, and eventually making a graph network of social connections.

[New York Social Diary](https://web.archive.org/web/20150913224145/http://www.newyorksocialdiary.com/) is a kind-of  voyeuristic view into New York's socially well-to-do. The data forms a natural social graph for New York's social elite, and such is an interesting dataset to play with.  An example is the this page of a [run-of-the-mill holiday party](https://web.archive.org/web/20150913224145/http://www.newyorksocialdiary.com/party-pictures/2014/holiday-dinners-and-doers). Please note that these links point to the internet archive, as the original website has recently removed most of its archives. Many of the images no longer load, but all the HTML is still there.

For the purpose of this project, the photos have carefully annotated captions labeling, which implicitly form a social graph: there is a connection between two individuals if they appear in a picture together.

For this project, I'll assemble the social graph from photo captions for parties dated December 1, 2014 (arbitrary cut-off for filtering), and before.  Using this graph, I'll make guesses at the most popular socialites, the most influential people, and the most tightly coupled pairs.

I will attack the project in three phases:
1. Get a list of all the photo pages to be analyzed.
2. Parse all of the captions on a sample page.
3. Parse all of the captions on all pages, and assemble the graph.

**Note:** This was an old project I worked on, and if I was to re-do it from scratch, my approach would be slightly different and cleaner (code wise) when it came to the names extraction portion (phase 2).
