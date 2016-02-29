#!/bin/bash
#
# Script pushToDevServererver.sh
# Prep CAR code for transport to the dev server.
# Runs on your local machine.
#
# This script assumes:
#   - you are connected to the OnlineTech network,
#   - your $CAR_HOME environment variable points to your up-to-date code on your local machine
#
# This script:
#   - removes cruft we don't need on the server,
#   - removes any existing folder named 'car' from your desktop,
#   - removes any existing file named 'car.tar' from your desktop,
#   - copies your $CAR_HOME folder to ~/Desktop/car,
#   - makes a tarball in ~/Desktop/car.tar,
#   - sets your local working directory to ~/Desktop (i.e. where car.tar got created),
#   - begins an sftp connection to the dev server

set -v
find $CAR_HOME -name "*.pyc" -exec rm -rvf {} \;
find $CAR_HOME -name ".DS_Store" -exec rm -rvf {} \;
python $CAR_HOME/config/incrementVersion.py
rm -vr ~/Desktop/car
rm -v  ~/Desktop/car.tar
cp -r $CAR_HOME ~/Desktop
cd ~/Desktop
rm -vr car/.idea
tar -cvf car.tar car
sftp mpsadmin@10.64.139.145
