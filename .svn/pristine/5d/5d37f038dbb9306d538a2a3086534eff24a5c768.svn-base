#!/bin/bash
#
# Script testdb.sh
# Rebuild the MPS Test database.

set -v
dropdb testdev
createdb testdev
psql testdev < $CAR_HOME/data/mpsCommonSchema.sql
psql testdev < $CAR_HOME/data/mpsCVSchema.sql
python $CAR_HOME/commands/cvLoad.py -d testdev -s test
