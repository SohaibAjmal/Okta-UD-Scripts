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


def GETRequest(url):

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


def PUTRequest(url, data):

    if data != "":

        response = requests.put(url, data= data, headers=headers)

    else:

        response = requests.put(url, headers=headers)

    
    responseJSON = response.json()
    
    if "errorCode" in responseJSON:

        print "\nYou encountered following Error: \n"
        print responseJSON
        print "\n"

        return "Error"

    else:

        return response.json()

def DELETERequest(url):

    response = requests.delete(url, headers=headers)

    responseJSON = response.json()

    if "errorCode" in responseJSON:
        print "\nYou encountered following Error: \n"
        print responseJSON
        print "\n"

        return "Error"

    else:

        return responseJSON



def UDOperation():

    url = "https://"+orgName+".com/api/v1/users"

    # Get paginated response
    userList = GetPaginatedResponse(url)
    

    # Send a delete request e.g. Remove a user from app 

    #url = "https://"+orgName+".com/api/v1/apps/{{appId}}/users/{{userId}}

    #DeleteRequest(url):

    # Send a Post request e.g. Create a user

    #url = "https://"+orgName+".com/api/v1/users

    #PostRequest(url):

   


if __name__ == "__main__":

	UDOperation()