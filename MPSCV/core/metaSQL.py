# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

def getAllCategories(_dbConnection):
	sql = '''SELECT * FROM cv_category ORDER BY seq'''
	return _dbConnection.executeSQLQuery(sql)

def getSpecificCategories(_dbConnection, _inCodeClause):
	sql = '''SELECT * FROM cv_category WHERE code IN %s ORDER BY seq;''' % (_inCodeClause)
	return _dbConnection.executeSQLQuery(sql)

def getOneCategory(_dbConnection, _category):
	sql = '''SELECT * FROM cv_category WHERE code = %s'''
	return _dbConnection.executeSQLQuery(sql, (_category,))

def getSubCategoriesForCategory(_dbConnection, _categoryCode):
	sql = '''SELECT
			GRP.id AS group_id,
			GRP.code AS group_code,
			GRP.descr AS group_descr,
			GRP.seq AS group_seq,
			SUBCAT.id AS id,
			SUBCAT.code AS code,
			SUBCAT.descr AS descr,
			SUBCAT.seq AS seq
		FROM cv_sub_category AS SUBCAT
			JOIN cv_sub_category_group AS GRP
				JOIN cv_category AS CAT ON CAT.id = GRP.category_id
			ON GRP.id = SUBCAT.sub_category_group_id
		WHERE CAT.code = %s
		ORDER BY SUBCAT.seq, SUBCAT.id'''
	args = (_categoryCode,)
	return _dbConnection.executeSQLQuery(sql, args)

def getSubCategoriesByGroupForCategory(_dbConnection, _categoryCode):
	sql = '''SELECT
			CAT.id AS category_id,
			CAT.code AS category_code,
			CAT.descr AS category_descr,
			CAT.seq AS category_seq,
			CAT.parent_code AS category_parent_code,
			CAT.exclude_from_cv_display AS category_exclude_from_cv_display,
			CAT.user_sortable AS category_user_sortable,
			CAT.display_options AS category_display_options,
			CAT.help_text AS category_help_text,
			MODE.id AS mode_id,
			MODE.code AS mode_code,
			MODE.descr AS mode_descr,
			GRP.id AS group_id,
			GRP.code AS group_code,
			GRP.descr AS group_descr,
			GRP.seq AS group_seq,
			SUBCAT.id AS subcat_id,
			SUBCAT.code AS subcat_code,
			SUBCAT.descr AS subcat_descr,
			SUBCAT.seq AS subcat_seq
		FROM cv_sub_category AS SUBCAT
			JOIN cv_sub_category_group AS GRP
				JOIN cv_category AS CAT
					JOIN cv_display_mode AS MODE ON MODE.id = CAT.list_display_mode_id
				ON CAT.id = GRP.category_id
			ON GRP.id = SUBCAT.sub_category_group_id
		WHERE CAT.code = %s
		ORDER BY GRP.seq, SUBCAT.seq'''
	args = (_categoryCode,)
	return _dbConnection.executeSQLQuery(sql, args)

def getParentCategories(_dbConnection):
	sql = '''SELECT * FROM cv_category WHERE code IN (SELECT distinct parent_code FROM cv_category WHERE parent_code <> '');'''
	args = ()
	return _dbConnection.executeSQLQuery(sql, args)

def getFieldsForCategory(_dbConnection, _categoryCode, _orderFor='LIST'):
	sql = '''SELECT
			CAT.id AS category_id,
			CAT.code AS category_code,
			CAT.descr AS category_descr,
			CAT.seq AS category_seq,
			CAT.parent_code AS category_parent_code,
			CAT.exclude_from_cv_display AS category_exclude_from_cv_display,
			CAT.user_sortable AS category_user_sortable,
			CAT.display_options AS category_display_options,
			CAT.help_text AS category_help_text,
			MODE.id AS mode_id,
			MODE.code AS mode_code,
			MODE.descr AS mode_descr,
			GRP.id AS group_id,
			GRP.code AS group_code,
			GRP.descr AS group_descr,
			GRP.seq AS group_seq,
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
			AFF.descr as affordance_descr
		FROM cv_field AS FIELD
			JOIN cv_field_group AS GRP
				JOIN cv_category AS CAT
					JOIN cv_display_mode AS MODE ON MODE.id = CAT.detail_display_mode_id
				ON CAT.id = GRP.category_id
			ON GRP.id = FIELD.field_group_id
			JOIN cv_affordance_type AS AFF
			ON AFF.id = FIELD.affordance_type_id
		WHERE CAT.code = %s '''

	if _orderFor.upper() == 'LIST':
		finalSql =  sql + '''ORDER BY FIELD.display_on_list_seq, FIELD.seq'''
	elif _orderFor.upper() == 'PDF':
		finalSql =  sql + '''ORDER BY FIELD.display_on_pdf_seq, FIELD.seq'''
	else:   # order for Detail
		finalSql =  sql + '''ORDER BY GRP.seq, FIELD.seq'''

	args = (_categoryCode,)
	return _dbConnection.executeSQLQuery(finalSql, args)

def getAllFields(_dbConnection):
	sql = '''SELECT * FROM cv_field'''
	return _dbConnection.executeSQLQuery(sql)

def getStaticLookupData(_dbConnection,static_lookup_code):
	args = (static_lookup_code,)
	sql = '''SELECT id,code,descr,alt_descr FROM cv_static_lookup WHERE lookup_key = %s ORDER BY seq;'''
	return _dbConnection.executeSQLQuery(sql,args)

def getSelectorCache(_dbConnection):
	sql = '''SELECT cv_selector_group.code as group_code,
		cv_selector_group.descr as group_descr,
		cv_selector.code,
		cv_selector.descr,
		cv_selector.style,
		cv_selector.seq
		FROM cv_selector_group,cv_selector
		WHERE cv_selector.cv_selector_group_id = cv_selector_group.id ORDER BY seq;'''
	args = ()
	rawqry = _dbConnection.executeSQLQuery(sql,args)
	cache = {}
	currentGroupIdentifier = ''
	for row in rawqry:
		if currentGroupIdentifier <> row.get('group_code',''):
			currentGroupIdentifier = row.get('group_code','')
			cache[currentGroupIdentifier] = []
		cache[currentGroupIdentifier].append({"val":row.get('code',''),"name":row.get('descr',''),"style":row.get('style',''),"seq":row.get('seq','')})
	return cache
