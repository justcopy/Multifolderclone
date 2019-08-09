from oauth2client.service_account import ServiceAccountCredentials
import googleapiclient.discovery, json, progress.bar, glob, sys, argparse

parse = argparse.ArgumentParser(description='A tool to add service accounts to a shared drive from a folder containing credential files.')
parse.add_argument('--path','-p',default='accounts',help='Specify an alternative path to the service accounts folder.')
parse.add_argument('--controller','-c',default='controller/*.json',help='Specify the relative path for the controller file.')
parsereq = parse.add_argument_group('required arguments')
parsereq.add_argument('--drive-id','-d',help='The ID of the Shared Drive.',required=True)

args = parse.parse_args()
acc_dir = args.path
did = args.drive_id
contrs = glob.glob(args.controller)

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

drive = googleapiclient.discovery.build("drive", "v3", credentials=credentials)
aa = glob.glob('%s/*.json' % acc_dir)
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
