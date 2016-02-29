# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

'''

copyright.py

Applies Copyright notices to all applicable files in a given source code tree.

Usage:

$ python copyright.py -i /path/to/source/tree

The /path/to/source/tree defaults to the car source tree, so the -i argument does not normally need to be specified.
When specified, arguments must be given as absolute paths (begin with '/').
Relative paths are not supported.
'''

import datetime
import optparse
import os
import os.path


class Copyright(object):

	#	Initialization

	def __init__(self, options=None, args=None):
		rootFolderPath = os.path.abspath(__file__).split("car")[0] + "car/"
		print rootFolderPath
		self.srcPath = rootFolderPath
		self.copyrightPath = os.path.join(rootFolderPath, "misc", "copyright")
		self.verbose = False
		self.includeConsoleLog = True

		self.ignoredNameCache = {}
		self.templateCache = {}

		if options:
			if options.srcPath: self.srcPath = options.srcPath
			if options.verbose and options.verbose == 1: self.verbose = True

		if not self.srcPath.endswith(os.sep):
			self.srcPath = "%s%s" % (self.srcPath, os.sep)

		self.logSetup()


	#	Shutdown

	def shutdown(self):
		pass


	#	Execution

	def process(self):
		try:
			self.logProcessStart()

			self.loadIgnoredFileList()
			self.loadCopyrightTemplates()
			self.processSourceFolder()

			self.logProcessEnd()

		except Exception, e:
			for err in e.args:
				print err

	def processSourceFolder(self):
		self.processOneFolder(self.srcPath)

	def processOneFolder(self, _folderPath):
		subFolderList = []
		shortFolderPath = _folderPath[len(self.srcPath)-1:]
		if self.includeConsoleLog:
			self.logMessage("Processing '%s'" % shortFolderPath)

		names = os.listdir(_folderPath)
		for name in names:
			strippedName = name.strip()
			if strippedName in self.ignoredNameCache:
				pass
			else:
				namePath = os.path.join(_folderPath, name)
				if os.path.isfile(namePath):
					self.processOneFile(_folderPath, name)
				elif os.path.isdir(namePath):
					subFolderList.append(strippedName)

		for subFolderName in subFolderList:
			subFolderPathPath = os.path.join(_folderPath, subFolderName)
			self.processOneFolder(subFolderPathPath)

	def processOneFile(self, _folderPath, _name):
		nameLC = _name.lower()
		if nameLC.endswith('.pyc'): return
		if self.verbose:
			self.logDetailMessage(_name)

		lastDotIdx = nameLC.rfind('.')
		if lastDotIdx > 0:
			suffix = nameLC[lastDotIdx+1:]
			templateCacheData = self.templateCache.get(suffix, None)
			if templateCacheData:
				self.processOneFileUsingTemplate(_folderPath, _name, templateCacheData)

	def processOneFileUsingTemplate(self, _folderPath, _name, _templateCacheData):
		filePath = os.path.join(_folderPath, _name)
		fileData = self.readFileData(filePath)
		fileData = self.removeLeadingBlankLines(fileData)
		if self.fileIsEmpty(fileData):
			self.writeCopyrightAndFileData(filePath, _templateCacheData, None, 0)
		else:
			contentStartIdx = self.findExistingCopyright(fileData, _templateCacheData)
			self.writeCopyrightAndFileData(filePath, _templateCacheData, fileData, contentStartIdx)

	def removeLeadingBlankLines(self, _fileData):
		while _fileData:
			if not _fileData: return _fileData
			if _fileData[0].rstrip(): return _fileData
			_fileData = _fileData[1:]


	def findExistingCopyright(self, _fileData, _templateCacheData):
		#   Returns the index of the first non-copyright line in _fileData.
		if not _templateCacheData: return 0
		if not _fileData: return 0

		#   File Data must start with the Copyright start line.
		copyrightStart = _templateCacheData['startLine']
		if not _fileData[0].rstrip().startswith(copyrightStart):
			return 0

		#   Must find the Copyright end line.
		maxIdx = len(_fileData) - 1
		copyrightEnd = _templateCacheData['endLine']
		idx = 1
		endIdx = 0
		while (idx <= maxIdx):
			if _fileData[idx].rstrip().startswith(copyrightEnd):
				endIdx = idx + 1
				break
			idx = idx + 1
		if not endIdx:
			return 0

		#   Skip blank lines between the Copyright end line and the start of real code.
		while (endIdx <= maxIdx):
			if _fileData[endIdx].rstrip():
				return endIdx
			endIdx = endIdx + 1
		return endIdx

	def fileIsEmpty(self, _fileData):
		if not _fileData: return True
		maxIdx = len(_fileData) - 1
		idx = 0
		while (idx <= maxIdx):
			if _fileData[idx].rstrip():
				return False
			idx = idx + 1
		return True

	def writeCopyrightAndFileData(self, _filePath, __templateCacheData, _fileData, _contentStartIdx):
		f = None
		try:
			f = open(_filePath,'w')
			templateData = __templateCacheData.get('template', [])
			hasCopyright = __templateCacheData.get('hasCopyright', True)
			if templateData and hasCopyright:
				f.writelines(templateData)
			if _fileData and _fileData[_contentStartIdx:]:
				if hasCopyright:
					f.writelines(['\n'])
				f.writelines(_fileData[_contentStartIdx:])
		except Exception, e:
			print "Unable to write file '%s'" % (_filePath)
			raise e
		finally:
			if f: f.close()


	#   Miscellaneous.

	def loadIgnoredFileList(self):
		ignoredNamesFilePath = os.path.join(self.copyrightPath, "ignore.txt")

		if self.includeConsoleLog:
			self.logMessage("Loading ignored file list from: '%s'" % ignoredNamesFilePath)

		self.ignoredNameCache = {}
		ignoredNames = self.readFileData(ignoredNamesFilePath)
		for ignoredName in ignoredNames:
			ignoredNameStrip = ignoredName.strip()
			if ignoredNameStrip:
				if self.verbose:
					self.logDetailMessage(ignoredNameStrip)
				self.ignoredNameCache[ignoredNameStrip] = True

	def loadCopyrightTemplates(self):
		if self.includeConsoleLog:
			self.logMessage("Loading copyright templates from: '%s'" % self.copyrightPath)

		self.templateCache = {}
		names = os.listdir(self.copyrightPath)
		for name in names:
			strippedName = name.strip()
			strippedNameUC = strippedName.upper()
			if strippedNameUC == '.DS_STORE': continue
			if strippedNameUC == 'IGNORE.TXT': continue

			filePath = os.path.join(self.copyrightPath, name)
			if (os.path.isfile(filePath)) and (strippedNameUC.endswith('.TXT')):
				if self.verbose:
					self.logDetailMessage(name)
				suffix = strippedName[0:len(strippedName) - len('.txt')]
				if suffix:
					templateData = self.readFileData(filePath)
					if templateData:
						startLine = self.firstNonBlankTemplateLine(templateData)
						endLine = self.lastNonBlankTemplateLine(templateData)
						if startLine and endLine:
							cacheDict = {}
							cacheDict['template'] = templateData
							cacheDict['startLine'] = startLine
							cacheDict['endLine'] = endLine
							cacheDict['hasCopyright'] = True
							if (len(templateData) == 2) and \
								(templateData[0].strip() == startLine) and \
								(templateData[1].strip() == endLine):
								cacheDict['hasCopyright'] = False
							self.templateCache[suffix.lower()] = cacheDict

	def readFileData(self, _filePath):
		f = None
		try:
			f = open(_filePath,'rU')
			return f.readlines()
		except Exception, e:
			print "Unable to read src file '%s'" % (_filePath)
			raise e
		finally:
			if f: f.close()

	def firstNonBlankTemplateLine(self, _template):
		for i in range(0, len(_template)):
			line = _template[i].strip()
			if line:
				return line
		return ''

	def lastNonBlankTemplateLine(self, _template):
		for i in range(len(_template)-1,-1,-1):
			line = _template[i].strip()
			if line:
				return line
		return ''


	#	Logging

	def logSetup(self):
		if self.includeConsoleLog:
			print "%s Copyright processor created" % (self.getLogTimestamp())
			self.logMessage("Source: %s" % (self.srcPath))
			self.logMessage("Copyright data folder: %s" % self.copyrightPath)
			self.logMessage("Verbose output: %s" % self.verbose)
			self.logMessage("")

	def logProcessStart(self):
		if self.includeConsoleLog:
			self.processStart = self.getLogTimestamp()
			print "%s Copyright process started" % (self.processStart)

	def logProcessEnd(self):
		if self.includeConsoleLog:
			self.processEnd = self.getLogTimestamp()
			self.logMessage("")
			print "%s Copyright process completed" % (self.processEnd)
			print "%s Copyright elapsed time: %s" % (self.processEnd, str(self.processEnd - self.processStart))

	def logMessage(self, _message):
		if self.includeConsoleLog:
			if _message:
				print "%s - %s" % (self.getLogTimestamp(), _message)
			else:
				print "%s" % (self.getLogTimestamp(),)

	def logDetailMessage(self, _message):
		self.logMessage("   %s" % _message)

	def getLogTimestamp(self):
		return datetime.datetime.now()

	def logFatalError(self, _message):
		if self.includeConsoleLog:
			self.logMessage(_message)
		else:
			print(_message)
		exit()


class CopyrightInterface:
	def __init__(self):
		pass

	def get_parser(self):
		descr = '''Applies Copyright notices to all applicable files in a given source code tree.'''
		parser = optparse.OptionParser(description=descr)
		parser.add_option('-i', '--src', dest='srcPath', default='', help='path to source tree folder')
		parser.add_option("-v", "--verbose", dest="verbose", default=1, help="verbose output. 1 = on, 0 = off.")
		return parser

	def run(self, options, args):
		copyRighter = None
		try:
			pass
			copyRighter = Copyright(options, args)
			copyRighter.process()
		except Exception, e:
			for each in e.args:
				print each
		finally:
			if copyRighter:
				copyRighter.shutdown()


if __name__ == '__main__':
	crInterface = CopyrightInterface()
	parser = crInterface.get_parser()
	(options, args) = parser.parse_args()
	crInterface.run(options, args)
