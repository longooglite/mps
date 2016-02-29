#!/bin/bash
#
# Script shibdb.sh
# Rebuild the Shibboleth Testing database.

set -v
dropdb shib
createdb shib
psql shib < $ALT2_CAR_HOME/data/mpsCommonSchema.sql
psql shib < $ALT2_CAR_HOME/data/mpsCVSchema.sql
python $ALT2_CAR_HOME/commands/cvLoad.py -d shib -s dev
if [ $? -eq 0 ]
then
  echo "cv load successful"
else
  echo "cv load failed" >&2
  exit
fi
psql shib < $ALT2_CAR_HOME/data/mpsAtramSchema.sql
python $ALT2_CAR_HOME/commands/atramLoad.py -d shib -s seed
if [ $? -eq 0 ]
then
  echo "atram load successful"
else
  echo "atram load failed" >&2
  exit
fi
python $ALT2_CAR_HOME/commands/workflowLoad.py -d shib -s seed
if [ $? -eq 0 ]
then
  echo "workflow load successful"
else
  echo "workflow load failed" >&2
  exit
fi

psql shib < $ALT2_CAR_HOME/data/atramData/sites/seed/username_department.sql
