# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import MPSCore.utilities.exceptionUtils as excUtils
import MPSAppt.core.sql.positionSQL as posSQL
import MPSAppt.services.lookupTableService as lookupTableSvc
import MPSAppt.services.departmentService as deptSvc
import MPSAppt.core.constants as constants

def createPosition(_dbConnection, _positionDict, _departmentDict, doCommit=True):
	try:
		if _positionDict.get('manualpcn',''):
			return createManuallyEnteredPosition(_dbConnection,_positionDict,doCommit)
		pcn = _positionDict.get('pcn', None)
		if not pcn:
			pcnList = getPcn(_dbConnection, _departmentDict.get('pcn_id', None))
			if not pcnList:
				raise excUtils.MPSValidationException("Department PCN not found")

			pcnDict = pcnList[0]
			pcnDict['seq'] = pcnDict.get('seq',None) + 1
			updatePcnSequence(_dbConnection, pcnDict, doCommit=False)
			pcn = formatPcn(pcnDict)
			_positionDict['pcn'] = pcn

		positionId = posSQL.createPosition(_dbConnection, _positionDict, doCommit=False)
		if doCommit:
			_dbConnection.performCommit()
		return positionId

	except Exception, e:
		try: _dbConnection.performRollback()
		except Exception, e1: pass
		raise e

def createManuallyEnteredPosition(_dbConnection,_positionDict, doCommit=True):
	try:
		_positionDict['pcn'] = _positionDict.get('manualpcn','')
		positionId = posSQL.createPosition(_dbConnection, _positionDict, doCommit=False)
		if doCommit:
			_dbConnection.performCommit()
		return positionId
	except Exception, e:
		try: _dbConnection.performRollback()
		except Exception, e1: pass
		raise e




def deletePosition(_dbConnection,pcnId):
	posSQL.deletePosition(_dbConnection,pcnId)

def formatPcn(_pcnDict, _pcnFormatString='%s-%05d'):
	return _pcnFormatString % (_pcnDict.get('code',None), _pcnDict.get('seq',None))

def getPcn(_dbConnection, _pcnId):
	return posSQL.getPcn(_dbConnection, _pcnId)

def getPostionById(_dbConnection, _id):
	return posSQL.getPostionById(_dbConnection, _id)

def getPostionFromPCN(_dbConnection, _pcn):
	return posSQL.getPostionFromPCN(_dbConnection, _pcn)

def updatePcnSequence(_dbConnection, _pcnDict, doCommit=True):
	posSQL.updatePcnSequence(_dbConnection, _pcnDict, doCommit)

def getDepartment(_dbConnection,positionId):
	departmentDict = {}
	position = getPostionById(_dbConnection,positionId)
	if position:
		departmentDict = deptSvc.DepartmentService(_dbConnection).getDepartment(position.get('department_id',0))
	return departmentDict

def getPositionsForDepartment(_dbConnection,_departmentDict):
	return posSQL.getPositionsForDepartment(_dbConnection,_departmentDict.get('id',-1))

def updateTitle(_dbConnection, _positionDict, doCommit=True):
	posSQL.updateTitle(_dbConnection, _positionDict, doCommit)

def updatePrimaryOrSecondaryPostionType(_dbConnection,positionDict,jobActionTypeId):
	jobActionType = lookupTableSvc.getEntityByKey(_dbConnection,'wf_job_action_type',jobActionTypeId,'id')
	changePositionType = False
	if jobActionType:
		isPrimary = True
		jaTypeCode = jobActionType.get('code','')
		if jaTypeCode in constants.kSecondaryPositionJobActionTypes:
			changePositionType = True
			isPrimary = False
		elif jaTypeCode in constants.kPrimaryPositionJobActionTypes:
			changePositionType = True
			isPrimary = True
		if changePositionType:
			if positionDict and positionDict.get('is_primary',True) <> isPrimary:
				positionDict['is_primary'] = isPrimary
				posSQL.updatePrimaryStatus(_dbConnection,positionDict,isPrimary)