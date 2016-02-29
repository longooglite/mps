# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

from MPSAppt.modules.abstractArtifact import AbstractArtifact

class Artifact(AbstractArtifact):
	def __init__(self, params):
		AbstractArtifact.__init__(self, params)

	def getContent(self):
		content = None
		try:
			f = open(self.params.get('env').srcRootFolderPath + '/misc/sandbox/' + 'marina_packet.pdf','rb')
			content = bytearray(f.read())
			f.close()
		except Exception,e:
			pass
		#artifacts responsible for returning these 3 values
		return {"descr":"marina","content":content,"pages":1}
