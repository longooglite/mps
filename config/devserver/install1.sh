#!/bin/bash
#
# Script install1.sh
# Install CAR code on the development server, Alternate Environment 1.
# Runs on the development server.
#
# This script assumes:
#   - you are connected to the OnlineTech network,
#	- you have ssh'd to the dev server as mpsadmin
#
# This script:
#   - removes old code,
#   - untars the new code (assumed to be in /home/mpsadmin/transfer) to the correct location

set -v
cd ~/alt1
pwd
rm -vr car
cp ~/transfer/car.tar ./
tar -xvf car.tar
rm car.tar
ls -al
