# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

from MPSAppt.modules.abstractArtifact import AbstractArtifact
import MPSAppt.modules.evalLetters as evalLetters
import json

class Artifact(AbstractArtifact):
	def __init__(self, params):
		AbstractArtifact.__init__(self, params)

	def getContent(self):
		try:
			returnVal = evalLetters.getEvaluatorLetters(self.dbConnection,eval(self.config),self.workflow,"Internal Evaluation Letters",self.env)
			return returnVal
		except Exception,e:
			pass
