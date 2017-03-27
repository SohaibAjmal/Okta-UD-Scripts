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




def GetEvents():

    eventsUrl = "https://"+orgName+".com/api/v1/events?filter=published gt \"2017-01-27T00:00:00.000Z\""

    responseJSON = GetPaginatedResponse(eventsUrl)

    userFile = open("App-Access-Events.csv", "wb")

    print "\nAll Events Retrieved. Generating CSV...\n"
    writer = csv.writer(userFile)

    writer.writerow(["Category", "Message", "RequestUri",  "Admin", "AppUser", "App","Timestamp" "EVENT_JSON"])
    
    if responseJSON != "Error":

        count = 0 
        for event in responseJSON:

            categories = []
            categories = event[u"action"][u"categories"]

            if "Application Assignment" in categories:

                admin = ""
                appUser = ""
                app = ""
               

                category = categories[categories.index("Application Assignment")]

                message = event[u"action"][u"message"]

                requestUri = event[u"action"][u"requestUri"]

                actors = event[u"actors"]

                targets = event[u"targets"]

                timestamp = event[u"published"]


                for actor in actors:

                    if actor[u"objectType"] == "User":

                        if u"login" in actor:

                            admin = actor[u"login"]


                for target in targets:

                    if target[u"objectType"] == "User":

                        if u"login" in target:

                            appUser = target[u"login"]


                    if target[u"objectType"] == "AppInstance":

                        if u"displayName" in target:

                            app = target[u"displayName"]



                if admin != "":
                	writer.writerow([category, message, requestUri, admin, appUser, app, timestamp, event])


if __name__ == "__main__":

	GetEvents()