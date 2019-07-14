'''
Usage:
python3 multifolderclone.py source dest

source:
ID of source folder

dest:
ID of destination folder
'''

from oauth2client.service_account import ServiceAccountCredentials
import googleapiclient.discovery, progress.bar, time, threading, httplib2shim, glob, sys

print('Started at %s' % time.strftime("%m-%d %H:%M:%S"))

def ls(parent, searchTerms="", fname=""):
    files = []
    resp = drive[0].files().list(q=f"'{parent}' in parents" + searchTerms, pageSize=1000, supportsAllDrives=True, includeItemsFromAllDrives=True).execute()
    files += resp["files"]
    while "nextPageToken" in resp:
        resp = drive[0].files().list(q=f"'{parent}' in parents" + searchTerms, pageSize=1000, supportsAllDrives=True, includeItemsFromAllDrives=True, pageToken=resp["nextPageToken"]).execute()
        files += resp["files"]
    return files

def lsd(parent, fname=""):
    
    return ls(parent, searchTerms=" and mimeType contains 'application/vnd.google-apps.folder'", fname=fname)

def lsf(parent, fname=""):
    
    return ls(parent, searchTerms=" and not mimeType contains 'application/vnd.google-apps.folder'", fname=fname)

def copy(source, dest, dtu):
    global drive
    while True:
        try:
            copied_file = drive[dtu].files().copy(fileId=source, body={"parents": [dest]}, supportsAllDrives=True).execute()
        except Exception as e:
            continue
        else:
            break
    threads.release()

def rcopy(source, dest, sname):
    
    global drive
    global accounts
    global dtu

    filestocopy = lsf(source, fname=sname)
    if len(filestocopy) > 0:
        pbar = progress.bar.Bar("copy " + sname, max=len(filestocopy))
        pbar.update()
        for i in filestocopy:
            threads.acquire()
            thread = threading.Thread(target=copy,args=(i["id"], dest,dtu))
            thread.start()
            dtu += 1
            if dtu == accounts:
                dtu = 1
            pbar.next()
        
        pbar.finish()
    else:
        print("copy " + sname)
    
    folderstocopy = lsd(source)
    for i in folderstocopy:
        resp = drive[0].files().create(body={
            "name": i["name"],
            "mimeType": "application/vnd.google-apps.folder",
            "parents": [dest]
        }, supportsAllDrives=True).execute()
        rcopy(i["id"], resp["id"], i["name"])

httplib2shim.patch()

drive = []
print('Finding accounts...')
accounts = 0
for i in glob.glob('accounts/*.json'):
    accounts += 1
    credentials = ServiceAccountCredentials.from_json_keyfile_name(i, scopes=[
        "https://www.googleapis.com/auth/drive"
    ])
    print('Creating drive service from %s' % i)
    drive.append(googleapiclient.discovery.build("drive", "v3", credentials=credentials))
print('Create %d drive services' % accounts)
threads = threading.BoundedSemaphore(accounts)
print('BoundedSemaphore with %d threads' % accounts)
dtu = 1

try:
    agg1 = sys.argv[1]
except:
    agg1 = input('Source Folder ID? ')

try:
    agg2 = sys.argv[2]
except:
    agg2 = input('Destination Drive ID? ')
    
try:
    rcopy(str(agg1), str(agg2), "root")
except Exception as e:
    print(e)
print('Complete.')
print('Ended at %s' % time.strftime("%m-%d %H:%M:%S"))
