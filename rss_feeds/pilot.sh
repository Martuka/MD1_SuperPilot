#!/bin/bash

if [[ -z $1 ]]; then
	#statements
	echo '[#] usage: ' $0 '<nb_minutes>'
	exit 0
fi

# remove old entry
crontab -u pi -l | grep -v 'guardian_rss_motor.py'  | crontab -u pi -

# add the new entry
(crontab -u pi -l ; echo "*/$1 * * * * pi /usr/bin/python /home/pi/git/MD1_SuperPilot/rss_feeds/guardian_rss_motor.py $1*60") | crontab -u pi -
