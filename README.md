Requirements for using the scripts
---------------------------------
* A Linux based OS (had problems using on Windows)
* Python 3.7+
* The following modules from pip3: `oauth2client`, `google-api-python-client`, `progress` & `httplib2shim`

Steps to make required number of service accounts for cloning
---------------------------------
1) Figure out how many projects you will need to make. For example, a 100TB clone job will take approximately 135 SAs to make a full clone. Each project can have a maximum limit of 100 SAs. Incase of the 100TB job, we will need 2 projects.
2) Head over to <https://console.developers.google.com/> and sign in with your account.
3) Click "Library" on the left column, then click on "Select a project" at the top. Click on `NEW PROJECT` on the top-right corner of the new window.
4) In the Project name section, input any project name you chose, followed by the number 1. For example, `copyjob`. Note down the Project ID. You will need them later.
5) After that, press `CREATE`. Wait till the project creation is done and then click on "Select a project" again at the top and select your project.
6) In the "Search for APIs & Services" search bar, look for "Google Drive API", click on it and press `ENABLE`. Do the same for "Identity and Access Management (IAM) API".
7) Repeat Steps 3-6 to create the amount of projects needed for your clone job.
8) You will need one master Service Account. To create it, select one of your projects. Click on the Google APIs logo on the top-left and then click on Credentials on the left pane. Next, press the blue `Create credentials` button and select "Service account key".
9) Make sure the selected Key type is JSON. Click on `Select...` and click on `New service account`.
10) Click on `Select a role` and scroll down to `Service Accounts`. From there, enable `Create Service Accounts` and `Service Account Key Admin`. Note down your Service account ID (`xxxx@xxxx.iam.gserviceaccount.com`) as you will need it later for the rest of your projects.
11) After that, press the blue `Create` button on the main screen. You should be prompted to download a JSON file. Save it to a new `controller` folder.
12) You will now need to share the rest of your projects with this new Service Account. To do so, head over to your next project. Open up the navigation menu in the top-left. Under `IAM & admin`, select `IAM`.
13) Click the `Add` button to add the Service account ID from Step 10. Assign the same roles from Step 10.
14) Repeat Steps 12 & 13 for each of your projects.
15) Open terminal in the scripts folder and run the following command. `python3 serviceaccountfactory.py`. It will autofill the project the Service Account originates from. Use it as an example to fill in the rest of your projects, followed by the desired amount of Service Accounts per project. 
16) Once the script is done making all the accounts, open Google Drive and make a new Shared Drive to copy all the files to.
17) Add the same Service account ID from Step 10 as a Manager to the Shared Drive.
18) Run the following command `python3 masshare.py`. It will prompt you for the Shared Drive ID. It can be taken from `https://drive.google.com/drive/folders/[Shared Drive ID]`.
19) After that, run the following command, `python3 multifolderclone.py`. It will prompt you for the source folder ID and for the destination shared drive ID. Both can be taken from `https://drive.google.com/drive/folders/[Folder ID/Shared Drive ID]`.
