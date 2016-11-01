#!/usr/bin/python
# -*- coding: utf-8 -*-

# Superpilot
# Basic rss feed analyser for The Guardian RSS feed
# This program needs is a rewritten version in python2 of the original version

###############################################################################
## Imports

import feedparser
import requests
import datetime
import time
import sys
import re as regex
from lxml import html
from collections import Counter
from collections import OrderedDict
from operator import itemgetter

# Adafruit library realted imports
import atexit
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor, Adafruit_StepperMotor


###############################################################################
## Global Variables

# Interval between two check in seconds
# interval_time = 60

DEBUG = True
WRITE_LOGS = True
article_counter = 0
global_match_occurrences = 0

rss_urls_list = "feeds.txt"
key_words_list = "keywords.txt"

# This variable is the name of the class attribute of the <div> containg the
# article text on the web page.
# Only valid for The Guardian, obviously
article_class_name = "content__article-body"

log_file = "results.txt"
db = "articles.db"

###############################################################################
## Functions

# Define if an article title is in the database
def post_is_in_db(title):
	encoded_title = title.encode('utf8')
	if encoded_title in open(db, 'r').read():
		return True
	return False

# Print usage of this program.
def print_usage():
	print "usage: new_gurdian.py <interval_time>"
	print "interval_time = time in seconds between two checks for new RSS feeds."

# Parse the feeds urls file and put each element in a list
def list_feeds_urls(feeds_file):
	feeds_list = [line.strip() for line in open(feeds_file, 'r')]
	return feeds_list

# Parse the tags file and put each elements in a list
def get_key_words(keywords_file):
	return set(list_feeds_urls(keywords_file))

# Put content in the file filename and writes the file in the file system
def write_file(filename, content):
	with open(filename, "w") as file_to_write:
		file_to_write.write(content)
		file_to_write.close()

# Create a set of unique words from the text
def create_word_list_from_text(text):
	foo = regex.sub('[^a-z\ \']+', " ", text.lower())
	return list(foo.split())

# Extract the text from an url and the class name of a specific div.
def get_article_from_rss_url(url, div_class_name):
	response = requests.get(url)
	tree = html.fromstring(response.content)
	div = tree.find_class(div_class_name)
	if len(div) != 0:
		return div[0].text_content()
	else:
		return ""

# Transform a datetime.datetime in its number of seconds from epoch
def time_in_seconds_from_date(dt):
	epoch = datetime.datetime.fromtimestamp(0)
	return (dt - epoch).total_seconds()

# Print in stdout and/or in a log file
def my_print(string):
	if DEBUG:
		print string
	if WRITE_LOGS:
		logs.write(string + "\n")

# Recommended for auto-disabling motors on shutdown!
def turnOffMotors():
	mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
	mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
	mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
	mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)

# Make the two motors turn simultaniously
def rotate_motors(motor1, motor2):
#	for i in range(0, 200):
#		motor1.oneStep(Adafruit_MotorHAT.FORWARD,  Adafruit_MotorHAT.SINGLE)
#		motor2.oneStep(Adafruit_MotorHAT.BACKWARD, Adafruit_MotorHAT.SINGLE)
#	for i in range(0, 200):
#		motor1.oneStep(Adafruit_MotorHAT.FORWARD,  Adafruit_MotorHAT.DOUBLE)
#		motor2.oneStep(Adafruit_MotorHAT.BACKWARD, Adafruit_MotorHAT.DOUBLE)
#	for i in range(0, 200):
#		motor1.oneStep(Adafruit_MotorHAT.FORWARD,  Adafruit_MotorHAT.INTERLEAVE)
#		motor2.oneStep(Adafruit_MotorHAT.BACKWARD, Adafruit_MotorHAT.INTERLEAVE)
	for i in range(0, 200):
		motor1.oneStep(Adafruit_MotorHAT.FORWARD,  Adafruit_MotorHAT.MICROSTEP)
		motor2.oneStep(Adafruit_MotorHAT.BACKWARD, Adafruit_MotorHAT.MICROSTEP)
	time.sleep(1)

def close_logfile():
	logs.close()

# Read all articles from RSS feeds and put their titles in the database
def refresh_db_with_recent_articles():
	print "Refreshing database..."
	hit_list = list_feeds_urls(rss_urls_list)
	f = open(db, 'a')
	for rss_url in hit_list:
		feeds = feedparser.parse(rss_url)
		entries = feeds.entries
		for entry in entries:
			if not post_is_in_db(entry.title):
				f.write(entry.title.encode('utf8') + "\n")
	f.close

###############################################################################
## Main
if __name__ == '__main__':

	interval_time = 120 # check_args()

	# create a default object, no changes to I2C address or frequency
	mh = Adafruit_MotorHAT()

	atexit.register(turnOffMotors)
	atexit.register(close_logfile)

	motor1 = mh.getStepper(200, 1)  	# 200 steps/rev, motor port #1
	motor1.setSpeed(60)  				# RPM
	motor2 = mh.getStepper(200, 2)
	motor2.setSpeed(60)

	refresh_db_with_recent_articles()

	logs = open(log_file, "w")

	while(True):
		now = datetime.datetime.now()

		posts_to_skip = []

		hit_list = list_feeds_urls(rss_urls_list)
		key_words =	get_key_words(key_words_list)
		my_print("\n")
		my_print("====================================================================")
		my_print("=========================                  =========================")
		my_print("========================= RSS The Guardian =========================")
		my_print("\n")
		my_print("Key words = \n")
		my_print(" ".join(key_words))

		matching_words = list()
		for rss_url in hit_list:
			my_print("\n\n************* ************* ************* *************\n")
			my_print("RSS url: {}".format(rss_url))
			feeds = feedparser.parse(rss_url)
			entries = feeds.entries

			for entry in entries:
				if post_is_in_db(entry.title):
					posts_to_skip.append(entry.title)
				else:
					f = open(db, 'a')
					f.write(entry.title.encode('utf8') + "\n")
					f.close
					my_print("\n************* ************* ************* *************\n\n")
					article_list = list()
					web_page_url = entry.link
					article = get_article_from_rss_url(web_page_url, article_class_name)
					wordlist = create_word_list_from_text(article)
					my_print("\nArticle:  '{}'\n\n".format(entry.title.encode('utf8')))
					my_print("Word list:\n")
					my_print(", ".join(wordlist))

					for word in wordlist:
						if word in key_words:
							rotate_motors(motor1, motor2)
							article_list.append(word)

					matching_words.extend(article_list)
					match_occurrences = len(article_list)
					my_print("\n\nThere were {} words from the key words list in this article\n".format(match_occurrences))
					my_print("Those words were:\n")
					my_print(", ".join(article_list))
					my_print("\n")
					global_match_occurrences += match_occurrences


		result = Counter(matching_words)
		my_print("\n\n========================= Final result =========================\n")
		my_print("In total, there were {} word matches.\n".format(global_match_occurrences))
		for k, v in sorted(result.items(), key=itemgetter(1), reverse=True):
			my_print("{}: {}\n".format(k, v))

		my_print("\n\nArticles not treated as they were already in the database:\n")
		for title in posts_to_skip:
			my_print(title.encode('utf8'))

		after = datetime.datetime.now()
		first = time_in_seconds_from_date(now)
		second = time_in_seconds_from_date(after)
		diff = int(round(second - first)) + 1
		sleep_time = interval_time - diff
		if sleep_time >= 0:
			time.sleep(sleep_time)
