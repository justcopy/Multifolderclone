"""
USAGE
python3 serviceaccountfactory.py project_lower project_upper account_prefix project_prefix

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
import googleapiclient.discovery, base64, json, progress.bar, sys

def create_service_account_and_dump_key(project_id, service_account_name, service_account_filename):
    
    service_account = iam.projects().serviceAccounts().create(
        name="projects/" + project_id,
        body={
            "accountId": service_account_name,
            "serviceAccount": {
                "displayName": service_account_name
            }
        }
    ).execute()

    key = iam.projects().serviceAccounts().keys().create(
        name="projects/" + project_id + "/serviceAccounts/" + service_account["uniqueId"],
        body={
            "privateKeyType": "TYPE_GOOGLE_CREDENTIALS_FILE",
            "keyAlgorithm": "KEY_ALG_RSA_2048"
        }
    ).execute()
    
    f = open("accounts/" + service_account_filename + ".json", "w")
    f.write(base64.b64decode(key["privateKeyData"]).decode("utf-8"))
    f.close()

pbar = progress.bar.Bar("creating accounts", max=((int(sys.argv[2]) + 1 - int(sys.argv[1])) * 100))

for i in range(int(sys.argv[1]), int(sys.argv[2])+1):
    
    credentials = ServiceAccountCredentials.from_json_keyfile_name("controller" + str(i) + ".json", scopes=[
        "https://www.googleapis.com/auth/iam"
    ])
    
    iam = googleapiclient.discovery.build("iam", "v1", credentials=credentials)
    
    for o in range(1, 101):
        
        create_service_account_and_dump_key(sys.argv[4] + str(i), sys.argv[3] + str(((i-1)*100)+o), str(((i-1)*100)+o))
        pbar.next()

pbar.finish()
