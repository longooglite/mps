#!/bin/bash
#
# Script prepRelease.sh
# Prep CAR code for transport to dev and production servers.
# Runs on your local machine.
#
# This script assumes:
#   - your $CAR_HOME environment variable points to your up-to-date code on your local machine
#
# This script:
#   - removes cruft we don't need on the server,
#   - removes any existing folder named 'car' from your desktop,
#   - removes any existing file named 'car.tar' from your desktop,
#   - copies your $CAR_HOME folder to ~/Desktop/car,
#   - makes a tarball in ~/Desktop/car.tar
#
#   This script DOES NOT:
#   - increment the version number. If you want to do that, run incrementVersion.py beforehand.

set -v
find $CAR_HOME -name "*.pyc" -exec rm -rvf {} \;
find $CAR_HOME -name ".DS_Store" -exec rm -rvf {} \;
python $CAR_HOME/config/setBuildDate.py
rm -vr ~/Desktop/car
rm -v  ~/Desktop/car.tar
cp -r $CAR_HOME ~/Desktop
cd ~/Desktop
rm -vr car/.idea
tar -cvf car.tar car
