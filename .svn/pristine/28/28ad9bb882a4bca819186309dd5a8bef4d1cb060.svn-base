#!/bin/bash
#
# Script startmps1.sh
# Execute CAR code on the staging server, Alternate Environment 1.
# Runs on the staging server.
#
# This script assumes:
#   - you are connected to the OnlineTech network,
#	- you have ssh'd to the dev server as mpsadmin
#
# This script:
#   - starts the MPS Platform programs in Alternate Environment 1

set -v
ps aux | grep MPS
python /home/mpsadmin/alt1/car/commands/skynyrd.py --dst /usr/local/mps1
python /home/mpsadmin/alt1/car/MPSAuthSvc.py -e staging --file config/staging/MPSAuthSvc/alt1_config.json &
python /home/mpsadmin/alt1/car/MPSAdmin.py -e staging --file config/staging/MPSAdmin/alt1_config.json &
python /home/mpsadmin/alt1/car/MPSCV.py -e staging --file config/staging/MPSCV/alt1_config.json &
python /home/mpsadmin/alt1/car/MPSCV.py -e staging --file config/staging/MPSCV/alt1_config_a.json &
python /home/mpsadmin/alt1/car/MPSAppt.py -e staging --file config/staging/MPSAppt/alt1_config.json &
python /home/mpsadmin/alt1/car/MPSAppt.py -e staging --file config/staging/MPSAppt/alt1_config_a.json &
python /home/mpsadmin/alt1/car/MPSLogin.py -e staging --file config/staging/MPSLogin/alt1_config.json &
ps aux | grep MPS
