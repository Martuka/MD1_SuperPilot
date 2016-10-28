#!/bin/bash

# remove old entry
crontab -u pi -l | grep -v 'guardian_rss_motor.py'  | crontab -u pi -
