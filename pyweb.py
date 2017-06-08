import web
import sys
import traceback

from userStory06.dwp_service_S1KA import dwp_service_S1KA
from userStory11.dwp_service_S1CB2 import dwp_service_S1CB2
from userStory02.dwp_serviceTower import dwp_serviceTower
from analytics import analytics

urls = (

'/dwp_S1KA', 'dwp_S1KA',
'/dwp_S1CB2', 'dwp_S1CB2',
'/dwp_service_Tower', 'dwp_service_Tower'

)

app = web.application(urls, globals())

# dwp
class dwp_S1KA:
	


	def __init__(self):
		print "dwp init"

		# get
	def GET(self):
		try:
			web.header('Content-Type', 'application/json')
			# read description
			user_query = web.input(description='')
			print user_query

			# model predict
			d = dwp_service_S1KA()
			output = d.modelPredict(user_query.description, "USR-3JP5U")
		except:
			traceback.print_exc()			
			output = 'Exception: No query passed'
			print output

		return output

	# post
	def POST(self):
		print('KA Matching Initiated')
		import json	
		try:
			web.header('Content-Type', 'application/json')
			print web.data()
			# read json incident no, Description
			data = json.loads(unicode(web.data(),errors='ignore'))
			user_query = ""
			incident_no = ""
			application_name = ""
			sys_id = ""
			state_id = ""
			notes_query = ""
			output = ""
			ka_number = ""

			for i in data:
				user_query = i["Description"]
				print "User Description is " + user_query
				incident_no = i["Number"]
				print "Incident Number is " + incident_no
				application_name = i["applicationName"]
				print "Application Name is " + application_name
				sys_id = i['ID']
				print 'SYS ID is ' + sys_id
				state_id = i["state"]
				print "State is  " + state_id
				notes_query = i['comments']
				print 'Notes is ' + notes_query
				for j in i["ka"]:
					ka_number = j
				if state_id == '4':
				# model predict 1-New 2-In Progress 3-Awaiting User Info 4-Missing User Info 5-Awaiting Vendor 6-Resolved 7-Closed 
					d = dwp_service_S1KA()
					#output = d.modelPredict(user_query, incident_no, application_name, sys_id)
					d.validate(user_query, incident_no, application_name, sys_id, notes_query)
				if state_id == '6':
					d = dwp_service_S1KA()
					output = d.statePredict(notes_query, state_id, sys_id, user_query, ka_number, application_name, incident_no)
		except:
			traceback.print_exc()		
			output = 'Exception: No query passed'
			print output

		return output

class dwp_S1CB2:
	

	#def GET(self):
	#print "get"
	#return "success"

	# post
	def POST(self):
		print('Triage Initiated')
		
		import json	
		try:
			web.header('Content-Type', 'application/json')
			print web.data()
			# read json applicationName, shortDescription
			data = json.loads(unicode(web.data(),errors='ignore'))
			user_query = ""
			incident_no = ""
			application_name = ""
			sys_id = ''
			for i in data:
				user_query = i["Description"]
				application_name = i["applicationName"]
				incident_no = i["Number"]
				sys_id = i['ID']
				print "User Description Is " + user_query
				print "Incident Number Is " + incident_no
				print 'SYS ID Is ' + sys_id
			cb = ''
			if application_name == 'PTP CAM':
				cb = 'CB1'	
			elif application_name == 'ESA CAM':
				cb = 'CB2'

			usr = cb + " " + user_query 
			# model predict
			d = dwp_service_S1CB2()
			output = d.modelPredict(usr, incident_no, sys_id)
		except:
			traceback.print_exc()		
			output = 'Exception: No query passed'
			print output

		return output		

class dwp_service_Tower:
	print('python web for dwp service called')

	#def GET(self):
	#print "get"
	#return "success"

	# post
	def POST(self):
		import json	
		try:
			web.header('Content-Type', 'application/json')
			print web.data()
			# read json applicationName, shortDescription
			data = json.loads(unicode(web.data(),errors='ignore'))
			user_query = ""
			incident_no = ""
			application_name = ""
			sys_id = ''
			for i in data:
				user_query = i["Description"]
				application_name = i["applicationName"]
				incident_no = i["Number"]
				sys_id = i['ID']
				print "User Description Is " + user_query
				print "Incident Number Is " + incident_no
				print 'SYS ID Is ' + sys_id
			resv = ''
			if application_name == 'PTP CAM':
				resv = 'HP-PTP'	
			elif application_name == 'ESA CAM':
				resv = 'HP-ESA'

			usr = resv + " " + user_query 
			# model predict
			d = dwp_serviceTower()
			output = d.modelPredict(usr, incident_no, sys_id)
		except:
			traceback.print_exc()		
			output = 'Exception: No query passed'
			print output

		return output		


if __name__ == "__main__":
	app.run()