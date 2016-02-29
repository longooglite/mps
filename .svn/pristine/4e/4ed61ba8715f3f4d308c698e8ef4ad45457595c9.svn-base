#!/bin/bash
#
# Script startmps.sh
# Execute CAR code on the Production 1 server.
# Runs on the Production 1 server.
#
# This script assumes:
#   - you are connected to the OnlineTech network,
#	- you have ssh'd to the Production 1 server as mpsadmin
#
# This script:
#   - starts the MPS Platform programs

set -v
ps aux | grep MPS
python /home/mpsadmin/car/commands/skynyrd.py
python /home/mpsadmin/car/MPSAuthSvc.py -e prod1 &
python /home/mpsadmin/car/MPSAdmin.py -e prod1 &
python /home/mpsadmin/car/MPSCV.py -e prod1 &
python /home/mpsadmin/car/MPSCV.py -e prod1 --file config/prod1/MPSCV/config1.json &
python /home/mpsadmin/car/MPSCV.py -e prod1 --file config/prod1/MPSCV/config2.json &
python /home/mpsadmin/car/MPSCV.py -e prod1 --file config/prod1/MPSCV/config3.json &
python /home/mpsadmin/car/MPSLogin.py -e prod1 &
python /home/mpsadmin/car/MPSAppt.py -e prod1 &
python /home/mpsadmin/car/MPSAppt.py -e prod1 --file config/prod1/MPSAppt/config1.json &
python /home/mpsadmin/car/MPSAppt.py -e prod1 --file config/prod1/MPSAppt/config2.json &
python /home/mpsadmin/car/MPSAppt.py -e prod1 --file config/prod1/MPSAppt/config3.json &
ps aux | grep MPS
