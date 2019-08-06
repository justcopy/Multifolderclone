Steps on how to use betterclone.py
---------------------------------

1) Head over to <https://console.developers.google.com/> and sign in with your account.
2) Click "Library" on the left column, then click on "Select a project" at the top. Click on `NEW PROJECT` on the top-right corner of the new window.
3) In the Project name section, input any project name you chose. Keep a note of the Project ID for project that you make.
4) Wait till the project creation is done and then click on "Select a project" again at the top and select your project.
5) In the "Search for APIs & Services" search bar, look for "Google Drive API", click on it and press `ENABLE`. Do the same for "Identity and Access Management (IAM) API".
6) Click on the Google APIs logo on the top-left, select your project, and then go to `IAM & admin -> Service accounts` from the left pane. Next, press the blue `Create Service Account` button. In the Service account name section, input any name you want. Copy down the full Service account ID, you will need this later. After that, press CREATE.
7) Click on `Select a role`. From the `Service Accounts` tab, select `Service Account Admin` role. Then Press `ADD ANOTHER ROLE`, and under `Service Accounts` tab, select `Service Account Key Admin` role. and press CONTINUE. Then Press `+ Create Key`. Make sure the Key type is selected as JSON, and press CREATE. This should prompt you to save a JSON file. Save it in whereever the default download directory is for now.
8) Place the JSON file you saved alongside with the scripts.
9) Go to Google Drive, sign in with your account. Go to Shared Drive tab and make a new Shared Drive. Add the email address you copied in Step 6 as a Manager in the Shared Drive. Copy the folder ID of the Shared Drive. It can be obtained from the URL when you open Shared Drive, it is 19 characters long and looks like 0xxxxxxxxxxxxxxxxx.
10) Copy the folder ID of the folder you are trying to copy. It can be obtained from the folder URL, it is 33 characters long and looks like 1xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx.
11) Open terminal in the scripts folder and run the following command. `python3 betterclone.py [projectid] [source] [destination] -k [JSON file]`. Replace `[projectid]` with the Project ID saved in Step 3. Replace `[source]` with the ID copied in Step 11, `[destination]` with the ID copied in Step 10 and `[JSON file]` with the filename of the JSON saved in Step 7.
