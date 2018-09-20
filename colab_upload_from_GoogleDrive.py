! pip install -U -q PyDrive  # Need to install this module in GoogleColab
import os
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from google.colab import auth
from oauth2client.client import GoogleCredentials


def get_files_from_dir(dir_id, local_download_path):
    try:
        os.makedirs(local_download_path)
    except Exception as e:
        print('Didnt make dir.', e)

    # 2. Auto-iterate using the query syntax
    #    https://developers.google.com/drive/v2/web/search-parameters
    file_list = drive.ListFile({'q': "'%s' in parents" % (dir_id)}).GetList()
    folders_tree = []
    for f in file_list:
        # 3. Iterate by file in list
        print('title: %s, id: %s, mimeType: %s' % (f['title'],
                                                   f['id'],
                                                   f['mimeType']))
        fname = os.path.join(local_download_path, f['title'])
        print('downloading to {}'.format(fname))
        try:
            if f['mimeType'] == 'application/vnd.google-apps.folder':
                # If element is subfolder:
                # 3.1 Create subfolder and iterate through it
                get_files_from_dir(f['id'], fname+'/')
            else:

                # 3.2 Create & download by id.
                f_ = drive.CreateFile({'id': f['id']})
                f_.GetContentFile(fname)
        except Exception as e:
            # local_download_path = fname
            # os.makedirs(local_download_path)
            print('file not downloaded.', e)


# 1. Authenticate and create the PyDrive client.
auth.authenticate_user()
gauth = GoogleAuth()
gauth.credentials = GoogleCredentials.get_application_default()
drive = GoogleDrive(gauth)

# Choose a local (colab) directory to store the data.
local_download_path = os.path.expanduser('')
try:
    os.makedirs(local_download_path)
except:
    pass

# Choose folder id in GoogleDrive
dir_id = input("Enter GoogleDrive directory ID: ")
get_files_from_dir(dir_id, local_download_path)
