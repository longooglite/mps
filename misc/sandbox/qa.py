import sys

#path problems on machine at home
sys.path.append("/Users/ericpaul/CAR/trunk/car")

import MPSCore.utilities.dbConnectionParms as dbConnParms
import MPSAppt.services.qaService as qaSvc
import MPSCore.utilities.sqlUtilities as sqlUtilities

connectionParms = dbConnParms.DbConnectionParms('localhost', 5432, 'mpsdev', 'mps', 'mps')
connection = sqlUtilities.SqlUtilities(connectionParms)

qaSvc = qaSvc.QAService(connection)

try:

	connection.executeSQLCommand("delete from wf_question_response",())

	qas = qaSvc.getQuestionsAndOptionsForTask("RFP")

	qaSvc.saveResponseToOption('RFP','Q00',"Q00_2","Text response to Q00_2")
	qaSvc.saveResponseToOption('RFP','Q00',"Q00_2","Updated response to Q00_2")
	qaSvc.saveResponseToOption('RFP','Q00',"Q00_1","Switch to different prompt")


	#questionsAndAnswers = list of {'taskcode','questioncode','optioncode','textresponse'}
	qaList = []
	qaList.append({"taskcode":"RFP","questioncode":"Q00","optioncode":"Q00_2","textresponse":"response 1"})
	qaList.append({"taskcode":"RFP","questioncode":"Q01","optioncode":"","textresponse":"response 2"})
	qaList.append({"taskcode":"RFP","questioncode":"Q02","optioncode":"","textresponse":"response 3"})
	qaList.append({"taskcode":"RFP","questioncode":"Q03","optioncode":"Q03_2","textresponse":"response 4"})
	qaList.append({"taskcode":"RFP","questioncode":"Q04","optioncode":"Q04_1","textresponse":"response 5"})
	qaList.append({"taskcode":"RFP","questioncode":"Q05","optioncode":"Q05_1","textresponse":"response 6"})
	qaSvc.saveResponsesToOptions(qaList)

	qaList = []
	qaList.append({"taskcode":"RFP","questioncode":"Q00","optioncode":"Q00_2","textresponse":"response 1 updated"})
	qaList.append({"taskcode":"RFP","questioncode":"Q01","optioncode":"","textresponse":"response 2 updated"})
	qaList.append({"taskcode":"RFP","questioncode":"Q02","optioncode":"","textresponse":"response 3 updated"})
	qaList.append({"taskcode":"RFP","questioncode":"Q03","optioncode":"Q03_2","textresponse":"response 4 updated"})
	qaList.append({"taskcode":"RFP","questioncode":"Q04","optioncode":"Q04_1","textresponse":"response 5 updated"})
	qaList.append({"taskcode":"RFP","questioncode":"Q05","optioncode":"Q05_1","textresponse":"response 6 updated"})
	qaSvc.saveResponsesToOptions(qaList)

except Exception,e:
	pass