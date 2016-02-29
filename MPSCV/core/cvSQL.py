# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

######################## CV Person ########################

def getPerson(_dbConnection, community, user_id):
	sql = "SELECT * FROM cv_person WHERE community = %s AND lower(user_id) = %s;"
	args = (community, user_id.lower())
	return _dbConnection.executeSQLQuery(sql,args)

def createPerson(_dbConnection, community, user_id, doCommit=True):
	sql = "INSERT INTO cv_person (community,user_id) values (%s,%s);"
	args = (community, user_id.lower())
	_dbConnection.executeSQLCommand(sql, args, doCommit)

def getFormalName(_dbConnection, _community, _username, _cvNameCode):
	sql = '''SELECT attribute_value FROM cv_person,cv_row,cv_attribute,cv_field
	WHERE cv_person.community = %s AND lower(cv_person.user_id) = %s AND
	cv_row.person_id = cv_person.id AND
	cv_attribute.row_id = cv_row.id AND
	cv_attribute.field_id = cv_field.id
	AND cv_field.code = %s;'''
	args = (_community, _username.lower(), _cvNameCode)
	return _dbConnection.executeSQLQuery(sql,args)

def deletePerson(_dbConnection, _community, _username, doCommit=True):
	sql = '''DELETE FROM cv_person WHERE community = %s AND lower(user_id) = %s'''
	args = (_community, _username)
	return _dbConnection.executeSQLCommand(sql, args, doCommit)

def whackPersonData(_dbConnection, _community, _username, doCommit=True):
	sql = '''UPDATE cv_person SET pubmedsearchkey='' WHERE community = %s AND lower(user_id) = %s'''
	args = (_community, _username)
	return _dbConnection.executeSQLCommand(sql, args, doCommit)

######################## CV Proxies ########################

def getProxiedCVsForGrantee(_dbConnection, community, grantee):
	sql = "SELECT * FROM cv_proxy WHERE grantee_community = %s AND lower(grantee) = %s AND deleted = false and accepted_when <> '';"
	args = (community, grantee.lower())
	return _dbConnection.executeSQLQuery(sql,args)

def getProxiedCVsForGrantor(_dbConnection, community, grantor):
	sql = "SELECT * FROM cv_proxy WHERE grantor_community = %s AND lower(grantor) = %s AND deleted = false;"
	args = (community, grantor.lower())
	return _dbConnection.executeSQLQuery(sql,args)

def getProxiedCVForGrantorAndGrantee(_dbConnection, grantor_community, grantor, grantee_community, grantee):
	sql = "SELECT * FROM cv_proxy WHERE grantor_community = %s AND lower(grantor) = %s AND grantee_community = %s AND lower(grantee) = %s AND deleted = false;"
	args = (grantor_community, grantor.lower(), grantee_community, grantee.lower())
	return _dbConnection.executeSQLQuery(sql,args)

def updateProxyApproval(_dbConnection,id, canWrite, now):
	sql = "UPDATE cv_proxy SET can_write = %s, accepted_when = %s  WHERE id = %s"
	args = (canWrite,now,id,)
	return _dbConnection.executeSQLCommand(sql,args)

def updateProxyDenied(_dbConnection,id, now):
	sql = "UPDATE cv_proxy SET deleted = true,accepted_when = %s, deleted_when = %s WHERE id = %s"
	args = (now,now,id,)
	return _dbConnection.executeSQLCommand(sql,args)

def updateProxyRole(_dbConnection, id, canWrite):
	sql = "UPDATE cv_proxy SET can_write = %s WHERE id = %s"
	args = (canWrite, id,)
	return _dbConnection.executeSQLCommand(sql,args)

def saveNewProxy(_dbConnection, grantor_community, grantor, grantee_community, grantee, canReadWrite, now):
	sql = "INSERT INTO cv_proxy (grantor_community,grantor,grantee_community,grantee,can_write,accepted_when,requested_when) VALUES (%s,%s,%s,%s,%s,%s,%s)"
	args = (grantor_community,grantor.lower(),grantee_community,grantee.lower(),canReadWrite,now,now)
	return _dbConnection.executeSQLCommand(sql,args)

def saveRequestForProxyAccess(_dbConnection, cvholder_community, cvholder, proxyrequestor_community, proxyrequestor, requestingReadWrite, now):
	sql = "INSERT INTO cv_proxy (grantor_community,grantor,grantee_community,grantee,can_write,requested_when) VALUES (%s,%s,%s,%s,%s,%s);"
	args = (cvholder_community, cvholder.lower(), proxyrequestor_community, proxyrequestor.lower(), requestingReadWrite, now)
	return _dbConnection.executeSQLCommand(sql,args)

######################## CV Data ########################

def getRow(_dbConnection, _rowId):
	sql = '''SELECT
			ROW.id AS row_id,
			ROW.person_id AS row_person_id,
			ROW.exclude_from_cv_val AS row_exclude_from_cv_val,
			ROW.user_sort_seq AS row_user_sort_seq,
			ROW.who_dunit AS row_who_dunit,
			ROW.when_dunit AS row_when_dunit
		FROM cv_row AS ROW
		WHERE ROW.id = %s'''
	args = (_rowId,)
	return _dbConnection.executeSQLQuery(sql,args)

def getRowData(_dbConnection, _rowId):
	sql = '''SELECT
			ROW.id AS row_id,
			ROW.person_id AS row_person_id,
			ROW.exclude_from_cv_val AS row_exclude_from_cv_val,
			ROW.user_sort_seq AS row_user_sort_seq,
			ROW.who_dunit AS row_who_dunit,
			ROW.when_dunit AS row_when_dunit,
			ATT.id AS attribute_id,
			ATT.field_id AS attribute_field_id,
			ATT.attribute_value AS attribute_value,
			ATT.who_dunit AS attribute_who_dunit,
			ATT.when_dunit AS attribute_when_dunit
		FROM cv_attribute AS ATT
			JOIN cv_row AS ROW ON ROW.id = ATT.row_id
		WHERE ROW.id = %s
		ORDER BY ATT.id'''
	args = (_rowId,)
	return _dbConnection.executeSQLQuery(sql,args)

def getRowPerson(_dbConnection, _rowId):
	sql = '''SELECT PERSON.* FROM cv_row AS ROW JOIN cv_person AS PERSON ON ROW.person_id = PERSON.id WHERE ROW.id=%s'''
	args = (_rowId,)
	return _dbConnection.executeSQLQuery(sql,args)

def rowExistsForCategoryAndAttributeValue(_dbConnection,cv_id,fieldCode,categoryCode,fieldValue):
	sql = '''SELECT COUNT(*) AS count FROM cv_row,cv_attribute,cv_field,cv_field_group,cv_category WHERE
	cv_row.person_id = %s AND
	cv_row.id = cv_attribute.row_id AND
	cv_attribute.field_id = cv_field.id AND
	cv_attribute.attribute_value = %s AND
	cv_field.code = %s AND
	cv_field.field_group_id = cv_field_group.id AND
	cv_field_group.category_id = cv_category.id AND
	cv_category.code = %s;'''
	args = (cv_id,fieldValue,fieldCode,categoryCode)
	qry = _dbConnection.executeSQLQuery(sql,args)
	return False if qry[0]['count'] == 0 else True

def rowExistsForPubMedID(_dbConnection,cv_id,fieldCodeINList,fieldValue):
	sql = '''SELECT COUNT(*) AS count FROM cv_row,cv_attribute,cv_field,cv_field_group WHERE
	cv_row.person_id = %s AND
	cv_row.id = cv_attribute.row_id AND
	cv_attribute.field_id = cv_field.id AND
	cv_attribute.attribute_value = %s AND
	cv_field.code IN''' + fieldCodeINList + ''' AND
	cv_field.field_group_id = cv_field_group.id'''
	args = (cv_id,fieldValue)
	qry = _dbConnection.executeSQLQuery(sql,args)
	return False if qry[0]['count'] == 0 else True

def deletePubMedPublication(_dbConnection,cv_id,fieldCodeINList,fieldValue):
	sql = '''SELECT cv_row.id FROM cv_row,cv_attribute,cv_field,cv_field_group WHERE
	cv_row.person_id = %s AND
	cv_row.id = cv_attribute.row_id AND
	cv_attribute.field_id = cv_field.id AND
	cv_attribute.attribute_value = %s AND
	cv_field.code IN''' + fieldCodeINList + ''' AND
	cv_field.field_group_id = cv_field_group.id'''
	args = (cv_id,fieldValue)
	qry = _dbConnection.executeSQLQuery(sql,args)
	if qry:
		sql = "DELETE FROM cv_attribute WHERE row_id = %s"
		args = (qry[0]['id'],)
		_dbConnection.executeSQLCommand(sql,args)
		sql = "DELETE FROM cv_row WHERE id = %s"
		args = (qry[0]['id'],)
		_dbConnection.executeSQLCommand(sql,args)

def getCVListDisplayDataForUser(_dbConnection, _community, _username, _categoryName, isPrintedCV = False):
	sql = '''SELECT
			ROW.id AS row_id,
			ROW.exclude_from_cv_val AS row_exclude_from_cv_val,
			ROW.user_sort_seq AS row_user_sort_seq,
			ROW.who_dunit AS row_who_dunit,
			ROW.when_dunit AS row_when_dunit,
			FIELD.id AS field_id,
			FIELD.code AS field_code,
			FIELD.descr AS field_descr,
			FIELD.alt_descr AS field_alt_descr,
			FIELD.required AS field_required,
			FIELD.seq AS field_seq,
			FIELD.display_on_list_seq AS field_display_on_list_seq,
			FIELD.display_on_pdf_seq AS field_display_on_pdf_seq,
			FIELD.list_display_options AS field_list_display_options,
			FIELD.list_sort_key_seq AS field_list_sort_key_seq,
			FIELD.text_length AS field_text_length,
			FIELD.text_height AS field_text_height,
			FIELD.static_lookup_code AS field_static_lookup_code,
			FIELD.date_format AS field_date_format,
			FIELD.help_text AS field_help_text,
			AFF.id as affordance_id,
			AFF.code as affordance_code,
			AFF.descr as affordance_descr,
			ATT.id AS attribute_id,
			ATT.attribute_value AS attribute_value,
			ATT.who_dunit AS attribute_who_dunit,
			ATT.when_dunit AS attribute_when_dunit
		FROM cv_attribute AS ATT
			JOIN cv_row AS ROW
				JOIN cv_person AS PERSON ON PERSON.id = ROW.person_id
			ON ROW.id = ATT.row_id
			JOIN cv_field AS FIELD
				JOIN cv_affordance_type AS AFF
				ON AFF.id = FIELD.affordance_type_id
				JOIN cv_field_group AS FLDGRP
					JOIN cv_category AS CAT ON CAT.id = FLDGRP.category_id
				ON FLDGRP.id = FIELD.field_group_id
			ON FIELD.id = ATT.field_id
		WHERE PERSON.community = %s AND PERSON.user_id = %s
		AND CAT.code = %s'''
	if isPrintedCV:
		sql = sql + " ORDER BY ROW.id, FIELD.display_on_pdf_seq, FIELD.id"
	else:
		sql = sql + " ORDER BY ROW.id, FIELD.display_on_list_seq, FIELD.id"
	args = (_community,  _username, _categoryName)
	return _dbConnection.executeSQLQuery(sql, args)

def getCVExportDataForUser(_dbConnection, _community, _username):
	sql = '''SELECT
			ROW.id AS row_id,
			ROW.exclude_from_cv_val AS row_exclude_from_cv_val,
			ROW.user_sort_seq AS row_user_sort_seq,
			ROW.who_dunit AS row_who_dunit,
			ROW.when_dunit AS row_when_dunit,
			FIELD.code AS field_code,
			ATT.attribute_value AS attribute_value,
			ATT.who_dunit AS attribute_who_dunit,
			ATT.when_dunit AS attribute_when_dunit
		FROM cv_attribute AS ATT
			JOIN cv_row AS ROW
				JOIN cv_person AS PERSON ON PERSON.id = ROW.person_id
			ON ROW.id = ATT.row_id
			JOIN cv_field AS FIELD ON FIELD.id = ATT.field_id
		WHERE PERSON.community = %s AND PERSON.user_id = %s
		ORDER BY ROW.id, FIELD.seq, FIELD.code, FIELD.id'''
	return _dbConnection.executeSQLQuery(sql, (_community, _username))

def insertRow(_dbConnection, _rowDict, doCommit=True):
	sql = "INSERT INTO cv_row (person_id,exclude_from_cv_val,user_sort_seq,who_dunit,when_dunit) VALUES ((SELECT id FROM cv_person WHERE community = %s AND user_id=%s),%s,%s,%s,%s) RETURNING id"
	args = (_rowDict.get('cvCommunity','default'), _rowDict.get('cvOwnerName',None), _rowDict.get('exclude_from_cv_val',None), _rowDict.get('user_sort_seq',0), _rowDict.get('who_dunit',None), _rowDict.get('when_dunit',None))
	pk = _dbConnection.executeSQLQuery(sql, args)
	return pk

def saveRow(_dbConnection, _rowDict, doCommit=True):
	sql = "UPDATE cv_row SET exclude_from_cv_val=%s,user_sort_seq=%s,who_dunit=%s,when_dunit=%s WHERE id=%s"
	args = (_rowDict.get('exclude_from_cv_val',None), _rowDict.get('user_sort_seq',0), _rowDict.get('who_dunit',None), _rowDict.get('when_dunit',None), _rowDict.get('id',None))
	_dbConnection.executeSQLCommand(sql, args, doCommit)

def deleteRow(_dbConnection, _rowId, doCommit=True):
	sql = '''DELETE FROM cv_row WHERE id=%s'''
	args = (_rowId,)
	return _dbConnection.executeSQLCommand(sql, args, doCommit)

def updateRowSequence(_dbConnection, _rowId, _sequenceNbr, doCommit=True):
	sql = "UPDATE cv_row SET user_sort_seq=%s WHERE id=%s"
	args = (_sequenceNbr, _rowId)
	_dbConnection.executeSQLCommand(sql, args, doCommit)

def insertAttribute(_dbConnection, _attributeDict, doCommit=True):
	sql = "INSERT INTO cv_attribute (row_id,field_id,attribute_value,who_dunit,when_dunit) VALUES (%s,(SELECT id FROM cv_field WHERE code=%s),%s,%s,%s)"
	args = (_attributeDict.get('row_id',None), _attributeDict.get('field_code',None), _attributeDict.get('attribute_value',None), _attributeDict.get('who_dunit',None), _attributeDict.get('when_dunit',None))
	_dbConnection.executeSQLCommand(sql, args, doCommit)

def saveAttribute(_dbConnection, _attributeDict, doCommit=True):
	sql = "UPDATE cv_attribute SET attribute_value=%s,who_dunit=%s,when_dunit=%s WHERE id=%s"
	args = (_attributeDict.get('attribute_value',None), _attributeDict.get('who_dunit',None), _attributeDict.get('when_dunit',None), _attributeDict.get('id',None))
	_dbConnection.executeSQLCommand(sql, args, doCommit)

def deleteAttributesForRow(_dbConnection, _rowId, doCommit=True):
	sql = '''DELETE FROM cv_attribute WHERE row_id=%s'''
	args = (_rowId,)
	return _dbConnection.executeSQLCommand(sql, args, doCommit)

def deleteAttributesForUsername(_dbConnection, _community, _username, doCommit=True):
	sql = '''DELETE FROM cv_attribute WHERE row_id IN (SELECT id FROM cv_row WHERE person_id = (SELECT id FROM cv_person WHERE community = %s AND lower(user_id) = %s))'''
	args = (_community, _username)
	return _dbConnection.executeSQLCommand(sql, args, doCommit)

def deleteRowsForUsername(_dbConnection, _community, _username, doCommit=True):
	sql = '''DELETE FROM cv_row WHERE person_id = (SELECT id FROM cv_person WHERE community = %s AND lower(user_id) = %s)'''
	args = (_community, _username)
	return _dbConnection.executeSQLCommand(sql, args, doCommit)


######################## Pubmed ########################

def createPubImportHeader(_dbConnection,cv_id, now):
	sql = "INSERT INTO cv_publication_import (person_id) VALUES (%s) RETURNING id;"
	args = (cv_id,)
	pk = _dbConnection.executeSQLQuery(sql, args)
	return pk

def importPubMedData(_dbConnection, pub_import_id, cv_id, pubData, now, uid, authorSearchString):
	if not pubMetaDataExists(_dbConnection, cv_id, uid):
		pubData.append(now)
		pubData.append(pub_import_id)
		pubData.append(authorSearchString)
		args = tuple(pubData)
		sqlBuf = []
		sqlBuf.append("INSERT INTO cv_pubmed_import (articleIds,attributes,authors,availablefromurl,bookname,booktitle,chapter,doccontriblist,docdate,doctype,edition,")
		sqlBuf.append("locationid,epubdate,essn,fulljournalname,history,issn,issue,languages,lastauthor,locationlabel,medium,nlmuniqueid,pages,pmcrefcount,publisherlocation,publishername,")
		sqlBuf.append("pubstatus,pubType,recordstatus,reference,reportnumber,sortfirstauthor,sorttitle,source,srcdate,title,uid,vernaculartitle,viewcount,volume,entrywhen,publication_import_id,authorSearchString) VALUES")
		sqlBuf.append("(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
		sql = ''.join(sqlBuf)
		_dbConnection.executeSQLCommand(sql, args, False)
		return True

def pubMetaDataExists(_dbConnection, cv_id, uid):
	sql = '''SELECT COUNT(*) as count FROM cv_pubmed_import,cv_publication_import
	WHERE cv_publication_import.id = cv_pubmed_import.publication_import_id and person_id = %s and uid = %s;'''
	args = (cv_id,uid,)
	result = _dbConnection.executeSQLQuery(sql, args)
	return True if result[0]['count'] > 0 else False

def removePubHeader(_dbConnection,pubimportId):
	sql = "DELETE FROM cv_publication_import WHERE id = %s;"
	args = (pubimportId,)
	_dbConnection.executeSQLCommand(sql, args)

def deletePubmedHeadersForUsername(_dbConnection, _community, _username, doCommit=True):
	sql = "DELETE FROM cv_publication_import WHERE person_id = (SELECT id FROM cv_person WHERE community = %s AND lower(user_id) = %s)"
	args = (_community, _username)
	_dbConnection.executeSQLCommand(sql, args, doCommit)

def deletePubmedPubsForUsername(_dbConnection, _community, _username, doCommit=True):
	sql = '''DELETE FROM cv_pubmed_import WHERE publication_import_id IN (SELECT id FROM cv_publication_import WHERE person_id = (SELECT id FROM cv_person WHERE community = %s AND lower(user_id) = %s))'''
	args = (_community, _username)
	_dbConnection.executeSQLCommand(sql, args, doCommit)

def getPubMedImportedUids(_dbconnection,cv_id):
	sql = '''SELECT uid FROM cv_pubmed_import,cv_publication_import WHERE
	 cv_pubmed_import.publication_import_id = cv_publication_import.id AND
	 cv_publication_import.person_id = %s;'''
	args = (cv_id,)
	return _dbconnection.executeSQLQuery(sql,args)

def getPubMedPublications(_dbconnection,cv_id):
	sql = '''SELECT * FROM cv_pubmed_import,cv_publication_import WHERE
	 cv_pubmed_import.publication_import_id = cv_publication_import.id AND
	 cv_publication_import.person_id = %s ORDER by epubdate ASC;'''
	args = (cv_id,)
	return _dbconnection.executeSQLQuery(sql,args)

def updatePubMedSearchKey(_dbconnection, cv_id, authorsearchkey):
	sql = "UPDATE cv_person SET pubmedsearchkey = %s WHERE id = %s;"
	args = (authorsearchkey,cv_id,)
	_dbconnection.executeSQLCommand(sql,args)

def persistMine(_dbconnection,now,cv_id,mineList):
	for each in mineList:
		sql = '''UPDATE cv_pubmed_import SET claimed = TRUE, reviewed = TRUE, entrywhen = %s,cvpublication_category = %s
		WHERE uid = %s AND publication_import_id IN (SELECT id FROM cv_publication_import WHERE person_id = %s); '''
		args = (now,each.get('pubcat',''),each.get('uid',''),cv_id,)
		_dbconnection.executeSQLCommand(sql,args)

def persistNotMine(_dbconnection,now,cv_id,uidList):
	sql = '''UPDATE cv_pubmed_import SET claimed = FALSE, reviewed = TRUE, entrywhen = %s,cvpublication_category = ''
	WHERE uid IN''' + uidList + " AND publication_import_id IN (SELECT id FROM cv_publication_import WHERE person_id = %s); "
	args = (now,cv_id,)
	_dbconnection.executeSQLCommand(sql,args)

def persistNotReviewed(_dbconnection,now,cv_id,uidList):
	sql = '''UPDATE cv_pubmed_import SET claimed = FALSE, reviewed = FALSE, entrywhen = %s,cvpublication_category = ''
	WHERE uid IN''' + uidList + " AND publication_import_id IN (SELECT id FROM cv_publication_import WHERE person_id = %s); "
	args = (now,cv_id,)
	_dbconnection.executeSQLCommand(sql,args)

def getPubMedImportRow(_dbconnection,uidCode,cv_id):
	sql = '''SELECT * FROM cv_pubmed_import,cv_publication_import WHERE
	 cv_pubmed_import.publication_import_id = cv_publication_import.id AND
	 cv_publication_import.person_id = %s and uid = %s;'''
	args = (cv_id,uidCode)
	return _dbconnection.executeSQLQuery(sql,args)

def removeNonReviewedPubsOnAuthorChange(_dbconnection,authorSearchKey,cv_id):
	sql = '''DELETE FROM cv_pubmed_import WHERE authorsearchstring = %s AND reviewed = FALSE AND publication_import_id IN (SELECT id FROM cv_publication_import WHERE person_id = %s); '''
	args = (authorSearchKey,cv_id,)
	_dbconnection.executeSQLCommand(sql,args)
