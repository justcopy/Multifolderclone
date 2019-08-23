from google.oauth2.service_account import Credentials
import googleapiclient.discovery, progress.bar, time, threading, httplib2shim, glob, sys, argparse

stt = time.time()
args = {}
views = ['tree','indented','basic']
view = 0
source_id = ""
dest_id = ""

parse = argparse.ArgumentParser(description='A tool intended to copy large files from one folder to another.')
parse.add_argument('--view',default='tree',help='Set the view to a different setting (tree|indented|basic).')
parse.add_argument('--width','-w',default=2,help='Set the width of the view option.')
parse.add_argument('--path','-p',default='accounts',help='Specify an alternative path to the service accounts.')
parsereq = parse.add_argument_group('required arguments')
parsereq.add_argument('--source-id','-s',help='The source ID of the folder to copy.',required=True)
parsereq.add_argument('--destination-id','-d',help='The destination ID of the folder to copy to.',required=True)
args = parse.parse_args()

print('Copy from %s to %s.' % (args.source_id,args.destination_id))
print('View set to %s (%d).' % (args.view,args.width))

view = args.view
width = args.width

def ls(parent, searchTerms=""):
    while True:
        try:
            files = []
            resp = drive[0].files().list(q=f"'{parent}' in parents" + searchTerms, pageSize=1000, supportsAllDrives=True, includeItemsFromAllDrives=True).execute()
            files += resp["files"]
            while "nextPageToken" in resp:
                resp = drive[0].files().list(q=f"'{parent}' in parents" + searchTerms, pageSize=1000, supportsAllDrives=True, includeItemsFromAllDrives=True, pageToken=resp["nextPageToken"]).execute()
                files += resp["files"]
            return files
        except Exception as e:
            time.sleep(3)

def lsd(parent):
    
    return ls(parent, searchTerms=" and mimeType contains 'application/vnd.google-apps.folder'")

def lsf(parent):
    
    return ls(parent, searchTerms=" and not mimeType contains 'application/vnd.google-apps.folder'")

def copy(source, dest, dtu):
    global drive
    while True:
        try:
            copied_file = drive[dtu].files().copy(fileId=source, body={"parents": [dest]}, supportsAllDrives=True).execute()
        except Exception as e:
            time.sleep(3)
        else:
            break
    threads.release()

def rcopy(source, dest, sname,pre):
    
    global drive
    global accounts
    global dtu
    global width

    pres = pre
    if view == 2:
        pres = ""
    elif view == 1:
        pres = " " * (int(((len(pre) - 4))/3) * width)

    filestocopy = lsf(source)
    if len(filestocopy) > 0:
        pbar = progress.bar.Bar(pres + sname, max=len(filestocopy))
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
        print(pres + sname)
    
    folderstocopy = lsd(source)
    fs = len(folderstocopy) - 1
    s = 0
    for i in folderstocopy:
        if s == fs:
            nstu = pre.replace("├" + "─" * width + " ","│" + " " * width + " ").replace("└" + "─" * width + " ","  " + " " * width) + "└" + "─" * width + " "
        else:
            nstu = pre.replace("├" + "─" * width + " ","│" + " " * width + " ").replace("└" + "─" * width + " ","  " + " " * width) + "├" + "─" * width + " "
        resp = drive[0].files().create(body={
            "name": i["name"],
            "mimeType": "application/vnd.google-apps.folder",
            "parents": [dest]
        }, supportsAllDrives=True).execute()
        rcopy(i["id"], resp["id"], i["name"].replace('%',"%%"),nstu)
        s += 1

httplib2shim.patch()
drive = []
accounts = 0
accsf = glob.glob(args.path + '/*.json')
pbar = progress.bar.Bar("Creating Drive Services", max=len(accsf))
for i in accsf:
    accounts += 1
    credentials = Credentials.from_service_account_file(i, scopes=[
        "https://www.googleapis.com/auth/drive"
    ])
    drive.append(googleapiclient.discovery.build("drive", "v3", credentials=credentials))
    pbar.next()
pbar.finish()
threads = threading.BoundedSemaphore(accounts)
print('BoundedSemaphore with %d threads' % accounts)
dtu = 1

try:
    rcopy(args.source_id,args.destination_id , "root","")
except KeyboardInterrupt:
    print('Quitting')
    pass
except Exception as e:
    print(e)
print('Complete.')
hours, rem = divmod((time.time() - stt),3600)
minutes, sec = divmod(rem,60)
print("Elapsed Time:\n{:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),sec))
