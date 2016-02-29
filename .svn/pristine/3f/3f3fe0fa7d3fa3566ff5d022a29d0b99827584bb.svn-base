#!/bin/bash
#
# Script startmps.sh
# Execute CAR code on the development server, Primary Environment.
# Runs on the development server.
#
# This script assumes:
#   - you are connected to the OnlineTech network,
#	- you have ssh'd to the dev server as mpsadmin
#
# This script:
#   - starts the MPS Platform programs in the Primary Environment

set -v
ps aux | grep MPS
python /home/mpsadmin/car/commands/skynyrd.py --dst /usr/local/mps
python /home/mpsadmin/car/MPSAuthSvc.py -e devserver --file config/devserver/MPSAuthSvc/config.json &
python /home/mpsadmin/car/MPSAdmin.py -e devserver --file config/devserver/MPSAdmin/config.json &
python /home/mpsadmin/car/MPSCV.py -e devserver --file config/devserver/MPSCV/config.json &
python /home/mpsadmin/car/MPSCV.py -e devserver --file config/devserver/MPSCV/config_a.json &
python /home/mpsadmin/car/MPSAppt.py -e devserver --file config/devserver/MPSAppt/config.json &
python /home/mpsadmin/car/MPSAppt.py -e devserver --file config/devserver/MPSAppt/config_a.json &
python /home/mpsadmin/car/MPSLogin.py -e devserver --file config/devserver/MPSLogin/config.json &
ps aux | grep MPS
