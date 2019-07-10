"""
USAGE
python3 masshare.py drive_id project_lower project_upper account_prefix project_prefix

drive_id:
id of the drive you're sharing to

project_lower:
lower bounds of project iterator

project_upper:
upper bounds of project iterator

account_prefix:
prefix of account

project_prefix:
prefix of project
"""

from oauth2client.service_account import ServiceAccountCredentials
import googleapiclient.discovery, json, progress.bar, sys

credentials = ServiceAccountCredentials.from_json_keyfile_name("controller1.json", scopes=[
    "https://www.googleapis.com/auth/drive"
])

drive = googleapiclient.discovery.build("drive", "v3", credentials=credentials)

for i in range(int(sys.argv[2]), int(sys.argv[3])+1):
    for o in range(1, 101):
        print(sys.argv[4] + str(o + (100*i) - 100) + "@" + sys.argv[5] + str(i) + ".iam.gserviceaccount.com")
        drive.permissions().create(fileId=sys.argv[1], supportsAllDrives=True, body={
            "role": "fileOrganizer",
            "type": "user",
            "emailAddress": sys.argv[4] + str(o + (100*i) - 100) + "@" + sys.argv[5] + str(i) + ".iam.gserviceaccount.com"
        }).execute()
