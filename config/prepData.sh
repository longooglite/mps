#!/bin/bash
#
# Script prepData.sh
# Prep CAR data folder only for transport to dev and production servers.
# Runs on your local machine.
#
# This script assumes:
#   - your $CAR_HOME environment variable points to your up-to-date code on your local machine
#
# This script:
#   - removes cruft we don't need on the server,
#   - removes any existing folder named 'data' from your desktop,
#   - removes any existing file named 'data.tar' from your desktop,
#   - copies your $CAR_HOME/data folder to ~/Desktop/data,
#   - makes a tarball in ~/Desktop/data.tar
#
#   This script DOES NOT:
#   - increment the version number. If you want to do that, run incrementVersion.py beforehand.

set -v
find $CAR_HOME/data -name "*.pyc" -exec rm -rvf {} \;
find $CAR_HOME/data -name ".DS_Store" -exec rm -rvf {} \;
rm -vr ~/Desktop/data
rm -v  ~/Desktop/data.tar
cp -r $CAR_HOME/data ~/Desktop
cd ~/Desktop
tar -cvf data.tar data
