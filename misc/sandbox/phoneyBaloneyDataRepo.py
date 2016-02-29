import datetime
import os
filepath = '/tmp/bolognaRepo.txt'


def writeToFile(value):
	f = open(filepath, "a")
	f.write("%s-%s\r" % (str(datetime.datetime.now()),value))
	f.flush()
	f.close()
