#!/bin/bash
#
# Script accept-umichdb.sh
# Rebuild the U-M Acceptance Testing database.

dropdb accept-umich
createdb accept-umich
psql accept-umich < $ALT1_CAR_HOME/data/mpsCommonSchema.sql
psql accept-umich < $ALT1_CAR_HOME/data/mpsCVSchema.sql
python $ALT1_CAR_HOME/commands/cvLoad.py -d accept-umich -s dev
if [ $? -eq 0 ]
then
  echo "cv load successful"
else
  echo "cv load failed" >&2
  exit
fi
psql accept-umich < $ALT1_CAR_HOME/data/mpsAtramSchema.sql
python $ALT1_CAR_HOME/commands/atramLoad.py -d accept-umich -s umms
if [ $? -eq 0 ]
then
  echo "atram load successful"
else
  echo "atram load failed" >&2
  exit
fi
python $ALT1_CAR_HOME/commands/workflowLoad.py -d accept-umich -s umms
if [ $? -eq 0 ]
then
  echo "workflow load successful"
else
  echo "workflow load failed" >&2
  exit
fi
psql accept-umich < $ALT1_CAR_HOME/data/atramData/sites/accept_umich/username_department.sql
python $ALT1_CAR_HOME/commands/ummsatramRosterLoad.py -d accept-umich -s umms
if [ $? -eq 0 ]
then
  echo "roster load successful"
else
  echo "roster load failed" >&2
  exit
fi
