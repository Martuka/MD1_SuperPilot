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

###############################################################################
## Functions

# Print usage of this program.
def print_usage():
	print "usage: guardian_rss.py <interval_time>"
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

#
def my_print(string):
	if DEBUG:
		print string
	if WRITE_LOGS:
		logs.write(string + "\n")

# Transform a datetime.datetime in its number of seconds from epoch
def time_in_seconds_from_date(dt):
	epoch = datetime.datetime.fromtimestamp(0)
	return (dt - epoch).total_seconds()

# Transform a time.stuct_time object into a datetime.datetime object
def date_from_time_struct(t):
	return datetime.datetime.fromtimestamp(time.mktime(t))

# Create a datetime.datetime from a numbre of seconds from epoch
def date_from_seconds(seconds):
	return datetime.datetime.fromtimestamp(seconds)

# Verify if an article has been published more recently that interval time.
def new_article(entry, now, interval):
	published_parsed = entry.published_parsed
	delta = time_in_seconds_from_date(now) - time_in_seconds_from_date(date_from_time_struct(published_parsed))
	if delta <= interval:
		return True
	return False

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

# Check the command line arguments
def check_args():
	if len(sys.argv) != 2:
		print_usage()
		sys.exit(0)

	try:
		interval_time = int(sys.argv[1])
	except ValueError as ex:
		print '"%s" does not represent a number of seconds: %s' % (sys.argv[1], ex)
		print_usage()
		sys.exit(0)
	print "interval time = ", interval_time
	return interval_time

###############################################################################
## Main
if __name__ == '__main__':

	interval_time = check_args()

	# create a default object, no changes to I2C address or frequency
	mh = Adafruit_MotorHAT()

	atexit.register(turnOffMotors)

	motor1 = mh.getStepper(200, 1)  	# 200 steps/rev, motor port #1
	motor1.setSpeed(60)  				# RPM
	motor2 = mh.getStepper(200, 2)
	motor2.setSpeed(60)

	now = datetime.datetime.now()

	logs = open(log_file, "w")

	hit_list = list_feeds_urls(rss_urls_list)
	key_words =	get_key_words(key_words_list)
	my_print("\n")
	my_print("====================================================================")
	my_print("=========================                  =========================")
	my_print("========================= RSS The Guardian =========================")
	my_print("\ntime is")
	my_print(str(now))
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
			if new_article(entry, now, interval_time):
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

	logs.close()
