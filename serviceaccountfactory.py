from google.oauth2.service_account import Credentials
import googleapiclient.discovery, base64, json, progress.bar, glob, sys
from os import mkdir

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
	
	f = open("accounts/" + service_account_filename, "w")
	f.write(base64.b64decode(key["privateKeyData"]).decode("utf-8"))
	f.close()


contrs = glob.glob('controller/*.json')
try:
	open(contrs[0],'r')
	print('Found controllers.')
except IndexError:
	print('No controller found.')
	sys.exit(0)
proj = 1
projects = {}
print('Add more projects:')
print('[project id] [accounts to create]')
pid = json.loads(open(contrs[0],'r').read())['project_id']
projects[pid] = 99
print(str(proj) + '. ' + pid + ' 99')
while pid != '':
	proj += 1
	pid = input(str(proj) + '. ')
	if pid:
		a = pid.split()
		projects[a[0]] = a[1]

prefix = ''
while len(prefix) < 4:
	prefix = input('Custom email prefix? ').lower()
	if prefix == '':
		prefix = 'folderclone'
	if len(prefix) < 4:
		print('Email prefix must be 5 characters or longer!')
print('Using ' + str(len(projects)) + ' projects...')

credentials = Credentials.from_service_account_file(contrs[0], scopes=[
	"https://www.googleapis.com/auth/iam"
	])
iam = googleapiclient.discovery.build("iam", "v1", credentials=credentials)

try:
	mkdir('accounts')
except FileExistsError:
	pass

gc = 1
for i in projects:
	pbar = progress.bar.Bar("Creating accounts in %s" % i,max=int(projects[i]))
	for o in range(1, int(projects[i]) + 1):
		try:
			create_service_account_and_dump_key(i,prefix + str(o),str(gc) + '.json')
		except googleapiclient.errors.HttpError:
			pass
		gc += 1
		pbar.next()
	pbar.finish()
