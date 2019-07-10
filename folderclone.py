"""
USAGE:
python3 folderclone.py starting_account source_dir destination_dir

starting_account:
account number to start on, useful for having multiple clones use different accounts

source_dir:
id of the source directory

destination_dir:
id of the destination directory
"""

from oauth2client.service_account import ServiceAccountCredentials
import googleapiclient.discovery, json, progress.bar, socket, time, sys

cred_num = int(sys.argv[1])

credentials = ServiceAccountCredentials.from_json_keyfile_name("accounts/" + str(cred_num) + ".json", scopes=[
    "https://www.googleapis.com/auth/drive"
])

drive = googleapiclient.discovery.build("drive", "v3", credentials=credentials)

logfile = open("log.txt", "w")

def logwrite(logtext):
    
    logfile.write(time.strftime("%m-%d %H:%M:%S") + " " + logtext + "\n")
    logfile.flush()

def ls(parent, searchTerms="", fname=""):
    files = []
    resp = drive.files().list(q=f"'{parent}' in parents" + searchTerms, pageSize=1000, supportsAllDrives=True, includeItemsFromAllDrives=True).execute()
    files += resp["files"]
    while "nextPageToken" in resp:
        resp = drive.files().list(q=f"'{parent}' in parents" + searchTerms, pageSize=1000, supportsAllDrives=True, includeItemsFromAllDrives=True, pageToken=resp["nextPageToken"]).execute()
        files += resp["files"]
    return files

def lsd(parent, fname=""):
    
    return ls(parent, searchTerms=" and mimeType contains 'application/vnd.google-apps.folder'", fname=fname)

def lsf(parent, fname=""):
    
    return ls(parent, searchTerms=" and not mimeType contains 'application/vnd.google-apps.folder'", fname=fname)

def copy(source, dest):
    
    global drive
    global cred_num
    
    try:
        copied_file = drive.files().copy(fileId=source, body={"parents": [dest]}, supportsAllDrives=True).execute()
    except googleapiclient.errors.HttpError as e:
        cred_num += 1
        if cred_num % 100 == 0:
            cred_num += 1
        credentials = ServiceAccountCredentials.from_json_keyfile_name("accounts/" + str(cred_num) + ".json", scopes=[
            "https://www.googleapis.com/auth/drive"
        ])
        drive = googleapiclient.discovery.build("drive", "v3", credentials=credentials)
        logwrite("changed cred_num to " + str(cred_num))
        copy(source, dest)
    except socket.timeout:
        logwrite("timeout")
        time.sleep(60)
        copy(source, dest)
    except Exception as e:
        logwrite("error: " + str(e))
        try:
            copy(source, dest)
        except RecursionError as e:
            logwrite("max recursion reached")
            raise e

def rcopy(source, dest, sname):
    
    global drive
    global cred_num
    
    filestocopy = lsf(source, fname=sname)
    if len(filestocopy) > 0:
        pbar = progress.bar.Bar("copy " + sname, max=len(filestocopy))
        pbar.update()
        logwrite("copy filedir " + sname)
        for i in filestocopy:
            
            copy(i["id"], dest)
            pbar.next()
        
        pbar.finish()
        
    else:
        
        logwrite("copy dirdir " + sname)
        print("copy " + sname)
    
    folderstocopy = lsd(source)
    for i in folderstocopy:
        
        resp = drive.files().create(body={
            "name": i["name"],
            "mimeType": "application/vnd.google-apps.folder",
            "parents": [dest]
        }, supportsAllDrives=True).execute()
        
        rcopy(i["id"], resp["id"], i["name"])

print("copying files... eta 5 minutes")
logwrite("start copy")
try:
    rcopy(str(sys.argv[2]), str(sys.argv[3]), "root")
except Exception as e:
    logfile.close()
    raise e
print("completed copy with account " + str(cred_num))
logwrite("finish copy")
logfile.close()
