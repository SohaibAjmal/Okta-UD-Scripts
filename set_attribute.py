import requests
import json
import re
import sys
import csv


orgName = ""

apiKey = ""

# Attribute name you want to set for all users
attributeName  = "setCustomBool"


# Attribute value to be set
attributeValue = False


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

def GetObject(url):

	response = requests.request("GET", url, headers=headers)
	
	responseJSON = response.json()

	if "errorCode" in responseJSON:
		print "\nYou encountered following Error: \n"
		print responseJSON
		print "\n"

		return "Error"

	else:

		return response.json()


def POSTRequest(url, data):

	if data != "":

		response = requests.post(url, data= data, headers=headers)

	else:

		response = requests.post(url, headers=headers)

	
	responseJSON = response.json()
	if "errorCode" in responseJSON:

		print "\nYou encountered following Error: \n"
		print responseJSON
		print "\n"

		return "Error"

	else:

		return response.json()

def SetAttribute():

    userSchemaUrl = "https://"+orgName+".com/api/v1/meta/schemas/user/default"

    userSchema = GetObject(userSchemaUrl)

    baseAttributesList =  userSchema["definitions"]["base"]["properties"]

    customAttributesList =  userSchema["definitions"]["custom"]["properties"]

    if attributeName in baseAttributesList or attributeName in customAttributesList:

    	listUserUrl = "https://"+orgName+".com/api/v1/users"

    	userList = GetPaginatedResponse(listUserUrl)

    	count = 1

    	for user in userList:

    		userId = user["id"]

    		userUrl = "https://"+orgName+".com/api/v1/users/"+ str(userId)

    		user_info = {}

    		user_info['profile'] = {}

    		user_info['profile'] [attributeName] = attributeValue

    		user_info_json = json.dumps(user_info)

    		response = POSTRequest(userUrl, user_info_json)

    		if response != "Error":

    			print "Attribue " + attributeName + " Set to " + str(attributeValue) + " for " + str(user["profile"]["firstName"]) + " " +  str(user["profile"]["lastName"]) + " " + str(count)

    		print "\n \n"

    		count += 1

    else:

    	print "Attribue " + attributeName + " Not Found in User Schema. Please Create and Try Again."


if __name__ == "__main__":

	SetAttribute()