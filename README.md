# Okta-UD-Scripts
Few scripts to operate on UD

Python scripts that demonstrte use of Okta's REST APIs for Unviversl Directory. Description of each script

1) activate_staged_users.py -> Activates all STAGED (Pending activation) users in the org.
2) create_random_users.py -> Create N number of random users in org. Helpful in case when you want to create bunch of users for testing
3) get_all_active_users.py -> Retrieve all active users from org and write them in csv
4) get_app_assignment_events -> Capture app assignments done by admin, in csv file. 
5) set_attribute.py -> Set any attribute (attributeName in the script) to a value (attributeValue) for all users in org
6) delete_users.py -> Delete all deactivated users in the Okta tenant. 

Last ud_script_template.py is a template. It has functions to make REST API calls (GET, GET paginated, POST, PUT and DELETE). 
This script can be used to create any use case. Test the use case in Python and use this script to create same flow using functions.

# Requirements to Run Script:

1) Python 2.7
2) Python's requests libaray (run "pip install requests" from command line or shell). You may need t install pip i.e. Python's package
manager on Windows system


# How to Run Script

For first 5 script open the script in your favorite editor (e.g. Sublime) and set orgName including okta/oktapreview to your org e.g. 
"myorg.okta" or "myorg.oktapreview". If there are any required attribute such as N, attributeName, attributeValue at the top, update 
those to yoru need as well.

In command prompt or shell navigate to folder where Python script is copied "cd ~/Documents/PythonScripts" and run the script e.g
"python activate_staged_users.py"
