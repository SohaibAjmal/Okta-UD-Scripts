import requests
import json
import re
import sys
import csv
import openpyxl


reload(sys)
sys.setdefaultencoding('utf-8')

orgName = "org-domain.oktapreview"
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



def DELETERequest(url):

    response = requests.delete(url, headers=headers)

    responseJSON = response

    if "errorCode" in responseJSON:
        print "\nYou encountered following Error: \n"
        print responseJSON
        print "\n"

        return "Error"

    else:

        return responseJSON


def DeleteUsers():


    ##### CSV Files #####

     # Deactive Users
    deactiveUsers = open("Deactive-Users.csv", "wb")

    deactiveWriter = csv.writer(deactiveUsers)
    
    deactiveWriter.writerow(["firstName", "lastName", "email", "login", "status"])

    #Deleted Users
    deletedUsers = open("Deleted-Users.csv", "wb")

    deletedWriter = csv.writer(deletedUsers)
    
    deletedWriter.writerow(["firstName", "lastName", "email", "login", "status"])

     #Not Deleted Users
    notDeletedUsers = open("Not-Deleted-Users.csv", "wb")

    notDeletedWriter = csv.writer(notDeletedUsers)
    
    notDeletedWriter.writerow(["firstName", "lastName", "login", "error"])

    ##### CSV Files #####

    url = "https://"+orgName+".com/api/v1/users?filter=status eq \"DEPROVISIONED\""

    deactivedUsers = GetPaginatedResponse(url)

    userInfoList = []

    deactivedUsersCount = 0
    deletedUsersCount = 0
    notDeletedUserCount = 0

    for user in deactivedUsers:

        userId = str(user["id"])

        deleteUrl = "https://"+orgName+".com/api/v1/users/"+userId

        deactiveWriter.writerow([user["profile"]["firstName"], user["profile"]["lastName"], user["profile"]["email"], user["profile"]["login"], user["status"]])
        deactivedUsersCount += 1

        response = DELETERequest(deleteUrl)

        response = str(response)

        if response == "<Response [204]>":

            print str(user["profile"]["login"]) + " is Deleted" 
            deletedUsersCount += 1

            deletedWriter.writerow([user["profile"]["firstName"], user["profile"]["lastName"], user["profile"]["email"], user["profile"]["login"], user["status"]])
        
        else:

            notDeletedUserCount += 1

            notDeletedWriter.writerow([user["profile"]["firstName"], user["profile"]["lastName"], user["profile"]["login"], response])
    


    print "Deactivated Users: " + str(deactivedUsersCount)
    print "Deleted Users: " + str(deletedUsersCount)
    print "Not Deleted Users: " + str(notDeletedUserCount)

   

  

        

if __name__ == "__main__":

	DeleteUsers()