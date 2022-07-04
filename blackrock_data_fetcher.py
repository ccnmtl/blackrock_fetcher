#!ve/bin/python
"""
This script fetches live data from the blackrock Google Drive server.
=====================================================================
The script is meant to be called from cron, with no arguments

blackrock_data_fetcher.py

Black Rock forest is taking a snapshot hour minute, and writing over
the same file each minute We want to pull down these files regularly,
and store it locally.

We will store the photos in a directory structure like

YYYY/MM/DD/HH/<FILENAMES>.jpg

Jonah Bossewitch, CCNMTL
Modified: 2022_06_28, Evan Petersen, CTL
"""
from __future__ import print_function

import sys
import io
import os
import os.path
from datetime import datetime

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload

from blackrock_data_processor import (
    process_dendrometer_data, process_environmental_data,
    apply_formula_to_processed_dendrometer_data
)

try:
    from local_settings import (
        SCOPES, DIR_MIMETYPE, ACCEPTED_FILETYPES,
        OL_EXPECTED_FILES_SET, RT_EXPECTED_FILES_SET,
        LOCAL_DIRECTORY_BASE, PURGE_OLDER_THAN, DEBUG,
    )
except ImportError:
    from example_settings import (
        SCOPES, DIR_MIMETYPE, ACCEPTED_FILETYPES,
        OL_EXPECTED_FILES_SET, RT_EXPECTED_FILES_SET,
        LOCAL_DIRECTORY_BASE, PURGE_OLDER_THAN, DEBUG,
    )


def create_local_directories(today):
    """
    Create local directories for today's date, if they don't yet exist
    """
    d = "%s/%s" % (LOCAL_DIRECTORY_BASE, today.strftime("%Y/%m/%d/%H"))
    d = os.path.normpath(d)

    if not os.path.exists(d):
        os.makedirs(d)

    return d


def get_credentials():
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
    return creds


def check_format(filename):
    for filetype in ACCEPTED_FILETYPES:
        if filename.endswith(filetype):
            return True
    return False


def copy_file_to_dir(service, file_metadata, local_dir):
    try:
        request = service.files().get_media(fileId=file_metadata['id'])
        to_download = io.BytesIO()
        downloader = MediaIoBaseDownload(to_download, request)
        done = False
        while done is False:
            try:
                status, done = downloader.next_chunk()
                if DEBUG:
                    print(file_metadata['name'])
                    open(F"{local_dir}/{file_metadata['name']}",
                         'wb').write(to_download.getvalue())
            except UnicodeDecodeError as error:
                print(F"Corrupted File - {file_metadata['name']}  - {error}")
                done = False
    except HttpError as error:
        print(f'An error occurred: {error}')
        to_download = None


def fetch_files(local_dir):
    creds = get_credentials()
    try:
        service = build('drive', 'v3', credentials=creds)
        # Call the Drive v3 API
        results = service.files().list(
             fields="nextPageToken, files(id, name, mimeType)").execute()
        items = results.get('files', [])
        if not items:
            if DEBUG:
                print('No files found.')
            return None
        if DEBUG:
            print('Files:')
        for item in items:
            if item['mimeType'] != DIR_MIMETYPE and check_format(item['name']):
                copy_file_to_dir(service, item, local_dir)
    except HttpError as error:
        print(f'An error occurred: {error}')


def main(argv=None):
    # import pdb; pdb.set_trace()
    today = datetime.today()

    local_dir = create_local_directories(today)

    fetch_files(local_dir)

    process_dendrometer_data(local_dir, 'Mnt_Misery_Table20.csv')
    apply_formula_to_processed_dendrometer_data(
        'Mnt_Misery_Table20.csv',
        # The DBH (diameter at breast height) for each of these
        # trees on October 7th, 2016 at 2pm.
        # Unit is centimeters.
        [48.0, 40.1, 42.1, 46.0, 42.4],
        # The dendrometer voltages at that same time.
        [20.9, 19.23, 20.93, 316.5, 120.9])

    process_dendrometer_data(local_dir, 'White_Oak_Table20.csv',
                             rename_trees='White_Oak')
    apply_formula_to_processed_dendrometer_data(
        'White_Oak_Table20.csv',
        # The DBH (diameter at breast height) for each of these
        # trees on October 7th, 2016 at 2pm.
        # Unit is centimeters.
        [32.1, 33.3, 46.7, 30.0, 26.7],
        # The dendrometer voltages at that same time.
        [160.8, 71.33, 100.4, 277.4, 456.6])

    process_dendrometer_data(local_dir, 'Mailley\'s_Mill_Table20Min.csv')
    process_environmental_data(local_dir, 'Lowland.csv',
                               start_dt=datetime(2016, 9, 10, 17))

    listdir = os.listdir(local_dir)

    if DEBUG:
        print("listdir: %s" % listdir)

    # confirm that we downloaded all the files we are expecting.
    # throw an error and bail (making sure not to relink the 'current'
    # symlink if things aren't as expected
    if not (set(listdir).issuperset(OL_EXPECTED_FILES_SET)):
        err = "Data fetching error: Some expected files not found at %s" % (
            OL_EXPECTED_FILES_SET - set(listdir))
        raise Exception(err)
    if not (set(listdir).issuperset(RT_EXPECTED_FILES_SET)):
        err = "Data fetching error: Some expected files not found at %s" % (
            RT_EXPECTED_FILES_SET - set(listdir))
        raise Exception(err)

    # make sure all the images are world readable
    for f in listdir:
        os.chmod(os.path.join(local_dir, f), 0o644)

    # make a symlink to the most current directory of images
    symlink = os.path.join(LOCAL_DIRECTORY_BASE, 'current')
    try:
        os.remove(symlink)
    except OSError:
        print('couldn\'t remove symlink: %s' % symlink)

    try:
        os.symlink(local_dir, symlink)
    except OSError:
        print('couldn\'t make symlink: %s' % symlink)

    # purge downloads older than PURGE_OLDER_THAN
    cmd = "find %s -type f -mtime %s -exec rm -f {} \;" % (
        LOCAL_DIRECTORY_BASE, PURGE_OLDER_THAN)
    if DEBUG:
        print("Fetched.")
        print(cmd)

    os.system(cmd)


if __name__ == "__main__":
    sys.exit(main())
