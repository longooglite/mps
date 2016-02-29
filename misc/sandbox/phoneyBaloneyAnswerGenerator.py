import json
import os

statusDict = { 'taskA':False, 'taskB':False, 'taskC':False }
filepath = '/tmp/bologna.json'

def readFile():
	if not os.path.exists(filepath):
		f = open(filepath, 'w')
		f.write(json.dumps(statusDict))
		f.flush()
		f.close()

	f = open(filepath, 'rU')
	x = json.load(f)
	f.close()
	return x

def writeFile(key, value):
	x = readFile()
	x[key] = value

	f = open(filepath, 'w')
	f.write(json.dumps(x))
	f.flush()
	f.close()

def getStatus(key):
	x = readFile()
	return x.get(key, False)

def toggleValue(key):
	x = readFile()
	writeFile(key, not x[key])

