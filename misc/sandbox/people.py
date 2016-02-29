import MPSAppt.services.personalInfoService as personSvc
import MPSCore.utilities.dbConnectionParms as dbConnParms
import MPSCore.utilities.sqlUtilities as sqlUtilities
import MPSAppt.services.jobActionService as jaService
import MPSAppt.services.workflowService as wfSvc

peronalInfoDict = {}

peronalInfoDict['id'] = 3

peronalInfoDict['user_name'] = 'ttttt'
peronalInfoDict['first_name'] = 'ttttt'
peronalInfoDict['last_name'] = 'uuuuu'
peronalInfoDict['suffix'] = 'Jr.'
peronalInfoDict['middle_name'] = 'Manning'
peronalInfoDict['email'] = 'eeee@eee.com'
peronalInfoDict['employee_nbr'] = '22122zzz'
peronalInfoDict['birth_date'] = '1981-09-01'
peronalInfoDict['birth_country'] = 'US'
peronalInfoDict['birth_state'] = 'MI'
peronalInfoDict['gender'] = 'M'
peronalInfoDict['us_citizen'] = 'y'
peronalInfoDict['living_in_us'] = 'n'
peronalInfoDict['has_ssn'] = '1'
peronalInfoDict['ssn'] = '222-22-2222'
peronalInfoDict['ethnicity'] = 'latino'
peronalInfoDict['scholarly_focus'] = 'medicine'
peronalInfoDict['aliases'] = ['Arnold','Butch']
peronalInfoDict['languages'] = ['Dutch','French']
peronalInfoDict['address_line1'] = '1003 Brooks Street'
peronalInfoDict['address_line2'] = 'Box A'
peronalInfoDict['address_line3'] = '2nd drive'
peronalInfoDict['address_line4'] = 'on right'
peronalInfoDict['address_city'] = 'Ann Arbor'
peronalInfoDict['address_state'] = 'MI'
peronalInfoDict['address_country'] = 'US'
peronalInfoDict['address_postal'] = '48103'
peronalInfoDict['address_home_phone'] = '999-222-1111'
peronalInfoDict['address_cell_phone'] = '888-222-1111'
peronalInfoDict['address_fax'] = '777-222-1111'
peronalInfoDict['hd_program'] = 'educational'
peronalInfoDict['hd_degree'] = 'PhD'
peronalInfoDict['hd_institution'] = 'UoM'
peronalInfoDict['hd_country'] = 'Peru'
peronalInfoDict['hd_state'] = 'Peruvian Jungle'
peronalInfoDict['hd_city'] = 'Akron'
peronalInfoDict['hd_name'] = 'Mike'
peronalInfoDict['hd_start'] = '2014-01-02'
peronalInfoDict['hd_end'] = '2015-03-12'
peronalInfoDict['completed'] = 'false'
peronalInfoDict['name_match'] = 'yes'
peronalInfoDict['created'] = '2015-03-12'
peronalInfoDict['updated'] = '2015-03-12'
peronalInfoDict['lastuser'] = 'eric'

personDict = {}
personDict['id'] = 1
personDict['user_name'] = 'zPaulezzz'
personDict['first_name'] = 'zErticzzz'
personDict['last_name'] = 'zPaul'
personDict['suffix'] = 'zJr.'
personDict['middle_name'] = 'zManning'
personDict['email'] = 'zeeee@zeee.com'
personDict['employee_nbr'] = 'z22122'
personDict['created'] = '2015-03-12'
personDict['updated'] = '2015-03-12'
personDict['lastuser'] = 'eric'



connectionParms = dbConnParms.DbConnectionParms('localhost', 5432, 'mpsdev', 'mps', 'mps')
connection = sqlUtilities.SqlUtilities(connectionParms)


task_code = 'bib_notes'

jService = jaService.JobActionService(connection)
jobAction = jService.getJobAction(3)
workflow = wfSvc.WorkflowService(connection).getWorkflowForJobAction(jobAction, {})
container = workflow.getContainer(task_code)
now = '2015-09-09 12:00:00'

taskDict = {}
taskDict['job_action_id'] = 3
taskDict['task_code'] = task_code
taskDict['created'] = now
taskDict['updated'] = now
taskDict['lastuser'] = 'eric'

#jService.createJobTask(taskDict)
jobTask = jService.getJobTask(jobAction,container)

personalInfoService = personSvc.PersonalInfoService(connection)
personalInfoService.handleSubmit(jobAction,jobTask,personDict,peronalInfoDict,container,now,'eric')
pinfo = personalInfoService.getPersonalInfo(jobTask)
x=1
