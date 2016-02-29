#!/bin/bash
pushd ~/Desktop/
svn checkout https://205.145.133.113/svn/platform/trunk/car file:///~/Deskop
rm ~/Desktop/car/MPSCV.py 
rm ~/Desktop/car/MPSTest.py
rm -r ~/Desktop/car/MPSCV
rm -r ~/Desktop/car/MPSLogin/tests
rm -r ~/Desktop/car/MPSCore/tests 
rm -r ~/Desktop/car/MPSAuthSvc/tests 
rm -r ~/Desktop/car/MPSAdmin/tests
rm -r ~/Desktop/car/misc/sandbox 
rm -r ~/Desktop/car/MartaLegacy 
cp ~/Desktop/car/misc/requirements.txt ~/Desktop/car/requirements.txt
cp ~/Desktop/car/misc/nginXInstall.txt ~/Desktop/car/nginXInstall.txt
cp ~/Desktop/car/misc/postgresInstall.txt ~/Desktop/car/postgresInstall.txt
rm -r ~/Desktop/car/misc
rm -r ~/Desktop/car/.svn 
rm -r ~/Desktop/car/data/cvMetaData
rm ~/Desktop/car/commands/cvLoad.py
rm ~/Desktop/car/commands/cvBulkDataFabricator.py
rm ~/Desktop/car/commands/cvRosterLoad.py
rm -r ~/Desktop/car/data/authData/environments/devserver 
rm -r ~/Desktop/car/config/devserver 
rm ~/Desktop/car/commands/bigRooster.py 
rm ~/Desktop/car/commands/copyright.py 
rm -r ~/Desktop/car/config/dev/MPSCV

for dir in ~/Desktop/car/skin/*/
do
	if ! [[ $dir == *"default"* ]]
	then
  		rm -r $dir
	fi
done;

for dir in ~/Desktop/car/data/atramData/sites/*/
do
	if ! ([[ $dir == *"accept-umich"* ]] || [[ $dir == *"umms"* ]])
	then
  		rm -r $dir
	fi
done;


for dir in ~/Desktop/car/data/authData/sites/*/
do
	if ! ([[ $dir == *"accept-umich"* ]] || [[ $dir == *"umms"* ]])
	then
  		rm -r $dir
	fi
done;


for dir in ~/Desktop/car/data/authData/environments/*/
do
	if [[ $dir != *"dev"* ]]
	then
  		rm -r $dir
	fi
done;

for dir in ~/Desktop/car/config/*/
do
	if [[ $dir != *"dev"* ]]
	then
  		rm -r $dir
	fi
done;


