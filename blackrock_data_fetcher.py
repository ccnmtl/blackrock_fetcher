#!ve/bin/python
"""
This script fetches live data from the blackrock servers.

The script is meant to be called from cron, with no arguments

blackrock_data_fetcher.py

Black Rock forest is taking a snapshot hour minute, and writing over
the same file each minute We want to pull down these files regularly,
and store it locally.

We will store the photos in a directory structure like

YYYY/MM/DD/HH/<FILENAMES>.jpg

Jonah Bossewitch, CCNMTL

"""
import sys
import os
import os.path
import datetime
import pexpect
from blackrock_data_processor import process

try:
    from local_settings import (
        SFTP_HOST, SFTP_PORT, SFTP_USER, SFTP_PASSWD,
        OL_REMOTE_IMAGES_DIRECTORY, RT_REMOTE_IMAGES_DIRECTORY,
        REMOTE_CSV_DIRECTORY, REMOTE_MOUNT_MISERY_DIRECTORY,
        REMOTE_WHITE_OAK_DIRECTORY, OL_EXPECTED_FILES_SET,
        RT_EXPECTED_FILES_SET, LOCAL_DIRECTORY_BASE,
        SCP, PURGE_OLDER_THAN, DEBUG,
    )
except ImportError:
    from example_settings import (
        SFTP_HOST, SFTP_PORT, SFTP_USER, SFTP_PASSWD,
        OL_REMOTE_IMAGES_DIRECTORY, RT_REMOTE_IMAGES_DIRECTORY,
        REMOTE_CSV_DIRECTORY, REMOTE_MOUNT_MISERY_DIRECTORY,
        REMOTE_WHITE_OAK_DIRECTORY, OL_EXPECTED_FILES_SET,
        RT_EXPECTED_FILES_SET, LOCAL_DIRECTORY_BASE,
        SCP, PURGE_OLDER_THAN, DEBUG,
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


def fetch_files(remote_dir, local_dir):
    if DEBUG:
        print("Fetching %s to %s" % (remote_dir, local_dir))

    cmd = '%s -r -P %s %s@%s:"%s/*" %s ' % (
        SCP, SFTP_PORT, SFTP_USER, SFTP_HOST, remote_dir, local_dir)
    if DEBUG:
        print("cmd: %s" % (cmd))

    try:
        child = pexpect.spawn(cmd)
        child.expect('password:')
        child.sendline(SFTP_PASSWD)
        # make sure to extend the timeout for long download times. 5
        # min should do it.
        child.expect(pexpect.EOF, timeout=600)
    except:
        print("SCP Error:", sys.exc_info()[0])
        raise Exception()


def main(argv=None):
    # import pdb; pdb.set_trace()
    today = datetime.datetime.today()

    local_dir = create_local_directories(today)

    fetch_files(OL_REMOTE_IMAGES_DIRECTORY, local_dir)
    fetch_files(RT_REMOTE_IMAGES_DIRECTORY, local_dir)
    fetch_files(REMOTE_CSV_DIRECTORY, local_dir)
    fetch_files(REMOTE_MOUNT_MISERY_DIRECTORY, local_dir)
    fetch_files(REMOTE_WHITE_OAK_DIRECTORY, local_dir)
    process(os.path.join(local_dir, 'Mnt_Misery_Table20.csv'))

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
        os.chmod(local_dir + "/" + f, 0o644)

    # make a symlink to the most current directory of images
    symlink = symlink = LOCAL_DIRECTORY_BASE + "/current"
    try:
        os.remove(symlink)
    except:
        pass

    os.symlink(local_dir, symlink)

    if DEBUG:
        print("Fetched.")

    # purge downloads older than PURGE_OLDER_THAN
    cmd = "find %s -type f -mtime %s -exec rm -f {} \;" % (
        LOCAL_DIRECTORY_BASE, PURGE_OLDER_THAN)
    if DEBUG:
        print(cmd)

    os.system(cmd)

if __name__ == "__main__":
    sys.exit(main())
