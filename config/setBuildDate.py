# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import datetime
import json
import os


fIn = open(os.path.abspath(__file__).split("car")[0] + "car%sconfig%sversion.json" % (os.sep,os.sep),'rU')
contentDict = json.loads(fIn.read())
fIn.close()
contentDict['releaseBuildDate'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
out = open(os.path.abspath(__file__).split("car")[0] + "car%sconfig%sversion.json" % (os.sep,os.sep),'w')
out.write(json.dumps(contentDict))
out.close()
