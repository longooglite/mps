# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import hashlib
import re


#   Various string-related utilities.

def interpretAsTrueFalse(_string):

	#   Returns True  iff the given _string should be interpreted as a 'true' condition.
	#   Returns False otherwise.

	if _string:
		if type(_string) is bool:
			return _string
		stringUC = _string.upper()
		if stringUC.startswith('1'): return True
		if stringUC.startswith('T'): return True
		if stringUC.startswith('Y'): return True
		if stringUC.startswith('ON'): return True
	return False

def encryptValue(_value):
	#   Encrypts the given value and returns the result.
	valu = hashlib.sha256()
	valu.update(_value)
	return valu.hexdigest()

def squeeze(_value):
	"""Replace all sequences of whitespace chars with a single space."""
	return re.sub(r"[\x00-\x20]+", " ", _value).strip()

def constructFullName(_firstName, _lastName, _middleName = '', _suffix = ''):
	firstName = _firstName.strip() if _firstName else ''
	lastName = _lastName.strip() if _lastName else ''
	middleName = _middleName.strip() if _middleName else ''
	suffix = _suffix.strip() if _suffix else ''
	name = firstName.strip()
	if middleName:
		name += " %s" % (middleName)
	if lastName:
		name += " %s" % (lastName)
	if suffix:
		name += " %s" % (suffix)
	return name

def constructLastCommaFirstName(_firstName, _lastName, _middleName = '', _suffix = ''):
	firstName = _firstName.strip() if _firstName else ''
	lastName = _lastName.strip() if _lastName else ''
	middleName = _middleName.strip() if _middleName else ''
	suffix = _suffix.strip() if _suffix else ''
	partsList = []
	if lastName and suffix: partsList.append("%s %s" % (lastName.strip(),suffix.strip()))
	elif lastName: partsList.append(lastName)
	if firstName and middleName: partsList.append("%s %s" % (firstName.strip(),middleName.strip()))
	elif firstName: partsList.append(firstName)
	return ", ".join(partsList)

def constructLastCommaFirstNameTheStoopidWay(_firstName, _lastName, _middleName = '', _suffix = ''):
	firstName = _firstName.strip() if _firstName else ''
	lastName = _lastName.strip() if _lastName else ''
	middleName = _middleName.strip() if _middleName else ''
	suffix = _suffix.strip() if _suffix else ''
	partsList = []
	if lastName: partsList.append(lastName.strip())
	if firstName: partsList.append(firstName.strip())
	if middleName: partsList.append(middleName.strip())
	if suffix: partsList.append(suffix.strip())
	return ", ".join(partsList)

def constructLastNamePossessive(_lastName):
	if _lastName.upper().endswith('S'):
		return _lastName + "'"
	return _lastName + "'s"

def constructCityStatePostal(_city, _state, _postal):
	city = _city or ''
	state = _state or ''
	postal = _postal or ''
	statePostal = ("%s %s" % (state.strip(), postal.strip())).strip()
	city = city.strip()
	if city:
		if statePostal:
			return ", ".join([city, statePostal])
		return city
	return statePostal


def getSQLInClause(attributeList, quoted = True):
	returnVal = "("
	for each in attributeList:
		if quoted:
			returnVal += "'%s'," % str(each)
		else:
			returnVal += str(each) + ","

	if returnVal <> "(":
		returnVal = returnVal[0:len(returnVal)-1] + ")"
	else:
		returnVal = ""
	return returnVal

def getSQLInClauseFromDictList(attributeList, key, quoted = True):
	returnVal = "("
	for each in attributeList:
		value = each.get(key,'')
		if quoted:
			returnVal += "'%s'," % str(value)
		else:
			returnVal += str(value) + ","

	if returnVal <> "(":
		returnVal = returnVal[0:len(returnVal)-1] + ")"
	else:
		returnVal = ""
	return returnVal


def maskString(maskStr,maskLength=4):
	strlen = len(maskStr)
	charList = []
	if strlen > maskLength:
		charList = list(maskStr)
		i = 0
		while i < strlen-maskLength:
			charList[i] = '*'
			i+=1
	return ''.join(charList)


def getDataTypeAttributeValueForKey(_dtAttributeStr, _keyStr, _defaultValue=None, _isBoolean=False, _delimiters=[' ', ',']):

	#   Returns the value associated with _keyStr in the given Data Attributes string, _dtAttributeStr.
	#   _defaultValue is returned if _keyStr is not found in _dtAttributeStr.
	#   If the optional _isBoolean arg is set, then True or False is returned instead of the raw string
	#   value according to the rules in the interpretAsTrueFalse(_string) method above.
	#
	#   Data Type Attributes (used in Appointments Uberforms) may contain multiple entries.
	#   The initial use of this feature is for Uberform Date fields, which may (optionally) contain
	#   configuration settings for the accepted date format, a restriction that a date must be on or
	#   after a specified date, and whether or not to allow future dates. This convention can be
	#   extended to other Uberform data types of other applications as necessary.
	#
	#   Settings are delimited by either space or comma (space is preferred).
	#   Within a setting, the key and the associated value are separated by a colon (':') character.
	#
	#   Example:
	#       format:M/D/Y after:BC_START future:false

	keyStr = _keyStr.strip()
	attrStr = _dtAttributeStr.strip()
	if (not keyStr) or (not attrStr) or (not _delimiters):
		return _defaultValue

	keyStrUC = keyStr.upper()
	attrStrUC = attrStr.upper()
	if keyStrUC not in attrStrUC:
		return _defaultValue

	keyStrUCPlusColon = keyStrUC + ':'
	for delimiter in _delimiters:
		splitsUC = attrStrUC.split(delimiter)
		idx = 0
		for each in splitsUC:
			if each.startswith(keyStrUCPlusColon):
				splits = attrStr.split(delimiter)
				matchedSplit = splits[idx]
				value = matchedSplit[len(keyStrUCPlusColon):]
				if _isBoolean:
					return interpretAsTrueFalse(value)
				return value
			idx += 1

	return _defaultValue
