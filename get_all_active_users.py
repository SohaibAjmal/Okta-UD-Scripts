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

            response = requests.request("GET", url, headers=headers)

            responseJSON = json.dumps(response.json())

            responseList = json.loads(responseJSON)

            returnResponseList = returnResponseList + responseList
        
            headerLink= response.headers["Link"]

        
        returnJSON = json.dumps(returnResponseList)

        return returnResponseList



def DownloadSFUsers():

    url = "https://"+orgName+".com/api/v1/users"

    responseJSON = GetPaginatedResponse(url)

    if responseJSON != "Error":


        userFile = open("All-Users-In-Okta.csv", "wb")

        writer = csv.writer(userFile)
        
        writer.writerow(["firstName", "lastName", "email", "login"])

        for user in responseJSON:

            firstName  = user[u"profile"][u"firstName"]
            lastName = user[u"profile"][u"lastName"]
            email = user[u"profile"][u"email"]
            login = user[u"profile"][u"login"]

            row = firstName+","+lastName+","+email+","+login
            
            writer.writerow([firstName,lastName,email,login])


if __name__ == "__main__":

    DownloadSFUsers()