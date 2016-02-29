# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import MPSAppt.services.lookupTableService as lookupSvc
import MPSAppt.core.sql.wfEditSQL as sqlLib
import pprint
import json



defaultWFContainer = {
	"code": "",
	"descr": "",
	"header": "",
	"componentType": "Workflow",
	"affordanceType":"",
    "metaTrackCodes":[],
    "jobActionType":"",
	"optional": False,
	"enabled": True,
	"accessPermissions": [],
	"viewPermissions": [],
	"blockers": [],
	"statusMsg": "",
	"className": "Container",
	"containers": []
}

defaultTABContainer = {
	"code": "",
	"descr": "",
	"header": "",
	"componentType": "Container",
    "affordanceType":"Tab",
	"optional": False,
	"enabled": True,
	"accessPermissions": [],
	"viewPermissions": [],
	"blockers": [],
	"statusMsg": "",
	"className": "Container",
	"containers": []
}

defaultSectionContainer = {
	"code": "",
	"descr": "",
	"header": "",
	"componentType": "Container",
    "affordanceType":"Section",
	"optional": False,
	"enabled": True,
	"accessPermissions": [],
	"viewPermissions": [],
	"blockers": [],
	"statusMsg": "",
	"className": "Container",
	"containers": []
}

defaultItemContainer = {
	"code": "",
	"descr": "",
	"header": "",
	"componentType": "Task",
    "affordanceType":"Item",
	"optional": False,
	"enabled": True,
	"accessPermissions": [],
	"viewPermissions": [],
	"blockers": [],
	"containers": [],
    "statusMsg": "",
	"className": "",
	"config": {},
}

defaultGenericContainer = {
	"code": "",
	"descr": "",
	"header": "",
	"componentType": "Container",
    "affordanceType":"",
	"optional": False,
	"enabled": True,
	"accessPermissions": [],
	"viewPermissions": [],
	"blockers": [],
	"statusMsg": "",
	"className": "Container",
	"containers": []
}


class WorkflowService:
	def __init__(self,_connection):
		self.db = _connection

	def createWorkflow(self,argsDict):
		job_action_type = lookupSvc.getEntityByKey(self.db,'wf_job_action_type',argsDict.get('jobactiontypecode','').upper())
		if not job_action_type:
			return "Invalid Job Action Type"
		component_type = lookupSvc.getEntityByKey(self.db,'wf_component_type',"WORKFLOW")
		if not component_type:
			return "Unable to find WORKFLOW component type"
		try:
			if not self.componentExists(argsDict.get('workflowcode','')):
				component = defaultWFContainer
				component['code'] = argsDict.get('workflowcode','')
				component['descr'] = argsDict.get('workflowdescr','')
				component['header'] = argsDict.get('workflowdescr','')
				component['jobActionType'] = job_action_type.get('code','')
				src = self.getComponentSource(component)
				sqlLib.createWorkflowComponent(self.db,argsDict.get('workflowcode',''),argsDict.get('workflowdescr',''),json.dumps(component),False,src,component_type.get('id',0),False)
			if not self.workflowExists(argsDict.get('workflowcode','')):
				sqlLib.createWorkflow(self.db,argsDict.get('workflowcode',''),argsDict.get('workflowdescr',''),job_action_type.get('id',-1),False)
		except:
			self.db.executeSQLCommand('rollback',())
		finally:
			self.db.executeSQLCommand('commit',())
			return 'ok'

	def addTab(self,argsDict):
		msg = 'ok'
		component_type = lookupSvc.getEntityByKey(self.db,'wf_component_type',"CONTAINER")
		if not component_type:
			return "Unable to find CONTAINER component type"
		if not self.componentExists(argsDict.get('tabcode','')):
			component = defaultTABContainer
			component['code'] = argsDict.get('tabcode','')
			component['descr'] = argsDict.get('tabdescr','')
			component['header'] = argsDict.get('tabdescr','')
			msg = self.persistAndAssociateContainer(component,component_type,argsDict.get('workflowcode',''),argsDict.get('optionalposition',''))
		return msg

	def addSection(self,argsDict):
		msg = 'ok'
		component_type = lookupSvc.getEntityByKey(self.db,'wf_component_type',"CONTAINER")
		if not component_type:
			return "Unable to find CONTAINER component type"
		if not self.componentExists(argsDict.get('sectioncode','')):
			component = defaultSectionContainer
			component['code'] = argsDict.get('sectioncode','')
			component['descr'] = argsDict.get('sectiondescr','')
			component['header'] = argsDict.get('sectiondescr','')
			msg = self.persistAndAssociateContainer(component,component_type,argsDict.get('tabcode',''),argsDict.get('optionalposition',''))
		return msg

	def addItem(self,argsDict):
		msg = 'ok'
		component_type = lookupSvc.getEntityByKey(self.db,'wf_component_type',"TASK")
		if not component_type:
			return "Unable to find TASK component type"
		if not self.componentExists(argsDict.get('itemcode','')):
			component = defaultItemContainer
			component['code'] = argsDict.get('itemcode','')
			component['descr'] = argsDict.get('itemdescr','')
			component['header'] = argsDict.get('itemdescr','')
			component['className'] = argsDict.get('classname','')
			msg = self.persistAndAssociateContainer(component,component_type,argsDict.get('sectioncode',''),argsDict.get('optionalposition',''))
		return msg

	def addContainer(self,argsDict):
		msg = 'ok'
		component_type = lookupSvc.getEntityByKey(self.db,'wf_component_type',"CONTAINER")
		if not component_type:
			return "Unable to find CONTAINER component type"
		if self.componentExists(argsDict.get('parentcontainercode','')):
			component = defaultGenericContainer
			component['code'] = argsDict.get('code','')
			component['descr'] = argsDict.get('descr','')
			component['header'] = argsDict.get('descr','')
			msg = self.persistAndAssociateContainer(component,component_type,argsDict.get('parentcontainercode',''),argsDict.get('optionalposition',''))
		else:
			return "parent container does not exist"
		return msg


	def persistAndAssociateContainer(self,component,component_type,workflowCode,optionalPosition):
		src = self.getComponentSource(component)
		sqlLib.createWorkflowComponent(self.db,component.get('code',''),component.get('descr',''),json.dumps(component),False,src,component_type.get('id',0))
		msg = self.associateContainers(component.get('code',''),workflowCode,optionalPosition)
		return msg

	def renameContainer(self,argsDict):
		msg = 'ok'
		origCode = argsDict.get('containercode','')
		newCode = argsDict.get('newcode','')
		optionalDesc = argsDict.get('optionalnewdescr','')
		containerRows = sqlLib.getAllContainerRows(self.db)
		for containerRow in containerRows:
			if containerRow.get('code') == origCode:
				self.renameCoreContainer(containerRow,newCode,optionalDesc)
			else:
				self.renameDependencies(containerRow,origCode,newCode)

	def renameCoreContainer(self,containerRow,newCode,optionalDesc):
		try:
			component = json.loads(containerRow.get('value'))
			origCode = component['code']
			component_type = lookupSvc.getEntityByKey(self.db,'wf_component_type',"WORKFLOW")
			if containerRow.get('component_type_id') == component_type.get('id',-1):
				sqlLib.updateWorkflowCodeDescr(self.db,origCode,newCode,optionalDesc,False)
			component['code'] = newCode
			if optionalDesc:
				component['header'] = optionalDesc
				component['descr'] = optionalDesc
			src = self.getComponentSource(component)
			sqlLib.updateComponentCodeSrcAndValue(self.db,newCode,src,json.dumps(component),origCode,False)
		except Exception,e:
			self.db.executeSQLCommand("rollback")
		finally:
			self.db.executeSQLCommand("commit")

	def renameDependencies(self,containerRow,origCode,newCode):
		component = json.loads(containerRow.get('value'))
		componentCode = component.get('code','')
		changedDict = {"changed":False}
		self.renameDict(component,origCode,newCode,changedDict)
		if changedDict.get('changed'):
			src = self.getComponentSource(component)
			value = json.dumps(component)
			sqlLib.updateComponentSrcAndValue(self.db,src,value,componentCode)

	def renameDict(self,aDict,origCode,newCode,changedDict):
		dictKeys = aDict.keys()
		for key in dictKeys:
			dtype = type(aDict.get(key,None))
			if dtype is str or dtype is unicode:
				if aDict[key] == origCode:
					aDict[key] = newCode
					changedDict['changed'] = True
			elif dtype is list:
				self.updateListWithNewCode(aDict[key],origCode,newCode,changedDict)
			elif dtype is dict:
				self.renameDict(aDict[key],origCode,newCode,changedDict)

	def updateListWithNewCode(self,theList,origCode,newCode,changedDict):
		changed = False
		counter = 0
		for item in theList:
			if type(item) in (str,unicode):
				if item == origCode:
					theList[counter] = newCode
					changedDict['changed'] = True
			elif type(item) is dict:
				self.renameDict(item,origCode,newCode)
			counter += 1
		return changed

	def getAllCodes(self):
		allCodes = sqlLib.getAllContainerCodesAndDescriptions(self.db)
		return allCodes


	def updateKV(self,argsDict):
		container = self.getContainerDict(argsDict.get('containercode',''))
		if not container:
			return "container not found"
		key = argsDict.get('key','')
		if key:
			keys = key.split('.')
			if len(keys) == 1:
				container[key] = argsDict.get('value','')
			else:
				dict = {}
				lastKey = keys[len(keys)-1]
				for key in keys:
					if key <> lastKey:
						dict = container.get(key,{})
				dict[lastKey] = argsDict.get('value','')

		src = self.getComponentSource(container)
		value = json.dumps(container)
		sqlLib.updateComponentSrcAndValue(self.db,src,value,container.get('code',''))
		return 'ok'


	def associateContainers(self,childCode,parentCode,optionalPosition):
		positionInt = self.getInt(optionalPosition)
		parentContainerRow = self.getContainerRow(parentCode)
		if not parentContainerRow:
			return "Unable to associate to parent"
		parentContainerDict = json.loads(parentContainerRow.get('value','{"containers":[]}'))

		containersList = parentContainerDict.get('containers',[])
		parentContainerDict['containers'] = self.addCodeToListAtIndex(childCode,containersList,positionInt)
		component = self.getComponentSource(parentContainerDict)

		sqlLib.updateComponentSrcAndValue(self.db,component,json.dumps(parentContainerDict),parentContainerDict.get('code',''),)
		return 'ok'

	def getContainerDict(self,workflowCode):
		qry = sqlLib.getContainerJSON(self.db,workflowCode)
		return json.loads(qry[0]['value']) if qry else None
	####### helpers ######

	def addCodeToListAtIndex(self,theCode,theList,positionInt):
		if not theCode in theList:
			if positionInt < 1 or positionInt > len(theList):
				theList.append(theCode)
			else:
				theList.insert(positionInt,theCode)
		return theList

	def getComponentSource(self,component):
		code = component.get('code','')
		srcString = "%s = %s" % (code,str(json.dumps(component,indent=4)))
		return srcString

	def componentExists(self,componentCode):
		return lookupSvc.getEntityByKey(self.db,'wf_component',componentCode) is not None

	def workflowExists(self,componentCode):
		return lookupSvc.getEntityByKey(self.db,'wf_workflow',componentCode) is not None


	def getContainerRow(self,parentCode):
		return lookupSvc.getEntityByKey(self.db,'wf_component',parentCode)

	def getInt(self,str):
		returnVal = -1
		try:
			returnVal = int(str)
		except Exception,e:
			pass
		finally:
			return returnVal