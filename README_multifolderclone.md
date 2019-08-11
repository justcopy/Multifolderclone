Steps on how to use multifolderclone.py
=================================

Steps to make the required accounts for cloning
---------------------------------
1) Figure out how many projects you will need to make. For example, a 100TB clone job will take approximately 135 SAs to make a full clone. Each project can have a maximum limit of 100 SAs. Incase of the 100TB job, we will need 2 projects.
2) Head over to <https://console.developers.google.com/> and sign in with your account.
3) Click "Library" on the left column, then click on "Select a project" at the top. Click on `NEW PROJECT` on the top-right corner of the new window.
4) In the Project name section, input any project name you chose. Keep a note of the Project ID for each project that you make.
5) Repeat Steps 3 & 4 to create the amount of projects needed for your clone job.
6) Wait till the project creation is done and then click on "Select a project" again at the top and select your first project.
7) In the "Search for APIs & Services" search bar, look for "Google Drive API", click on it and press `ENABLE`. Do the same for "Identity and Access Management (IAM) API". Repeat this step for all the projects made.
8) Click on the Google APIs logo on the top-left, select your first project, and then go to `IAM & admin -> Service accounts` from the left pane. Next, press the blue `Create Service Account` button. In the Service account name section, input any name you want. Copy down the full Service account ID from your first project only, you will need this later. After that, press CREATE.
9) Click on `Select a role`. From the `Service Accounts` tab, select `Create Service Accounts` role. Then Press `ADD ANOTHER ROLE`, and under `Service Accounts` tab, select `Service Account Key Admin` role. and press CONTINUE. Then Press `+ Create Key`. Make sure the Key type is selected as JSON, and press CREATE. This should prompt you to save a JSON file. Save it in whereever the default download directory is for now.
10) Add the email address copied in Step 8 and add this to your other project with the same roles as mentioned in Step 9. You can do this by clicking on Google APIs logo on top left, selecting the project you want to share the email address with, then click on the Navigation menu icon which to the left of Google APIs logo, click `IAM & admin > IAM`. Now press  the blue `+ ADD` button, add the email address copied in Step 8, select the roles from step 9 and then press save. Repeat this for all the projects except the first project.
11) Place the JSON file you saved in a folder called `controller` and place the `controller` folder alongside with the 4 scripts.
12) Open terminal in the scripts folder and run the following command. `python3 serviceaccountfactory.py`.
13) It should automatically enter the project id and the number of accounts to create for the first project. Add all the other project ids and set accounts to create as 100. After you are done adding all, just press enter.
14) Enter any email prefix you want to use for your SAs and press enter. It should start making all the service accounts.
`The prefix needs to be 6 characters or longer.`

Steps to add all the SAs to the Shared Drive
---------------------------------
1) Once the previous script is done making all the accounts, open Google Drive and make a new Shared Drive to copy all the files to.
2) Run the following command `python3 masshare.py -d [SDFolderID]`. Replace the `[SDFolderID]` with `XXXXXXXXXXXXXXXXXXX`. The Folder ID can be obtained from the Shared Drive Folder Link `https://drive.google.com/drive/folders/XXXXXXXXXXXXXXXXXXX`.
3) Add the address mentioned by the script as a Manager to the Shared Drive and then press ENTER.
4) If everything was done correctly, the scripr will add all the service accounts to your Shared Drive.

Steps to clone a public folder to the Shared Drive
---------------------------------
1) Run the following command, `python3 multifolderclone.py -s [SourceFolderID] -d [SDFolderID]`. Replace `[SourceFolderID]` with the folder ID of the folder you are trying to copy and replace `[SDFolderID]` with the same ID as used in step 3 in `Steps to add all the SAs to the Shared Drive`. It should start cloning the source folder to the Shared Drive at this point if everything was done correctly.
