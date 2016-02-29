# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import MPSAppt.core.backgroundCheck.abstractBackgroundCheckService as absBCSvc
import MPSAppt.core.backgroundCheck.abstractCredentialCheckService as absCCSvc
import MPSAppt.services.jobActionResolverService as resolverSvc
import MPSAppt.core.constants as constants
import MPSCore.utilities.stringUtilities as stringUtils

kUofMPackage = 'UOFM_PACKAGE'
kStateTypeII = 'STATE_TYPE_II'
kFederalCriminal = 'FEDERAL_CRIMINAL'
kCountyCriminal = 'FEL_MISD'
kEducationVerification = 'EDUCATION_VERIFICATION'
kUofMDrugTest = 'UM_DRUG_TEST'
kCredentialCheckDrugTest = 'CRCK_DRUG_TEST'

ummsOrders = {
	kUofMPackage: {
		'orderCode': kUofMPackage,
		'orderDescr': 'U of M Package',
		'orderType': absBCSvc.kOrderTypePackage,
		'orderID': '513'
	},
	kStateTypeII: {
		'orderCode': kStateTypeII,
		'orderDescr': 'Statewide Type II - UofM GME',
		'orderType': absBCSvc.kOrderTypeService,
		'orderID': '353'
	},
	kFederalCriminal: {
		'orderCode': kFederalCriminal,
		'orderDescr': 'Federal Criminal',
		'orderType': absBCSvc.kOrderTypeService,
		'orderID': '283'
	},
	kCountyCriminal: {
		'orderCode': kCountyCriminal,
		'orderDescr': 'County Criminal Search',
		'orderType': absBCSvc.kOrderTypeService,
		'orderID': '281'
	},
	kEducationVerification: {
		'orderCode': kEducationVerification,
		'orderDescr': 'Education - U of M',
		'orderType': absBCSvc.kOrderTypeService,
		'orderID': '376'
	},
	kUofMDrugTest: {
		'orderCode': kUofMDrugTest,
		'orderDescr': 'Institution Facilitated Drug Test',
		'orderType': absBCSvc.kOrderTypeService,
		'orderID': '16'
	},
	kCredentialCheckDrugTest: {
		'orderCode': kCredentialCheckDrugTest,
		'orderDescr': 'Service Faciltated Drug Test',
		'orderType': absBCSvc.kOrderTypeService,
		'orderID': '282'
	},
}

class UMMSBackgroundCheck(absCCSvc.AbstractCredentialCheckService):
	def __init__(self, _container, _dbConnection):
		absCCSvc.AbstractCredentialCheckService.__init__(self, _container, _dbConnection)

	################################################################################
	#   Required method implementations.
	################################################################################

	#   Obtain the List of Orders pertaining to this Background and Education Check request.
	#   See superclass for description.

	def getCredentialCheckOrders(self, **kwargs):
		orderList = []

		self.container.loadInstance()
		bgCheck = self.container.getBackgroundCheck()
		if bgCheck:
			personalInfoContainer = self.container.locateEnabledPersonalInfoContainer()
			if personalInfoContainer.isComplete():

				#   Do not send these Orders if CBC is 'Waived'
				if not self._isCBCWaived(personalInfoContainer):
					orderList.append(ummsOrders[kUofMPackage])
					orderList.append(ummsOrders[kStateTypeII])
					orderList.append(ummsOrders[kFederalCriminal])
					orderList.append(ummsOrders[kCountyCriminal])

				#   Do not send Education Verification Order if Candidate
				#   attended med school outside the US.
				if not self._isEdVerifyWaived(personalInfoContainer):
					orderList.append(ummsOrders[kEducationVerification])

				#   Do not send drug test for Adjunct.
				jobActionDict = self.container.getWorkflow().getJobActionDict()
				jaResolver = resolverSvc.JobActionResolverService(self.connection, {})
				context = jaResolver.resolve(jobActionDict)
				if 'ADJUNCT' not in context.get('title',{}).get('tags','').upper():
					#   Only use credential check automated drug test if prospect lives in US
					if self._isLivingInUS(personalInfoContainer):
						orderList.append(ummsOrders[kCredentialCheckDrugTest])
					else:
						orderList.append(ummsOrders[kUofMDrugTest])

		return orderList

	def _isLivingInUS(self, _personalInfoContainer):
		_personalInfoContainer.loadInstance()
		if _personalInfoContainer.getClassName() == constants.kContainerClassUberForm:
			livingResponse = self._getUberformResponseForIdentifierCode(_personalInfoContainer, 'living_in_us', 'false')
			return stringUtils.interpretAsTrueFalse(livingResponse)

		return False

	def _isCBCWaived(self, _personalInfoContainer):
		_personalInfoContainer.loadInstance()
		if _personalInfoContainer.getClassName() == constants.kContainerClassUberForm:
			livingInUS = self._isLivingInUS(_personalInfoContainer)
			if livingInUS:
				return False
			hasSSNResponse = self._getUberformResponseForIdentifierCode(_personalInfoContainer, 'has_ssn', 'false')
			return not stringUtils.interpretAsTrueFalse(hasSSNResponse)

		return False

	def _isEdVerifyWaived(self, _personalInfoContainer):
		_personalInfoContainer.loadInstance()
		if _personalInfoContainer.getClassName() == constants.kContainerClassUberForm:
			hdCountryResponse = self._getUberformResponseForIdentifierCode(_personalInfoContainer, 'hd_country', '')
			return hdCountryResponse not in ['United States of America', 'UnitedStatesofAmerica']

		return False

	def _getUberformResponseForIdentifierCode(self, _personalInfoContainer, _identifierCode, _defaultResponse):
		response = _personalInfoContainer.getResponseCacheByIdentifierCode().get(_identifierCode, '')
		if not response:
			return _defaultResponse
		return response
