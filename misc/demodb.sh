#!/bin/bash
#
# Script demodb.sh
# Rebuild the Demo database.

dropdb demo
createdb demo
psql demo < $CAR_HOME/data/mpsCommonSchema.sql
psql demo < $CAR_HOME/data/mpsCVSchema.sql
python $CAR_HOME/commands/cvLoad.py -d demo -s dev
if [ $? -eq 0 ]
then
  echo "cv load successful"
else
  echo "cv load failed" >&2
  exit
fi
psql demo < $CAR_HOME/data/mpsAtramSchema.sql
python $CAR_HOME/commands/atramLoad.py -d demo -s demo
if [ $? -eq 0 ]
then
  echo "atram load successful"
else
  echo "atram load failed" >&2
  exit
fi
python $CAR_HOME/commands/workflowLoad.py -d demo -s umms
if [ $? -eq 0 ]
then
  echo "workflow load successful"
else
  echo "workflow load failed" >&2
  exit
fi
psql demo < $CAR_HOME/misc/atramdummy2.sql
python $CAR_HOME/commands/atramRosterLoad.py -d demo -s demo
if [ $? -eq 0 ]
then
  echo "roster load successful"
else
  echo "roster load failed" >&2
  exit
fi
