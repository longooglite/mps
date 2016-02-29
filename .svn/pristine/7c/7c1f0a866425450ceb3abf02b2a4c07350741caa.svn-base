# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

#   Base class for interfaces to 3rd-party, external Background and Education Verification Services.
#   In addition to holding common configuration information, this class defines a set of (abstract)
#   methods, which sub-classes must implement. Also implements some convenience routines for use
#   by subclasses.

kOrderTypePackage = 'package'
kOrderTypeService = 'service'

class AbstractBackgroundCheckService(object):
	def __init__(self, _container, _dbConnection):
		self.container = _container
		self.connection = _dbConnection
		self.backgroundCheckClassName = _container.getConfigDict().get('backgroundCheckClassName', '')
		self.backgroundCheckConfig = _container.getConfigDict().get('backgroundCheckConfig', {})


	################################################################################
	#   Convenience routines.
	################################################################################

	#   Returns the 'fake' configuration setting.
	#   True indicates that all responses should be fake.
	#   False means actually interact with the 3rd-party service.

	def isFake(self):
		return self.backgroundCheckConfig.get('fake', True)


	#   Set a status in the given dictionary.

	def setOKStatus(self, _dict):
		_dict['status'] = 'ok'
	def setErrorStatus(self, _dict):
		_dict['status'] = 'error'


	################################################################################
	#   Abstract methods.
	################################################################################

	#   Submit a request to the 3rd-party service, initiating a new request.
	#
	#   Input:
	#       doCommit:       True if any database activity should be immediately committed.
	#                       False if no database activity should be committed.
	#
	#   Output: a dictionary that may contain the following keys:
	#       status:         'ok' if the request was successfully created and sent
	#                       'error' if any issues were encountered
	#       externalKey:    a unique string representing this request. This becomes the identifier used
	#                       in subsequent inquiries with regard to this specific request.
	#       error:          error information, preferably a string
	#                       applicable when status is 'error'

	def submit(self, doCommit, **kwargs):
		raise Exception("submit not implemented")


	#   Query the status of an outstanding request.
	#
	#   Input:
	#       externalKey:    a unique string representing the request.
	#       doCommit:       True if any database activity should be immediately committed.
	#                       False if no database activity should be committed.
	#
	#   Output: a dictionary that may contain the following keys:
	#       status:         'ok' if the request was successfully created and sent
	#                       'error' if any issues were encountered
	#       complete:       True if the 3rd-party service has completed its work.
	#                       False if their work in stall in-progress.
	#       flagged:        True if the 3rd-party service marked any order as potentially problematic.
	#                       False otherwise.
	#                       Only meaningful when complete = True.
	#       error:          error information, preferably a string
	#                       applicable when status is 'error'

	def getCandidateStatus(self, _externalKey, doCommit, **kwargs):
		raise Exception("getCandidateStatus not implemented")


	#   Obtain URL to the most recent report for an outstanding request.
	#
	#   Input:
	#       externalKey:    a unique string representing the request.
	#       doCommit:       True if any database activity should be immediately committed.
	#                       False if no database activity should be committed.
	#
	#   Output: a dictionary that may contain the following keys:
	#       status:         'ok' if the request was successfully created and sent
	#                       'error' if any issues were encountered
	#       url:            URL to existing report, if any.
	#       error:          error information, preferably a string
	#                       applicable when status is 'error'

	def getCandidateReport(self, _externalKey, doCommit, **kwargs):
		raise Exception("getCandidateReport not implemented")


	#   Obtain the List of Orders pertaining to this Background and Education Check request.
	#
	#   Input:
	#       doCommit:       True if any database activity should be immediately committed.
	#                       False if no database activity should be committed.
	#
	#   Output: a dictionary that may contain the following keys:
	#       status:         'ok' if the request was successfully created and sent
	#                       'error' if any issues were encountered
	#       orderList:      a List of Orders. Each Order is a dictionary containing the following keys:
	#                           orderType:      'package' or 'service'
	#                           orderCode:      a unique code identifying the Order
	#                           orderDescr:     human-readable description of the Order
	#                           orderID:        code sent to 3rd-party service to identify this order
	#       error:          error information, preferably a string
	#                       applicable when status is 'error'

	def getOrders(self, doCommit, **kwargs):
		raise Exception("getOrders not implemented")
