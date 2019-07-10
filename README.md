Requirements for using the scripts
---------------------------------
* A Linux based OS (had problems using on Windows)
* Python 3.7+
* The following modules from pip3: `oauth2client`, `google-api-python-client` & `progress`

Steps to make required number of service accounts for cloning
---------------------------------
1) Figure out how many projects you will need to make. For example, a 100TB clone job will take approximately 135 SAs to make a full clone. Each project can have a maximum limit of 100 SAs. Incase of the 100TB job, we will need 2 projects.
2) Head over to <https://console.developers.google.com/> and sign in with your account.
3) Click "Library" on the left column, then click on "Select a project" at the top. Click on `NEW PROJECT` on the top-right corner of the new window.
4) In the Project name section, input any project name you chose, followed by the number 1. For example, `copyjob1`. After that, press `CREATE`.
5) Repeat Steps 3 & 4 to create the amount of projects needed for your clone job, while keeping the first part of the project name same and increasing the number at the end for each new project needed. For example, we need to make `copyjob1` and `copyjob2` project for our 100TB clone job.
6) Wait till the project creation is done and then click on "Select a project" again at the top and select your first project.
7) In the "Search for APIs & Services" search bar, look for "Google Drive API", click on it and press `ENABLE`. Do the same for "Identity and Access Management (IAM) API".
8) Click on the Google APIs logo on the top-left and then click on Credentials on the left pane. Next, press the blue `Create credentials` button and select "Service account key".
9) Make sure the selected Key type is JSON. Click on `Select...` and click on `New service account`.
10) Select the Service account name the same as the project name. For example, the Service account name for our 100TB job will be `copyjob1`.
11) Click on `Select a role` and scroll down to `Service Accounts`. From there, enable `Create Service Accounts` and `Service Account Key Admin`. After that, press the blue `Create` button on the main screen. You should be prompted to download a JSON file. Save it.
12) Repeat Steps 7 to 11 for all your projects.
13) Place the JSON files in the same folder as the 3 scripts are in. Rename the first project JSON file to controller1.json, the 2nd JSON to controller2.json and so on.
14) Open terminal in the scripts folder and run the following command. `python3 serviceaccountfactory.py 1 [number of projects] [accountprefix of your choice] [project prefix]`. Replace `[number of projects]` with the total number of projects used, `[accountprefix of your choice]` with prefix of your choice and `[project prefix]` with the project name used in Step 4.
15) If you have set everything up correctly, you should see the script making 99 service accounts of each project.
16) Once the script is done making all the accounts, open Google Drive and make a new TeamDrive to copy all the files to.
17) Add `[projectname1]@[projectname1].iam.gserviceaccount.com` as a Manager to the TD. Replace `[projectname1]` with the name of your first project. For example, the first project name for our example was copyjob1, so the email address will be `copyjob1@copyjob1.iam.gserviceaccount.com`.
18) Run the following command `python3 masshare.py [TDFolderID] 1 [number of projects] [accountprefix of your choice] [project prefix]`. Replace the `[TDFolderID]` with `XXXXXXXXXXXXXXXXXXXXXXXXX`. The Folder ID can be obtained from the TD Folder Link `https://drive.google.com/drive/folders/XXXXXXXXXXXXXXXXXXXXXXXXX`. This will add all the service accounts to your TD.
19) After that, run the following command, `python3 folderclone.py 1 [SourceFolderID] [TDFolderID]`. Replace `[SourceFolderID]` with the folder ID of the folder you are trying to copy and replace `[TDFolderID]` with the same ID as used in step 18. It should start cloning the source folder to the TD at this point if everything was done correctly.
