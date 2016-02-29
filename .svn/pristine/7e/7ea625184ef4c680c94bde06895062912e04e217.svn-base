# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import re

import MPSAuthSvc.services.abstractService as absService

#   A service for user kweries against the mpsuser table.

class UserSearchService(absService.abstractService):

	#   DOOMED_CHARACTERS
	#       A list of characters that are to be removed from the initial search string
	#   DOOMED_RE
	#   	A compiled RE of doomed characters
	#   SPACE_CHARACTERS
	#   	A list of characters that are to be turned into spaces from the initial search string
	#   SPACE_RE
	#   	A compiled RE of space characters
	#
	#   DEFAULT_SEARCH_COLUMNS
	#   	A list of table columns to be searched

	DOOMED_CHARACTERS = r'[\\!@#$%^&*()_+|={}/<>?":;.]'
	DOOMED_RE = re.compile(DOOMED_CHARACTERS)
	SPACE_CHARACTERS = r'[,]'
	SPACE_RE = re.compile(SPACE_CHARACTERS)

	DEFAULT_SEARCH_COLUMNS = ['username','last_name','first_name']

	def __init__(self, _dbaseUtils=None):
		absService.abstractService.__init__(self, _dbaseUtils)
		self.searchColumns = self.DEFAULT_SEARCH_COLUMNS
		self.offset = 0
		self.limit = 0


	#   Public methods.

	def userSearch(self, _site, _searchCommunity, _searchStr, _limit=0, _offset=0):
		if _limit is not None and \
			type(_limit) == type(1) and \
			_limit > 0:
			self.limit = _limit
		if _offset is not None and \
			type(_offset) == type(1) and \
			_offset > 0:
			self.offset = _offset

		filteredSearchStr = self._filterInput(str(_searchStr))
		qry, parms = self._formSearchQuery(_site, _searchCommunity, filteredSearchStr)
		return self.getDbaseUtils().executeSQLQuery(qry, tuple(parms))

	def userSearchCount(self, _site, _searchStr):
		self.offset = 0
		self.limit = 0
		filteredSearchStr = self._filterInput(str(_searchStr))
		qry, parms = self._formSearchCountQuery(_site, filteredSearchStr)
		countList = self.getDbaseUtils().executeSQLQuery(qry, tuple(parms))
		if countList:
			return countList[0]
		return { 'count': 0 }


	#   Workers.

	def _filterInput(self, _searchStr):
		#   requires a search string
		#   modifies the string to remove the following characters [!,@,#,$,%,^,&,*,(,),_,+,=,{,[,|,\,/,:,;,<,>,.,]}]
		#   modifies the string to turn the following characters [,] into spaces

		return re.sub(self.SPACE_RE, ' ', re.sub(self.DOOMED_RE, '', _searchStr.encode('string-escape'))).lower()

	def _formSearchQuery(self, _site, _searchCommunity, _filteredSearchStr):
		#   requires a filtered search string
		#   splits the string to create multiple search clauses
		#   returns a 2-tuple:
		#	1 - SQL
		#	2 - parameters

		qry, qryParms = self._formQuery(_filteredSearchStr)

		sql = []
		sql.append("SELECT USR.*, COMM.code AS community_code, COMM.descr as community_descr FROM mpsuser AS USR")
		sql.append("JOIN site_community AS COMM ON USR.community_id = COMM.id")
		sql.append("WHERE USR.site_id = (SELECT id FROM site WHERE code = %s)")
		if _searchCommunity:
			sql.append("AND COMM.code = %s")
		if qryParms:
			sql.append("AND")
			sql.append(" AND ".join(qry))
		sql.append("ORDER BY username ASC, last_name ASC, first_name ASC, id ASC")

		if self.limit:
			sql.append("LIMIT %s" % str(self.limit))
		if self.offset:
			sql.append("OFFSET %s" % str(self.offset))

		parms = [_site]
		if _searchCommunity:
			parms.append(_searchCommunity)
		parms.extend(qryParms)

		return (" ".join(sql), parms)

	def _formSearchCountQuery(self, _site, _filteredSearchStr):
		#   requires a filtered search string
		#   splits the string to create multiple search clauses
		#   returns a 2-tuple:
		#	1 - SQL
		#	2 - parameters

		qry, qryParms = self._formQuery(_filteredSearchStr)

		sql = []
		sql.append("SELECT COUNT(*) AS count FROM mpsuser")
		sql.append("WHERE site_id = (SELECT id FROM site WHERE code = %s)")
		if qryParms:
			sql.append("AND")
			sql.append(" AND ".join(qry))

		parms = [_site]
		parms.extend(qryParms)

		return (" ".join(sql), parms)

	def _formQuery(self, _filteredSearchStr):
		searchList = self._formSearchList(_filteredSearchStr)

		qry = []
		parms = []
		for search in searchList:
			where = self._formWhere(search)
			qry.append(where[0])
			parms.extend(where[1])
		return (qry, parms)

	def _formSearchList(self, _filteredSearchStr):
		#   requires a filtered search string
		#   returns a trimmed list of parameters to search

		returnVal=[]
		for s in _filteredSearchStr.split(' '):
			searchStr = s.strip()
			if searchStr: returnVal.append(searchStr)
		return returnVal

	def _formWhere(self, _searchStr):
		#   requires a filtered string with no spaces
		#   returns a 2-tuple:
		#	1 - a partial sql statement
		#		"LOWER(%s) LIKE '%%s%' OR ... OR LOWER(%s) LIKE '%%s%'"
		#	2 - a list of parameters
		#		['clark', 'clark', 'clark']

		orClause = ' OR '.join(["LOWER(%s) LIKE %%s" % search for search in self.searchColumns])
		sql = '(%s)' % orClause.strip()
		parms = ['%%%s%%' % _searchStr for item in self.searchColumns]
		return (sql, parms)
