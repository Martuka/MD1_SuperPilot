# SuperPilot
### By Marta Revuelta
###### Code by Laurent Weingart

Simple specific RSS article analyzer written in python. This program reads RSS
feeds and looks for the presence of key words in the articles.

##### Dependencies:
- FeedParser: `python3 -m pip install feedparser`
- requests: `python3 -m pip install requests`
- lxml: `python3 -m pip install lxml`

#### How to use this program.
This program needs two files to run.
- One file containing one RSS feed url per line named `feeds.txt`
- One file containing one key word per line named `keywords.txt`

These two files have to be placed in the same folder as `guardian_rss.py`

Currently this program only works with RSS feeds from
[The Guardian](https://www.theguardian.com/international).

To execute the program:</br>
`python guardian_rss_motor.py <interval>`</br>
where interval is the time in seconds between two checks for new RSS articles.
