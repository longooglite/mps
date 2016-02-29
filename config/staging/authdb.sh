#!/bin/bash
#
# Script authdb.sh
# Rebuild the MPS Authorization database for the demo site.

set -v
dropdb mpsauth
createdb mpsauth
psql mpsauth < $CAR_HOME/data/mpsCommonSchema.sql
psql mpsauth < $CAR_HOME/data/mpsauthSchema.sql
python $CAR_HOME/commands/authLoad.py -s demo
