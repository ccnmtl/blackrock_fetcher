#!ve/bin/python
"""
Updated 2022-06-21: SFTP from a remote server changed to Google Drive
API requests.

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

"""
import requests
import sys
import os
import os.path
from datetime import datetime
from blackrock_data_processor import (
    process_dendrometer_data, process_environmental_data,
    apply_formula_to_processed_dendrometer_data
)

try:
    from local_settings import (
        API_KEY, VIRTUAL_FOREST_ID,
        METADATA_URI, FILE_URI,
        OL_EXPECTED_FILES_SET,
        RT_EXPECTED_FILES_SET, LOCAL_DIRECTORY_BASE,
        PURGE_OLDER_THAN, DEBUG,
    )
except ImportError:
    from example_settings import (
        API_KEY, VIRTUAL_FOREST_ID,
        METADATA_URI, FILE_URI,
        OL_EXPECTED_FILES_SET,
        RT_EXPECTED_FILES_SET, LOCAL_DIRECTORY_BASE,
        PURGE_OLDER_THAN, DEBUG,
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


def find_files(items):
    """
    Runs in fetch_files()
    Recursively creates a list of files present in current and sub directories
    """
    file_list = []
    for item in items:
        if item['mimeType'] == 'application/vnd.google-apps.folder':
            subfolder = get_api_response(METADATA_URI, item['id'])
            file_list.extend(find_files(subfolder.json()['files']))
        else:
            file_list.append(item)
    return file_list


def fetch_files(local_dir):
    if DEBUG:
        print("Fetching from Google Drive to %s" % (local_dir))
    virtual_forest = get_api_response(METADATA_URI, VIRTUAL_FOREST_ID)
    download_files = find_files(virtual_forest.json()['files'])
    for item in download_files:
        to_download = get_api_response(FILE_URI, item['id'])
        open('%s/%s' % (local_dir, item['name']),
             'wb').write(to_download.content)


def get_api_response(uri, file_id):
    return requests.get(uri.format(file_id, API_KEY))


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
