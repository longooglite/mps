#!/bin/bash
#
# Script engin-umichdb.sh
# Rebuild the UM Engineering School database.

set -v
dropdb engin-umich
createdb engin-umich
psql engin-umich < $CAR_HOME/data/mpsCommonSchema.sql
psql engin-umich < $CAR_HOME/data/mpsCVSchema.sql
python $CAR_HOME/commands/cvLoad.py -d engin-umich -s engin-umich
if [ $? -eq 0 ]
then
  echo "cv load successful"
else
  echo "cv load failed" >&2
  exit
fi
psql engin-umich < $CAR_HOME/data/mpsAtramSchema.sql
python $CAR_HOME/commands/atramLoad.py -d engin-umich -s engin_umich
if [ $? -eq 0 ]
then
  echo "atram load successful"
else
  echo "atram load failed" >&2
  exit
fi
python $CAR_HOME/commands/workflowLoad.py -d engin-umich -s engin_umich
if [ $? -eq 0 ]
then
  echo "workflow load successful"
else
  echo "workflow load failed" >&2
  exit
fi

psql engin-umich < $CAR_HOME/data/atramData/sites/engin_umich/username_department.sql
