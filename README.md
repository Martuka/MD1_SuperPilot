# Superpilot
### By Marta Revulta
###### Code by Laurent Weingart

Simple specific RSS article analyzer written in python. This program reads RSS feeds and looks for the presence of key words in the articles.

##### Dependencies:
- FeedParser: pip install feedparser

#### How to use this program.
This program needs two files to function.
- One file containing one RSS feed url per line named `feeds.txt`
- One file containing one key word per line named `keywords.txt`

These two files have to be placed in the same folder as `guardian_rss.py`

Currently this program only works with RSS feeds from The Guardian.
