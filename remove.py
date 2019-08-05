from oauth2client.service_account import ServiceAccountCredentials
import googleapiclient.discovery, glob, progress.bar, sys

controls = glob.glob('controller/*.json')

try:
	key = controls[0]
except IndexError:
	print('No controller found.')
	sys.exit(0)

try:
	sid = sys.argv[1]
except:
	sid = input("Shared Drive ID? ").strip()

credentials = ServiceAccountCredentials.from_json_keyfile_name(key, scopes=[
	"https://www.googleapis.com/auth/drive"
])

drive = googleapiclient.discovery.build("drive", "v3", credentials=credentials)

print('Getting permissions...')

tbr = []

rp = drive.permissions().list(fileId=sid,supportsAllDrives=True).execute()['permissions']
for i in rp:
	if i['role'] != 'organizer':
		tbr.append(i['id'])

while "nextPageToken" in rp:
	rp = drive.permissions().list(fileId=sid,supportsAllDrives=True).execute()['permissions']
	for i in rp:
		if i['role'] != 'organizer':
			tbr.append(i['id'])

pbar = progress.bar.Bar("Removing accounts",max=len(tbr))

for i in tbr:
	drive.permissions().delete(fileId=sid,permissionId=i,supportsAllDrives=True).execute()
	pbar.next()
pbar.finish()
print('Done.')
