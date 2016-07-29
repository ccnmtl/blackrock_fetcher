#!ve/bin/python
"""
This script fetches webcam photos from the blackrock servers.

The script is meannt to be called from cron,

blackrock_photo_fetcher.py

Black Rock forest is taking a snapshot every minute, and writing over
the same file each minute We want to pull down this file regularly,
and store it locally.

We will store the photos in a directory structure like

YYYY/MM/DD/<FILENAME>_HOUR_MIN.jpg

Jonah Bossewitch, CCNMTL

"""
import sys
import os
import os.path
from subprocess import call
import datetime
import pexpect

try:
    from local_settings import (
        SFTP_HOST, SFTP_PORT, SFTP_USER, SFTP_PASSWD,
        REMOTE_DIRECTORY, REMOTE_FILENAME,
        LOCAL_WEBCAM_DIRECTORY_BASE, LOCAL_FILENAME_PREFIX,
        SCP, CONVERT, DEBUG,
    )
except ImportError:
    from example_settings import (
        SFTP_HOST, SFTP_PORT, SFTP_USER, SFTP_PASSWD,
        REMOTE_DIRECTORY, REMOTE_FILENAME,
        LOCAL_WEBCAM_DIRECTORY_BASE, LOCAL_FILENAME_PREFIX,
        SCP, CONVERT, DEBUG,
    )


def create_local_directories(today):
    """
    Create local directories for today's date, if they don't yet exist
    """
    # year = today.strftime("%Y")
    # month = today.strftime("%m")
    # day = today.strftime("%d")

    dir = "%s/%s" % (LOCAL_WEBCAM_DIRECTORY_BASE, today.strftime("%Y/%m/%d"))

    if not os.path.exists(dir):
        os.makedirs(dir)

    return dir


def fetch_image(remote_path, local_path):
    if DEBUG:
        print("Fetching %s to %s" % (remote_path, local_path))

    cmd = '%s -P %s %s@%s:"%s" %s ' % (
        SCP, SFTP_PORT, SFTP_USER, SFTP_HOST, remote_path, local_path)
    if DEBUG:
        print("cmd: %s" % (cmd))

    try:
        # import pdb; pdb.set_trace()
        child = pexpect.spawn(cmd)
        child.expect('password:')
        child.sendline(SFTP_PASSWD)
        child.expect(pexpect.EOF)
    except:
        print("SCP Error:", sys.exc_info()[0])
        raise


def main(argv=None):
    # import pdb; pdb.set_trace()
    today = datetime.datetime.today()

    local_dir = create_local_directories(today)

    hour_min = today.strftime("%H_%M")

    new_filename = "%s_%s.jpg" % (LOCAL_FILENAME_PREFIX, hour_min)
    new_thumbname = "%s_%s_thumb.jpg" % (LOCAL_FILENAME_PREFIX, hour_min)

    remote_path = "%s/%s" % (REMOTE_DIRECTORY, REMOTE_FILENAME)
    local_path = "%s/%s" % (local_dir, new_filename)
    local_thumb_path = "%s/%s" % (local_dir, new_thumbname)
    # print remote_path, local_path
    fetch_image(remote_path, local_path)

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
    except:
        pass

    os.symlink(local_path, symlink)
    os.symlink(local_thumb_path, symlink_thumb)

    if DEBUG:
        print("Fetched.")

if __name__ == "__main__":
    sys.exit(main())
