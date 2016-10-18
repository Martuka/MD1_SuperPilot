#!/usr/local/bin/python3
# -#- coding: utf-8 -#-

# Superpilot
# Basic rss feeds analyser for The Guardian RSS feed
# This program needs python 3 to run

import feedparser
import requests
import datetime
import re as regex
from lxml import html
from collections import Counter
from collections import OrderedDict
from operator import itemgetter

DEBUG = False
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

# parse the feeds urls file and put each element in a list
def list_feeds_urls(feeds_file):
	feeds_list = [line.strip() for line in open(feeds_file, 'r')]
	return feeds_list

# parse the tags file and put each elements in a list
def get_key_words(keywords_file):
	return set(list_feeds_urls(keywords_file))

# put content in the file filename and writes the file in the file system
def write_file(filename, content):
	with open(filename, "w") as file_to_write:
		file_to_write.write(content)
		file_to_write.close()

# Create a set of unique words from the text
def create_word_list_from_text(text):
	foo = regex.sub('[^a-z\ \']+', " ", text.lower())
	return list(foo.split())

# extract the text from an url and the class name of a specific div.
def get_article_from_rss_url(url, div_class_name):
	response = requests.get(url)
	tree = html.fromstring(response.content)
	div = tree.find_class(div_class_name)
	if len(div) != 0:
		return div[0].text_content()
	else:
		return ""

def my_print(string):
	print(string)
	logs.write(string)
###############################################################################
## Main
if __name__ == '__main__':

	logs = open(log_file, "w")

	hit_list = list_feeds_urls(rss_urls_list)
	key_words =	get_key_words(key_words_list)
	print("\n")
	print("\n")
	print("====================================================================")
	print("=========================                  =========================")
	print("========================= RSS The Guardian =========================")
	logs.write("====================================================================\n")
	logs.write("=========================                  =========================\n")
	logs.write("========================= RSS The Guardian =========================\n")
	# print("\nRSS urls to check = ", hit_list)
	print("\n")
	print("Key words = ", key_words)
	print("\n")
	logs.write("\n")
	logs.write("Key words =\n")
	logs.write(" ".join(key_words))

	matching_words = list()
	for rss_url in hit_list:
		print("************* ************* ************* *************")
		print("RSS url:", rss_url)
		logs.write("\n\n************* ************* ************* *************\n")
		logs.write("RSS url: {}".format(rss_url))
		feeds = feedparser.parse(rss_url)
		entries = feeds.entries

		for entry in entries:
			print("************* ************* ************* *************")
			logs.write("\n************* ************* ************* *************\n\n")
			article_list = list()
			web_page_url = entry.link
			article = get_article_from_rss_url(web_page_url, article_class_name)
			wordlist = create_word_list_from_text(article)
			print("\n")
			print("Word list from article:")
			print(wordlist)
			logs.write("\nArticle:  '{}'\n\n".format(entry.title))
			logs.write("Word list:\n")
			logs.write(", ".join(wordlist))

			for word in wordlist:
				if word in key_words:
					article_list.append(word)

			matching_words.extend(article_list)
			match_occurrences = len(article_list)
			print("\n")
			print("\nThere were {} words from the key words list in this article".format(match_occurrences))
			print("\n")
			print("Those words were:")
			print(article_list)
			print("\n")
			logs.write("\n\nThere were {} words from the key words list in this article\n".format(match_occurrences))
			logs.write("Those words were:\n")
			logs.write(", ".join(article_list))
			logs.write("\n")
			global_match_occurrences += match_occurrences

	print("========================= Final result =========================")
	print("In total, there were {} word matches.".format(global_match_occurrences))
	print("\n")
	result = Counter(matching_words)
	logs.write("\n\n========================= Final result =========================\n")
	logs.write("In total, there were {} word matches.\n".format(global_match_occurrences))
	for k, v in sorted(result.items(), key=itemgetter(1), reverse=True):
		print(k, v)
		logs.write("{}: {}\n".format(k, v))

	logs.close()
