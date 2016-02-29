#!/bin/bash
#
# Script dentdb.sh
# Rebuild the UM Dental School database.

set -v
dropdb dent-umich
createdb dent-umich
psql dent-umich < $CAR_HOME/data/mpsCommonSchema.sql
psql dent-umich < $CAR_HOME/data/mpsCVSchema.sql
python $CAR_HOME/commands/cvLoad.py -d dent-umich -s dent-umich
