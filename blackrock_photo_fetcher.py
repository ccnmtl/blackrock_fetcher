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
import requests
import sys
import os
import os.path
from subprocess import call
import datetime

try:
    from local_settings import (
        API_KEY, VIRTUAL_FOREST_ID,
        METADATA_URI, FILE_URI, REMOTE_FILENAME,
        LOCAL_WEBCAM_DIRECTORY_BASE, LOCAL_FILENAME_PREFIX,
        CONVERT, DEBUG,
    )
except ImportError:
    from example_settings import (
        API_KEY, VIRTUAL_FOREST_ID,
        METADATA_URI, FILE_URI, REMOTE_FILENAME,
        LOCAL_WEBCAM_DIRECTORY_BASE, LOCAL_FILENAME_PREFIX,
        CONVERT, DEBUG,
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


def find_file_id(directory_id):
    found = None
    subfolder = []
    response = requests.get(METADATA_URI.format(directory_id, API_KEY))
    for item in response.json()['files']:
        if item['mimeType'] == 'application/vnd.google-apps.folder':
            subfolder.append(item['id'])
        if item['name'] == REMOTE_FILENAME:
            found = item['id']
    i = 0
    while found is None and i < len(subfolder):
        find_file_id(subfolder[i])
        i += 1
    return found


def fetch_image(local_path):
    if DEBUG:
        print("Fetching {0} from Google Drive to {1}".
              format(REMOTE_FILENAME, local_path))
    found = find_file_id(VIRTUAL_FOREST_ID)
    if found is None:
        raise NameError('%s not found in GDrive' % (REMOTE_FILENAME))
    response = requests.get(FILE_URI.format(found, API_KEY))
    open('{0}'.format(local_path), 'wb').write(response.content)


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
