print("you probably shouldn't be using this program in production, as it's not been finished yet")

from oauth2client.service_account import ServiceAccountCredentials
import googleapiclient.discovery, json, socket, base64, random, string, argparse, itertools
from multiprocessing.dummy import Pool as ThreadPool

prid = ""

def ls(drive, parent, searchTerms=""):
    
    files = []
    resp = apicall(drive.files().list(q=f"'{parent}' in parents" + searchTerms, pageSize=1000,
        supportsAllDrives=True, includeItemsFromAllDrives=True))
    files += resp["files"]
    
    while "nextPageToken" in resp:
        resp = apicall(drive.files().list(q=f"'{parent}' in parents" + searchTerms, pageSize=1000,
            supportsAllDrives=True, includeItemsFromAllDrives=True, pageToken=resp["nextPageToken"]))
        files += resp["files"]
        
    return files

def lsd(drive, parent):
    
    return ls(drive, parent, searchTerms=" and mimeType contains 'application/vnd.google-apps.folder'")

def lsf(drive, parent):
    
    return ls(drive, parent, searchTerms=" and not mimeType contains 'application/vnd.google-apps.folder'")

def check_error(error):
    
    if isinstance(error, googleapiclient.errors.HttpError):
        edeets = json.loads(error.content.decode("utf-8"))
        ereasons = [i["reason"] for i in edeets["error"]["errors"]]
        if "dailyLimitExceeded" in ereasons:
            return 0
    return 1

class TransferRateLimit(Exception):
    
    pass

def apicall(request):
    
    resp = _apicall(request)
    while not resp: resp = _apicall(request)
    return resp
    
def _apicall(request):

    try:
        return request.execute()
    except googleapiclient.errors.HttpError as e:
        details = json.loads(e.content.decode("utf-8"))
        code = details["error"]["code"]
        reason = details["error"]["errors"][0]["reason"]
        message = details["error"]["errors"][0]["message"]
        if code in [400, 401, 404]:
            print("gapi error code " + str(code) + " [" + reason + "]: " + message)
            raise e
            return False
        elif code in [429, 500, 503]:
            return False
        elif code == 403:
            if reason in ["dailyLimitExceeded", "rateLimitExceeded"]:
                return False
            if reason == "userRateLimitExceeded":
                raise TransferRateLimit()
                return True
            elif reason in ["sharingRateLimitExceeded", "appNotAuthorizedToFile", "insufficientFilePermissions", "domainPolicy"]:
                print("gapi error code " + str(code) + " [" + reason + "]: " + message)
                raise e
            else:
                print("unknown reason '" + reason + "'")
        else:
            print("unknown error code " + str(code))
            raise e
    except socket.error as e:
        return False
        
# ret 1 = error
# ret * = new account
def new_account(iam, drive, driveid):
    global prid
    
    print("create new account")
    
    resp2 = apicall(iam.projects().serviceAccounts().create(name="projects/" + prid, body={
        "accountId": ''.join(random.choices(string.ascii_lowercase, k=30))
    }))
    key = apicall(iam.projects().serviceAccounts().keys().create(name="projects/" + prid + "/serviceAccounts/" + resp2["uniqueId"], body={
        "privateKeyType": "TYPE_GOOGLE_CREDENTIALS_FILE",
        "keyAlgorithm": "KEY_ALG_RSA_2048"
    }))
    
    resp = apicall(drive.permissions().create(fileId=driveid, body={
        "role": "organizer",
        "type": "user",
        "emailAddress": resp2["email"]
    }, supportsAllDrives=True))
    
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(json.loads(base64.b64decode(key["privateKeyData"]).decode("utf8")))
    drive = googleapiclient.discovery.build("drive", "v3", credentials=credentials)
    drive.pid = resp["id"]
    drive.service_id = resp2["uniqueId"]
    drive.email = resp2["email"]
    return drive

def old_account(iam, drive, driveid):
    global prid
    
    print("delete old account")
    
    try:
        apicall(drive.permissions().delete(fileId=driveid, permissionId=drive.pid, supportsAllDrives=True))
    except googleapiclient.errors.HttpError:
        pass
    try:
        apicall(iam.projects().serviceAccounts().delete(name="projects/" + prid + "/serviceAccounts/" + drive.email))
    except googleapiclient.errors.HttpError:
        pass

def cycle_drive(iam, drive, quotafile):
    
    print("cycle drive")
    
    resp1 = apicall(drive.files().get(fileId=quotafile, supportsAllDrives=True))
    
    new_drive = new_account(iam, drive, resp1["driveId"])
    while new_drive == 1:
        new_drive = new_account(iam, drive, resp1["driveId"])
    old_account(iam, drive, resp1["driveId"])
    
    return new_drive

# ret 0 = success
# ret 1 = error
# ret * = new drive instance
def copy(iam, drive, source, dest):
    
    print("copy file from " + source + " to " + dest)
    
    try:
        apicall(drive.files().copy(fileId=source, body={"parents": [dest]}, supportsAllDrives=True))
    except TransferRateLimit as e:
        return cycle_drive(iam, drive, source)
    else:
        return 0

def copy_dir(credentials, source, dest):
    
    print("start copydir from " + source + " to " + dest)
    
    drive = googleapiclient.discovery.build("drive", "v3", credentials=credentials)
    iam = googleapiclient.discovery.build("iam", "v1", credentials=credentials)
    
    print("get file")
    resp = apicall(drive.files().get(fileId=dest, supportsAllDrives=True))
    driveid = resp["driveId"]
    new_drive = new_account(iam, drive, driveid)
    while new_drive == 1:
        new_drive = new_account(iam, drive, driveid)
    drive = new_drive
    flist = lsf(drive, source)
    for i in flist:
        while True:
            resp = copy(iam, drive, i["id"], dest)
            if resp == 0:
                break
            elif resp == 1:
                continue
            else:
                drive = resp
    old_account(iam, drive, driveid)

# ret [source_id, dest_id, is_final?]
def resolve_folder(drive, source, dest):
    
    flist = lsf(drive, source)
    dlist = lsd(drive, source)
    
    ret = []
    
    if flist:
        ret.append([source, dest, True])
    for i in dlist:
        resp = apicall(drive.files().create(body={
            "name": i["name"],
            "mimeType": "application/vnd.google-apps.folder",
            "parents": [dest]
        }, supportsAllDrives=True))
        ret.append([i["id"], resp["id"], False])
    
    return ret

def main():
    global prid

    parser = argparse.ArgumentParser("betterclone.py", description="copies a folder using service accounts")
    parser.add_argument("-k", "--keyfile", default="key.json", help="keyfile filename")
    parser.add_argument("project", help="id of the project")
    parser.add_argument("source", help="id of the source folder")
    parser.add_argument("destination", help="id of the destination folder")
    args = parser.parse_args()

    print("auth main sa")
    credentials = ServiceAccountCredentials.from_json_keyfile_name(args.keyfile, [
        "https://www.googleapis.com/auth/iam",
        "https://www.googleapis.com/auth/drive"
    ])
    iam = googleapiclient.discovery.build("iam", "v1", credentials=credentials)
    drive = googleapiclient.discovery.build("drive", "v3", credentials=credentials)
    prid = args.project
    flist = resolve_folder(drive, args.source, args.destination)
    
    print("processing directories")
    while True:
        
        c = True
        
        for i in flist:
            if not i[2]:
                print("process " + i[0])
                flist += resolve_folder(drive, i[0], i[1])
                del flist[flist.index(i)]
                c = False
        
        if c:
            break
    
    print("start copy")
    pool = ThreadPool(98)
    pool.starmap(copy_dir, zip(itertools.repeat(credentials), [i[0] for i in flist], [i[1] for i in flist]))
    pool.close()
    pool.join()

if __name__ == "__main__":
    main()
