#!/bin/bash
#
# Script startmps2.sh
# Execute CAR code on the staging server, Alternate Environment 2.
# Runs on the staging server.
#
# This script assumes:
#   - you are connected to the OnlineTech network,
#	- you have ssh'd to the dev server as mpsadmin
#
# This script:
#   - starts the MPS Platform programs in Alternate Environment 2

set -v
ps aux | grep MPS
python /home/mpsadmin/alt2/car/commands/skynyrd.py --dst /usr/local/mps1
python /home/mpsadmin/alt2/car/MPSAuthSvc.py -e staging --file config/staging/MPSAuthSvc/alt2_config.json &
python /home/mpsadmin/alt2/car/MPSAdmin.py -e staging --file config/staging/MPSAdmin/alt2_config.json &
python /home/mpsadmin/alt2/car/MPSCV.py -e staging --file config/staging/MPSCV/alt2_config.json &
python /home/mpsadmin/alt2/car/MPSCV.py -e staging --file config/staging/MPSCV/alt2_config_a.json &
python /home/mpsadmin/alt2/car/MPSAppt.py -e staging --file config/staging/MPSAppt/alt2_config.json &
python /home/mpsadmin/alt2/car/MPSAppt.py -e staging --file config/staging/MPSAppt/alt2_config_a.json &
python /home/mpsadmin/alt2/car/MPSLogin.py -e staging --file config/staging/MPSLogin/alt2_config.json &
ps aux | grep MPS
