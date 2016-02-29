# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

'''

skynyrd.py

Copies 'skin' files from the source code tree to the web server directory
and prepares them for use in the MPS applications.

Usage:

$ python skynyrd.py -i /path/to/skin/source/tree -o /path/to/web/server/directory

The /path/to/skin/source/tree defaults to the 'skin' folder in the car source tree,
so the -i argument does not normally need to be specified. The /path/to/web/server/directory
defaults to /usr/local/mps, so the -o argument does not normally need to be specified, either.

When specified, arguments must be given as absolute paths (begin with '/').
Relative paths are not supported.
'''

import datetime
import distutils.dir_util
import distutils.file_util
import optparse
import os
import os.path


class Skynyrd(object):

	#	Initialization

	def __init__(self, options=None, args=None):
		rootFolderPath = os.path.abspath(__file__).split("car")[0] + "car/"
		print rootFolderPath
		self.srcPath = os.path.join(rootFolderPath, "skin")
		self.dstPath = "/usr/local/mps"
		self.fileList = []
		self.folderList = []
		self.defaultSkinSrcFilePath = None
		self.defaultSkinDstFilePath = None
		self.includeConsoleLog = True

		if options:
			if options.srcPath: self.srcPath = options.srcPath
			if options.dstPath: self.dstPath = options.dstPath
		
		self.logSetup()


	#	Shutdown

	def shutdown(self):
		pass


	#	Execution

	def process(self):
		try:
			self.logProcessStart()

			self.analyzeSourceFolder()
			self.removeDestinationFolder()
			self.createDestinationFolder()
			self.copyIndividualFiles()
			self.copyDefaultSkin()
			self.copyCustomSkins()

			self.logProcessEnd()
		finally:
			pass

	def analyzeSourceFolder(self):
		if self.includeConsoleLog:
			self.logMessage("Analyzing source skin tree '%s'" % self.srcPath)

		#   Enumerate the files and folders in the source directory.
		#   Separate folders from files, ignore cruft.
		#   Make sure we find a 'default' skin.

		names = os.listdir(self.srcPath)
		for name in names:
			if name == '.DS_Store':
				continue
			filePath = os.path.join(self.srcPath, name)
			if os.path.isfile(filePath):
				self.fileList.append(name)
			else:
				if os.path.isdir(filePath):
					if name == 'default':
						self.defaultSkinSrcFilePath = filePath
					else:
						self.folderList.append(name)

		if not self.defaultSkinSrcFilePath:
			self.logFatalError("FATAL ERROR: 'default' skin not found")

	def removeDestinationFolder(self):
		if self.includeConsoleLog:
			self.logMessage("Removing existing destination skin tree '%s'" % self.dstPath)
		try:
			distutils.dir_util.remove_tree(self.dstPath)
		except Exception, e:
			self.logMessage(e.args)

	def createDestinationFolder(self):
		if self.includeConsoleLog:
			self.logMessage("Creating destination skin tree '%s'" % self.dstPath)
		try:
			distutils.dir_util.mkpath(self.dstPath)
		except Exception, e:
			self.logMessage(e.args)

	def copyIndividualFiles(self):
		if self.fileList:
			if self.includeConsoleLog:
				self.logMessage("Copying individual files to destination skin tree '%s'" % self.dstPath)
			try:
				for name in self.fileList:
					self.logMessage("  " + name)
					srcPath = os.path.join(self.srcPath, name)
					distutils.file_util.copy_file(srcPath, self.dstPath)
			except Exception, e:
				self.logFatalError(e.args)

	def copyDefaultSkin(self):
		if self.includeConsoleLog:
			self.logMessage("Copying 'default' skin to destination skin tree '%s'" % self.dstPath)

		self.defaultSkinDstFilePath = os.path.join(self.dstPath, 'default')
		try:
			distutils.dir_util.mkpath(self.defaultSkinDstFilePath)
			distutils.dir_util.copy_tree(self.defaultSkinSrcFilePath, self.defaultSkinDstFilePath)
		except Exception, e:
			self.logFatalError(e.args)

	def copyCustomSkins(self):
		if self.folderList:
			if self.includeConsoleLog:
				self.logMessage("Copying custom skins to destination skin tree '%s'" % self.dstPath)
			try:
				for name in self.folderList:
					self.logMessage("  " + name)

					#   Copy the custom skin.
					customSrcFilePath = os.path.join(self.srcPath, name)
					customDstFilePath = os.path.join(self.dstPath, name)
					try:
						distutils.dir_util.mkpath(customDstFilePath)
						distutils.dir_util.copy_tree(customSrcFilePath, customDstFilePath)
					except Exception, e:
						self.logFatalError(e.args)

					#   Fill in missing elements of the custom skin with
					#   symbolic links to their counterparts in the default skin.
					defaultTuples = os.walk(self.defaultSkinDstFilePath)
					for defaultTuple in defaultTuples:
						thisSrcPath = defaultTuple[0]
						thisSrcFolders = defaultTuple[1]
						thisSrcFilenames = defaultTuple[2]

						thisDstPath = thisSrcPath.replace(self.defaultSkinDstFilePath, customDstFilePath)

						for folderName in thisSrcFolders:
							thisSrcNamedPath = os.path.join(thisSrcPath, folderName)
							thisDstNamedPath = os.path.join(thisDstPath, folderName)
							if not os.path.exists(thisDstNamedPath):
								os.symlink(thisSrcNamedPath, thisDstNamedPath)

						for fileName in thisSrcFilenames:
							thisSrcNamedPath = os.path.join(thisSrcPath, fileName)
							thisDstNamedPath = os.path.join(thisDstPath, fileName)
							if not os.path.exists(thisDstNamedPath):
								os.symlink(thisSrcNamedPath, thisDstNamedPath)
			except Exception, e:
				self.logFatalError(e.args)


	#	Logging

	def logSetup(self):
		if self.includeConsoleLog:
			print "%s Skynyrd processor created" % (self.getLogTimestamp())
			print "%s - Source: %s" % (self.getLogTimestamp(), self.srcPath)
			print "%s - Destination: %s" % (self.getLogTimestamp(), self.dstPath)

	def logProcessStart(self):
		if self.includeConsoleLog:
			self.processStart = self.getLogTimestamp()
			print "%s Skynyrd process started" % (self.processStart)

	def logProcessEnd(self):
		if self.includeConsoleLog:
			self.processEnd = self.getLogTimestamp()
			self.logMessage("")
			print "%s Skynyrd process completed" % (self.processEnd)
			print "%s Skynyrd elapsed time: %s" % (self.processEnd, str(self.processEnd - self.processStart))
	
	def logMessage(self, _message):
		if self.includeConsoleLog:
			if _message:
				print "%s - %s" % (self.getLogTimestamp(), _message)
			else:
				print "%s" % (self.getLogTimestamp(),)
	
	def getLogTimestamp(self):
		return datetime.datetime.now()

	def logFatalError(self, _message):
		if self.includeConsoleLog:
			self.logMessage(_message)
		else:
			print(_message)
		exit()


class Skynyrdface:
	def __init__(self):
		pass

	def get_parser(self):
		descr = '''Copies 'skin' files from the source code tree to the web server directory and prepares them for use in the MPS applications.'''
		parser = optparse.OptionParser(description=descr)
		parser.add_option('-i', '--src', dest='srcPath', default='', help='path to source skin folder')
		parser.add_option('-t', '--dst', dest='dstPath', default='', help='path to destination skin folder')
		return parser

	def run(self, options, args):
		try:
			skynyrd = Skynyrd(options, args)
			skynyrd.process()
		except Exception, e:
			for each in e.args:
				print each
		finally:
			if skynyrd:
				skynyrd.shutdown()


if __name__ == '__main__':
	skynyrdInterface = Skynyrdface()
	parser = skynyrdInterface.get_parser()
	(options, args) = parser.parse_args()
	skynyrdInterface.run(options, args)
