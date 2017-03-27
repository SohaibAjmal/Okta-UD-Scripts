import requests
import json
import re
import sys
import csv

orgName = ""
apiKey = ""

api_token = "SSWS "+ apiKey

headers = {'Accept':'application/json','Content-Type':'application/json','Authorization':api_token}

def GetPaginatedResponse(url):

    response = requests.request("GET", url, headers=headers)

    returnResponseList = []

    responseJSON = json.dumps(response.json())

    responseList = json.loads(responseJSON)

    returnResponseList = returnResponseList + responseList


    if "errorCode" in responseJSON:

        print "\nYou encountered following Error: \n"
        print responseJSON
        print "\n"

        return "Error"

    else:

        headerLink= response.headers["Link"]
        
        count = 1
  
        while str(headerLink).find("rel=\"next\"") > -1:

            linkItems = str(headerLink).split(",")

            nextCursorLink = ""
            for link in linkItems:

                if str(link).find("rel=\"next\"") > -1:
                    nextCursorLink = str(link)


            nextLink = str(nextCursorLink.split(";")[0]).strip()
            nextLink = nextLink[1:]
            nextLink = nextLink[:-1]

            url = nextLink

            print "\nCalling Paginated Url " + str(url) + "  " + str(count) +  " \n"
            response = requests.request("GET", url, headers=headers)

            responseJSON = json.dumps(response.json())

            responseList = json.loads(responseJSON)

            returnResponseList = returnResponseList + responseList
        
            headerLink= response.headers["Link"]

            count += 1

        
        returnJSON = json.dumps(returnResponseList)

        return returnResponseList

def ActivateUser(url):

	response = requests.post(url, headers=headers)
	
	responseJSON = response.json()

	if "errorCode" in responseJSON:
		print "\nYou encountered following Error: \n"
		print responseJSON
		print "\n"

		return "Error"

	else:

		return responseJSON



def UpdateAssignment():


    getStagedUsersUrl = "https://"+orgName+".com/api/v1/users?filter=status eq \"STAGED\""

    stagedUsers = GetPaginatedResponse(getStagedUsersUrl)

    count = 1

    for stagedUser in stagedUsers:

        userId = str(stagedUser[u"id"])

        print "Activating " + stagedUser[u"profile"][u"firstName"] + " " + stagedUser[u"profile"][u"lastName"] + stagedUser[u"profile"][u"login"] + " " + str(count) 

        acticvateUserUrl = "https://"+orgName+".com/api/v1/users/" + userId + "/lifecycle/activate?sendEmail=false"


        activationResponse = ActivateUser(acticvateUserUrl)

        if "Error" != activationResponse:

            print stagedUser[u"profile"][u"firstName"] + " " + stagedUser[u"profile"][u"lastName"] + stagedUser[u"profile"][u"login"] + " ACTIVATED\n"

        count += 1

 
   


if __name__ == "__main__":

	UpdateAssignment()