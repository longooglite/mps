#!/bin/bash
#
# Script startmps.sh
# Execute CAR code on the staging server, Primary Environment.
# Runs on the staging server.
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
python /home/mpsadmin/car/MPSAuthSvc.py -e staging --file config/staging/MPSAuthSvc/config.json &
python /home/mpsadmin/car/MPSAdmin.py -e staging --file config/staging/MPSAdmin/config.json &
python /home/mpsadmin/car/MPSCV.py -e staging --file config/staging/MPSCV/config.json &
python /home/mpsadmin/car/MPSCV.py -e staging --file config/staging/MPSCV/config_a.json &
python /home/mpsadmin/car/MPSAppt.py -e staging --file config/staging/MPSAppt/config.json &
python /home/mpsadmin/car/MPSAppt.py -e staging --file config/staging/MPSAppt/config_a.json &
python /home/mpsadmin/car/MPSLogin.py -e staging --file config/staging/MPSLogin/config.json &
ps aux | grep MPS
