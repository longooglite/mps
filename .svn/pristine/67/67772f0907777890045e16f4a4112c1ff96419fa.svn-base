# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

#   Instantiate an object that interfaces with a 3rd-party, external Background and Education Verification Service.
#   The container has configuration data to indicate which interface should be created.

def instantiateBackgroundCheck(_container, _dbConnection):
	if not _container: return None
	backgroundCheckClassName = _container.getConfigDict().get('backgroundCheckClassName', '')
	if not backgroundCheckClassName: return None

	try:
		importString = "from MPSAppt.core.backgroundCheck.%s import %s" % (backgroundCheckClassName, backgroundCheckClassName)
		exec importString

		bcObj = eval(backgroundCheckClassName + '(_container, _dbConnection)')
		return bcObj

	except Exception, e:
		return None
