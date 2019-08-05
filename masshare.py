from oauth2client.service_account import ServiceAccountCredentials
import googleapiclient.discovery, json, progress.bar, glob, sys

contrs = glob.glob('controller/*.json')

try:
	open(contrs[0],'r')
	print('Found controllers.')
except IndexError:
	print('No controller found.')
	sys.exit(0)

input('Make sure the following email is added to the shared drive as Manager:\n' + json.loads((open(contrs[0],'r').read()))['client_email'])

credentials = ServiceAccountCredentials.from_json_keyfile_name(contrs[0], scopes=[
	"https://www.googleapis.com/auth/drive"
])

try:
	did = sys.argv[1]
except:
	did = input('Drive ID? ').strip()

drive = googleapiclient.discovery.build("drive", "v3", credentials=credentials)
aa = glob.glob('accounts/*.json')
pbar = progress.bar.Bar("Adding to %s" % did,max=len(aa))
for i in aa:
	ce = json.loads(open(i,'r').read())['client_email']
	drive.permissions().create(fileId=did, supportsAllDrives=True, body={
		"role": "fileOrganizer",
		"type": "user",
		"emailAddress": ce
	}).execute()
	pbar.next()
pbar.finish()

print('Complete. You can now drop the controller inside the accounts folder for an added SA.')
