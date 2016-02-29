import MPSCore.utilities.dateUtilities as dateUtils

class UberContentMangler:
	def mangleContent(self,_dbConnection,_context,_container,_evaluatorId):
		jobActionDict = _container.workflow.jobActionDict
		proposedStartDate = jobActionDict.get('proposed_start_date','')
		if proposedStartDate:
			localizedDate = dateUtils.localizeUTCDate(proposedStartDate)
			formattedPropStart = dateUtils.parseDate(localizedDate,'%m/%d/%Y')
			newtext = '''Your answers to these questions will be used to evaluate the candidate's <b><u>clinical</u></b>
			competence and qualifications, not his or her research, teaching, or other competence and qualifications,
			which may be different. <b><u>PLEASE RESPOND TO ALL QUESTIONS - YOU MUST HAVE CLINICAL KNOWLEDGE OF THIS APPLICANT IN THE 18 MONTHS PRIOR
			TO %s.</u></b><br/>''' % (formattedPropStart)

			uber = _context.get('uber_instance',{})
			if uber:
				questions = uber.get('questions',{})
				for element in questions.get('elements',{}):
					elementCode = element.get('code','')
					if elementCode == 'CPAHeader':
						element['display_text'] = newtext
			uberContent = _context.get('uberContent',{})
			if uberContent:
				for element in uberContent:
					elementCode = element.get('code','')
					if elementCode == 'CPAHeader':
						element['groupdescr'] = newtext
