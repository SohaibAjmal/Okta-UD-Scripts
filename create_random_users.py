import requests
import json
import re
import sys
import csv

orgName = ""
apiKey = ""

def CreateUsers():

	N  = 3

	firstName = "OktaSupp"
	lastName = "TestUser"

	## CSV file before user is created

	beforeCreation = open("User-Info-Before-Creation.csv", "wb")
	beforeWriter = csv.writer(beforeCreation)

	beforeWriter.writerow(["firstName", "lastName", "email", "login"])

	afterCreation = open("User-Info-After-Creation.csv", "wb")
	afterWriter = csv.writer(afterCreation)
	afterWriter.writerow(["id", "status", "email","Okta-Request-Id"])

	for userNum in range(1, N):
		
		try:
			
			email = firstName.lower()+str(userNum)+lastName.lower()+str(userNum)+"@mailinator.com"

			## First name of the user
			print "\n Creating User " + email + "\n"

			#Write to CSV before creating
			beforeWriter.writerow([firstName,lastName,email,email])
				

			user_info = {}
			
			user_info['profile'] = {}
			user_info['credentials'] = {}

			user_info['profile'] ['firstName'] = firstName+str(userNum)
			user_info['profile'] ['lastName'] = lastName+str(userNum)
			user_info['profile'] ['email'] = email
			user_info['profile'] ['login'] = email

			user_info['credentials'] ['password'] = {}
			user_info['credentials'] ['recovery_question'] = {}

			user_info['credentials'] ['password']['value'] = ""
			user_info['credentials']['recovery_question'] ['question'] = "Who's a major player"
			user_info['credentials']['recovery_question'] ['answer'] = ""
			
			user_info_json = json.dumps(user_info)
			
			url = "https://"+orgName+".com/api/v1/users"

			api_token = "SSWS "+ apiKey
			headers = {'Accept':'application/json','Content-Type':'application/json','Authorization':api_token}
			
			print user_info
			response = requests.post(url, data = user_info_json, headers = headers)

			responseJSON = response.json()

			##Read headers
			oktaRequestId= response.headers["X-Okta-Request-Id"]

			if "errorCode" in  responseJSON:
				

				print responseJSON

			else:

				userId = responseJSON["id"]
				status = responseJSON["status"]
				userEmail = responseJSON["profile"]["email"]



				#Write to CSV after creating
				afterWriter.writerow([userId,status,email,oktaRequestId])

				print "\n User " + email + " Created Successfully"

		except:

			print "Unexpected error:", sys.exc_info()
			print "\n"
			pass

if __name__ == "__main__":
	CreateUsers()


