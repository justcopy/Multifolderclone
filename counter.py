from google.oauth2.service_account import Credentials
import googleapiclient.discovery, json, progress.bar, socket, time, sys, glob

stt = time.time()
fct = 0
dct = 0

try:
    sas = glob.glob('key.json')
    sas.extend(glob.glob('controller/*.json'))
    sas.extend(glob.glob('accounts/*.json'))
    filename = sas[0]
except IndexError:
    print('No Service Account Found.')
    sys.exit(0)

credentials = Credentials.from_service_account_file(filename, scopes=[
    "https://www.googleapis.com/auth/drive"
])
drive = googleapiclient.discovery.build("drive", "v3", credentials=credentials)

def ls(parent, searchTerms=""):
    files = []
    resp = drive.files().list(q=f"'{parent}' in parents" + searchTerms, pageSize=1000, supportsAllDrives=True, includeItemsFromAllDrives=True).execute()
    files += resp["files"]
    while "nextPageToken" in resp:
        resp = drive.files().list(q=f"'{parent}' in parents" + searchTerms, pageSize=1000, supportsAllDrives=True, includeItemsFromAllDrives=True, pageToken=resp["nextPageToken"]).execute()
        files += resp["files"]
    return files

def lsd(parent):
    return ls(parent, searchTerms=" and mimeType contains 'application/vnd.google-apps.folder'")

def lsf(parent):
    return ls(parent, searchTerms=" and not mimeType contains 'application/vnd.google-apps.folder'")

def rs(source):
    global fct, dct
    
    fs = lsf(source)
    fct += len(fs)
    
    fd = lsd(source)
    dct += len(fd)
    for i in fd:
        rs(i['id'])

try:
    sp = sys.argv[1]
except IndexError:
    sp = input('Folder ID to scan? ').strip()

print('Counting objects in %s' % sp)
rs(sp)
print('Objects: %d\nFolders: %d' % (fct,dct))

hours, rem = divmod((time.time() - stt),3600)
minutes, sec = divmod(rem,60)
print("Elapsed Time:\n{:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),sec))
