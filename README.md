# Google Drive Logger

Run `setup.sh` to install dependencies.
Some modification is needed to customize the data to be uploaded and the key for the google docs spreadsheet.
Additionally a credentials.json file needs to be placed in the same directory.
Instructions for creating that file can be found [here](http://gspread.readthedocs.org/en/latest/oauth2.html)

Run `gogl-drive.py` to add a row to a spreadsheet of your choosing.
This should be added to a cronjob for propper logging.
