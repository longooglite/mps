#!/bin/bash
#
# Script med-oaklanddb.sh
# Rebuild the Oakland Medical School database.

set -v
dropdb med-oakland
createdb med-oakland
psql med-oakland < $CAR_HOME/data/mpsCommonSchema.sql
psql med-oakland < $CAR_HOME/data/mpsCVSchema.sql
python $CAR_HOME/commands/cvLoad.py -d med-oakland -s med-oakland
if [ $? -eq 0 ]
then
  echo "cv load successful"
else
  echo "cv load failed" >&2
  exit
fi
psql med-oakland < $CAR_HOME/data/mpsAtramSchema.sql
python $CAR_HOME/commands/atramLoad.py -d med-oakland -s med_oakland
if [ $? -eq 0 ]
then
  echo "atram load successful"
else
  echo "atram load failed" >&2
  exit
fi
python $CAR_HOME/commands/workflowLoad.py -d med-oakland -s med-oakland
if [ $? -eq 0 ]
then
  echo "workflow load successful"
else
  echo "workflow load failed" >&2
  exit
fi

psql med-oakland < $CAR_HOME/data/atramData/sites/med_oakland/username_department.sql
psql med-oakland < $CAR_HOME/data/atramData/sites/med_oakland/internal_reviewers.sql
