# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

# Greg's LDAP test program

import ldap
import datetime

# CMU
def cmu():
	ldapConnection = ldap.initialize('ldaps://centraldc01.central.cmich.local:636/')
	ldapConnection.set_option(ldap.OPT_REFERRALS, 0)
	print datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
	result = ldapConnection.simple_bind_s('cn=mpldap,cn=users,dc=central,dc=cmich,dc=local','4/&AB7CzA/T4')
	#result = ldapConnection.simple_bind_s('','')
	import pprint;pprint.pprint(result)
	#r2 = ldapConnection.search_s('cn=bell2hj,cn=users,dc=central,dc=cmich,dc=local',ldap.SCOPE_BASE,attrlist=['displayName'])
	#r2 = ldapConnection.search_s('cn=nahat1bl,cn=users,dc=central,dc=cmich,dc=local',ldap.SCOPE_BASE,attrlist=['displayName'])
	r2 = ldapConnection.search_s('cn=nahat1bl,cn=users,dc=central,dc=cmich,dc=local',ldap.SCOPE_BASE)
	import pprint;pprint.pprint(r2)
	if r2:
		import pprint;pprint.pprint(r2[0][1])


# MPS
def mps():
#	ldapConnection = ldap.initialize('ldap://ldap.mntnpass.com:389/')
	ldapConnection = ldap.initialize('ldap://10.64.139.145:389/')
	ldapConnection.set_option(ldap.OPT_REFERRALS, 0)
	print datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
	result = ldapConnection.simple_bind_s('uid=mpssearch,ou=users,dc=mntnpass,dc=com','search')
	import pprint;pprint.pprint(result)
	r2 = ldapConnection.search_s('uid=ggg,ou=users,dc=mntnpass,dc=com', ldap.SCOPE_BASE)
	import pprint;pprint.pprint(r2)


# Oakland University
def oakland():
	ldapConnection = ldap.initialize('ldaps://ldap.oakland.edu:636/')
	ldapConnection.set_option(ldap.OPT_REFERRALS, 0)
	print datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
	result = ldapConnection.simple_bind_s('uid=bindmountainpass, dc=oakland, dc=edu','L!GK4Y8rEuLwbXeCaPRV6$')
	import pprint;pprint.pprint(result)
	r2 = ldapConnection.search_s('uid=bindmountainpass, dc=oakland, dc=edu', ldap.SCOPE_BASE)
	import pprint;pprint.pprint(r2)


# University of Michigan - College of Engineering
def umEng():
	ldapConnection = ldap.initialize('ldaps://ldap.umich.edu:636/')
	ldapConnection.set_option(ldap.OPT_REFERRALS, 0)
	print datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
	result = ldapConnection.simple_bind_s('uid=bindmountainpass,ou=People,dc=umich,dc=edu','WeHaveNoPasswordYet')
	import pprint;pprint.pprint(result)
	r2 = ldapConnection.search_s('uid=kingch,ou=People,dc=umich,dc=edu', ldap.SCOPE_BASE)
	import pprint;pprint.pprint(r2)

#cmu()
#mps()
#oakland()
#umEng()
