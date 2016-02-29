# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

#!/usr/bin/python

import sys
import getopt
import os
import distutils.dir_util
import shutil
from os.path import expanduser


class Brander:
	def __init__(self,_projectPath,_resourcePath):
		self.projectPath = os.path.join(_projectPath, '')
		self.resourcePath = os.path.join(_resourcePath, '')
		self.brandedPath = os.getenv("HOME") + "/Desktop/Branded/"
		self.martaResourcesPrjPath = "web/src/main/resources/"
		self.messages = []
		if self.pathExists(self.projectPath, "Project Path") == False:
			sys.exit(0)
		if self.pathExists(self.resourcePath, "Resoure Path") == False:
			sys.exit(0)
	
	def pathExists(self,path, pathDescription):
		if os.path.exists(path) == False:
			print "%s %s does not exist." % (pathDescription,path)
			return False
		return True

	def brand(self):
		self.copyProject()
		self.applyResources()
		self.applyCodeModifications()
		self.applyGraphics()
		for each in self.messages:
			print each

	def applyGraphics(self):
		print "Applying Graphics"
		imagePath = '/web/src/main/webapp/img/'
		print "...icon_header.png"
		shutil.copy(self.resourcePath + 'images/icon_header.png',self.brandedPath + imagePath + 'icon_header.png')
		print "...icon.png"
		shutil.copy(self.resourcePath + 'images/icon.png',self.brandedPath + imagePath + 'icon.png')
		print "...ummslogo.gif"
		shutil.copy(self.resourcePath + 'images/ummslogo.gif',self.brandedPath + imagePath + 'ummslogo.gif')
		print "...default_sig.png"
		shutil.copy(self.resourcePath + 'images/default_sig.png',self.brandedPath + imagePath + 'default_sig.png')

	def applyResources(self):
		print "Applying Resources"
		for dirname, dirnames, filenames in os.walk(self.resourcePath):
			if self.getCurrentDirectory(dirname) == 'resources':
				self.copyPropertiesFiles(filenames,dirname)
			elif self.getCurrentDirectory(dirname) == 'emails':
				self.copyEmails(filenames,dirname)

	def copyPropertiesFiles(self,files,dirname):
		print "Moving resources from %s" % (dirname)
		for each in files:
			if each.endswith(".properties"):
				self.diffResources(dirname + '/' + each,self.brandedPath + self.martaResourcesPrjPath + each)
				print "...%s" % (each)
				shutil.copy(dirname + '/' + each,self.brandedPath + self.martaResourcesPrjPath + each)
	
	def diffResources(self,brandedPropertyFilePath,projectProperyFilePath):
		bpfHandle = open(brandedPropertyFilePath,'r')
		ppfHandle = open(projectProperyFilePath,'r')
		bpfKeys = self.getPropertiesKeys(bpfHandle)
		ppfKeys = self.getPropertiesKeys(ppfHandle)
		for key in ppfKeys.keys():
			if not bpfKeys.has_key(key):
				self.messages.append("missing propery key %s in %s" % (key,brandedPropertyFilePath))
		bpfHandle.close()
		ppfHandle.close()
		
	def getPropertiesKeys(self,file):
		lines = file.readlines()
		returnDict = dict()
		for each in lines:
			if not each.startswith("#") and not each.strip() == '':
				#cheeseball hacks to work around no good options parser for python
				if each.find("=") > 0:
					partsIsParts = each.split("=")
					if len(partsIsParts[0]) < 30 and partsIsParts[0].find("<") == -1:
						returnDict[partsIsParts[0]] = ''
		return returnDict
			
	def copyEmails(self,files,dirname):
		print "Moving resources from %s" % (dirname)
		for each in files:
			if each.endswith(".html"):
				print "%s" % (each)
				shutil.copy(dirname + '/' + each,self.brandedPath + self.martaResourcesPrjPath + 'emails/' + each)

	def getCurrentDirectory(self,path):
		pathParts = os.path.split(path)
		return pathParts[len(pathParts)-1]
	
	def applyCodeModifications(self):
		print "Applying Source Modifications"
		print "...context.xml"
		shutil.copy(self.resourcePath + 'context.xml',self.brandedPath + 'web/src/main/webapp/META-INF/context.xml' )
		print "...UniqnameController.java"
		shutil.copy(self.resourcePath + 'UniqnameController.java', self.brandedPath + 'web/src/main/java/edu/umich/umms/open/controller/json/UniqnameController.java')


	def copyProject(self):
		print "Copying project directory to %s" % (self.brandedPath)
		distutils.dir_util.copy_tree(self.projectPath, self.brandedPath)



########################################################################################
# Eric
#resourcePath = expanduser("~") + "/CAR/trunk/car/MartaLegacy/sites/CMU/Branding/resources"
#projectPath = expanduser("~") + "/MPSMarta/marta/trunk"
# Greg
resourcePath = "/Users/gpoth/MPS/platform/trunk/car/MartaLegacy/sites/CMU/Branding/resources"
projectPath = "/Users/gpoth/Legacy/marta/trunk"

schools = {"CMU":{"projectPath":projectPath,"resourcePath":resourcePath}}

def main(argv):
	school = "CMU"
	projectPath = schools.get(school,{}).get("projectPath","")
	resourcePath = schools.get(school,{}).get("resourcePath","")

	if projectPath <> '' and resourcePath <> '':
		brander = Brander(projectPath,resourcePath)
		brander.brand()

if __name__ == "__main__":
	main(sys.argv[1:])