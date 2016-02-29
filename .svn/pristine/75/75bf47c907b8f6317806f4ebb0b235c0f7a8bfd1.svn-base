#!/bin/bash
#
# Script installData.sh
# Install CAR data folder only on the Production 1 server.
# Runs on the Production 1 server.
#
# This script assumes:
#   - you are connected to the OnlineTech network,
#	- you have ssh'd to the Production 1 server as mpsadmin
#
# This script:
#   - removes old data folder,
#   - untars the new data folder (assumed to be in /home/mpsadmin/transfer) to the correct location

set -v
cd ~/
pwd
rm -vr data
cp transfer/data.tar ./
tar -xvf data.tar
rm data.tar
ls -al
cp -vr data car
ls -al car/data
