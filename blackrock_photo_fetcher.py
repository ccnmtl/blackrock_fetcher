#!ve/bin/python
"""
This script fetches webcam photos from the blackrock servers.

The script is meant to be called from cron,

blackrock_photo_fetcher.py

Black Rock forest is taking a snapshot every minute, and writing over
the same file each minute We want to pull down this file regularly,
and store it locally.

We will store the photos in a directory structure like

YYYY/MM/DD/<FILENAME>_HOUR_MIN.jpg

Jonah Bossewitch, CCNMTL

"""
from __future__ import print_function

import sys
import io
import os
import os.path
from subprocess import call
import datetime

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload

try:
    from local_settings import (
        SCOPES, REMOTE_FILENAME,
        LOCAL_WEBCAM_DIRECTORY_BASE,
        LOCAL_FILENAME_PREFIX, CONVERT, DEBUG,
    )
except ImportError:
    from example_settings import (
        SCOPES, REMOTE_FILENAME,
        LOCAL_WEBCAM_DIRECTORY_BASE,
        LOCAL_FILENAME_PREFIX, CONVERT, DEBUG,
    )


def create_local_directories(today):
    """
    Create local directories for today's date, if they don't yet exist
    """
    d = "%s/%s" % (LOCAL_WEBCAM_DIRECTORY_BASE, today.strftime("%Y/%m/%d"))
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


def copy_photo_to_dir(service, file_metadata, local_path):
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
                    open(local_path, 'wb').write(to_download.getvalue())
            except UnicodeDecodeError as error:
                print(F"Corrupted File - {file_metadata['name']}  - {error}")
                done = False
    except HttpError as error:
        print(f'An error occurred: {error}')
        to_download = None


def fetch_image(local_path):
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
            print('Searching:')
        for item in items:
            if item['name'] == REMOTE_FILENAME:
                copy_photo_to_dir(service, item, local_path)
    except HttpError as error:
        print(f'An error occurred: {error}')


def main(argv=None):
    today = datetime.datetime.today()

    local_dir = create_local_directories(today)

    hour_min = today.strftime("%H_%M")

    new_filename = "%s_%s.jpg" % (LOCAL_FILENAME_PREFIX, hour_min)
    new_thumbname = "%s_%s_thumb.jpg" % (LOCAL_FILENAME_PREFIX, hour_min)

    local_path = "%s/%s" % (local_dir, new_filename)
    local_thumb_path = "%s/%s" % (local_dir, new_thumbname)
    fetch_image(local_path)

    # create a thumbnail
    call([CONVERT,
          '-resize',
          '207x207',
          local_path,
          local_thumb_path,
          ])

    # make sure the images are world readable
    os.chmod(local_path, 0o644)
    os.chmod(local_thumb_path, 0o644)

    # create a symlink to the most current image
    symlink = LOCAL_WEBCAM_DIRECTORY_BASE + "/current.jpg"
    symlink_thumb = LOCAL_WEBCAM_DIRECTORY_BASE + "/current_thumb.jpg"

    try:
        os.remove(symlink)
        os.remove(symlink_thumb)
    except OSError:
        pass

    os.symlink(local_path, symlink)
    os.symlink(local_thumb_path, symlink_thumb)

    if DEBUG:
        print("Fetched.")


if __name__ == "__main__":
    sys.exit(main())
