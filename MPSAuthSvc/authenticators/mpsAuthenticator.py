# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import MPSCore.utilities.stringUtilities as stringUtils
import MPSAuthSvc.authenticators.abstractAuthenticator as absAuthenticator
import MPSAuthSvc.services.userService as userSvc
import MPSCore.utilities.exceptionUtils as excUtils
from MPSCore.utilities.exceptionWrapper import mpsExceptionWrapper

#   MPS Authenticator.

class MpsAuthenticator(absAuthenticator.AbstractAuthenticator):

	#   MPS Authentication.

	@mpsExceptionWrapper("Invalid Username")
	def authenticate(self, _siteProfile, _community, _username, _password):

		#   If password validation is not in effect, let everything pass at this level.
		#   Future code in the Authentication process will validate that the the user
		#   exists in the Authentication database.

		if not self.seeIfPasswordRequired(_siteProfile):
			return self.generateUniqueId()

		#   Find the user record and validate the password.

		site = _siteProfile.get('site', '')
		userDict = userSvc.UserService().getUser(site, _community, _username)
		if userDict:
			storedPassword = userDict.get('password', '')
			if storedPassword:
				givenPassword = stringUtils.encryptValue(_password)
				if storedPassword == givenPassword:
					return self.generateUniqueId()

		raise excUtils.MPSValidationException("Invalid Username")
