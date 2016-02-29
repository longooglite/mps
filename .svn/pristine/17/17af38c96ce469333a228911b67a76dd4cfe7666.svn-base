# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

from MPSAppt.core.containers.baseContainer import BaseContainer, buildContainer

class Container(BaseContainer):

	#   Containers hold other Containers and Tasks.

	def __init__(self, containerCode, parameterBlock):
		BaseContainer.__init__(self, containerCode, parameterBlock)
		self.setContainers([])

		for containerName in parameterBlock.get('containerDict',{}).get('containers', []):
			container =  buildContainer(containerName, parameterBlock)
			if container:
				self.addContainer(container)

	def getContainers(self): return self.containers
	def setContainers(self,_containers): self.containers = _containers
	def addContainer(self, _container):
		self.containers.append(_container)

	#   Overrides.

	def isComplete(self):
		if not self.getIsEnabled():
			return True
		for each in self.getContainers():
			if not each.isComplete():
				return False
		return True

	def isCompleteWithConsiderations(self):
		if (not self.getIsEnabled()) or self.getIsOptional():
			return True

		for each in self.getContainers():
			if not each.isCompleteWithConsiderations():
				return False
		return True

	#   Status calculation.

	def computeStatus(self):
		lastStatus = ''
		for each in self.getContainers():
			containerStatusMessage = each.computeStatus()
			if containerStatusMessage:
				lastStatus = containerStatusMessage

			theBuckStopsHere = not each.isCompleteWithConsiderations()
			if theBuckStopsHere:
				return lastStatus

		if self.getIsEnabled() and self.getStatusMsg():
			lastStatus = self.getStatusMsg()
		return lastStatus

