#!/bin/bash
#
# Script devdb.sh
# Rebuild the Dev database.

dropdb dev
createdb dev
psql dev < $CAR_HOME/data/mpsCommonSchema.sql
psql dev < $CAR_HOME/data/mpsCVSchema.sql
python $CAR_HOME/commands/cvLoad.py -d dev -s dev
if [ $? -eq 0 ]
then
  echo "cv load successful"
else
  echo "cv load failed" >&2
  exit
fi
psql dev < $CAR_HOME/data/mpsAtramSchema.sql
python $CAR_HOME/commands/atramLoad.py -d dev -s dev
if [ $? -eq 0 ]
then
  echo "atram load successful"
else
  echo "atram load failed" >&2
  exit
fi
python $CAR_HOME/commands/workflowLoad.py -d dev -s dev
if [ $? -eq 0 ]
then
  echo "workflow load successful"
else
  echo "workflow load failed" >&2
  exit
fi
psql dev < $CAR_HOME/misc/atramdummy.sql
