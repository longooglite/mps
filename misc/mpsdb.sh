#!/bin/bash
#
# Script mpsdb.sh
# Rebuild the MPS Site database.

set -v
dropdb mpsdev
createdb mpsdev
psql mpsdev < $CAR_HOME/data/mpsCommonSchema.sql
psql mpsdev < $CAR_HOME/data/mpsCVSchema.sql
python $CAR_HOME/commands/cvLoad.py
psql mpsdev < $CAR_HOME/data/mpsAtramSchema.sql
python $CAR_HOME/commands/atramLoad.py
python $CAR_HOME/commands/workflowLoad.py
psql mpsdev < $CAR_HOME/misc/atramdummy.sql
