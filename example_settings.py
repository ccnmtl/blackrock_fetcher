# Copy this file to local_settings.py and customize.

SFTP_HOST = ''
SFTP_USER = ''
SFTP_PASSWD = ''

OL_REMOTE_IMAGES_DIRECTORY = '/OL_Display_Screens'
RT_REMOTE_IMAGES_DIRECTORY = '/RT_Display_Screens'
REMOTE_CSV_DIRECTORY = '/Datalogger_Files'
REMOTE_MOUNT_MISERY_DIRECTORY = '/Mount_Misery_LTP'
REMOTE_WHITE_OAK_DIRECTORY = '/White_Oak_LTP'
REMOTE_MAILLEYS_MILL_DIRECTORY = '/Mailley\\\'s_Mill'

OL_EXPECTED_FILES_SET = set(
    ('OL_Air-Soil-7Day.png', 'OL_Air-Soil-24Hr.png', 'OL_Air-Soil-30Day.png',
     'OL_Baro-7Day.png', 'OL_Baro-24Hr.png', 'OL_Baro-30Day.png',
     'OL_CO2-7Day.png', 'OL_CO2-24Hr.png', 'OL_CO2-30Day.png',
     'OL_Ozone-7Day.png', 'OL_Ozone-24Hr.png', 'OL_Ozone-30Day.png',
     'OL_Precip-7Day.png', 'OL_Precip-24Hr.png', 'OL_Precip-30Day.png',
     'OL_Wind-7Day.png', 'OL_Wind-24Hr.png', 'OL_Wind-30Day.png',
     'Widget.png'))

RT_EXPECTED_FILES_SET = set(
    ('RT_Air-Soil-7Day.png', 'RT_Air-Soil-24Hr.png', 'RT_Air-Soil-30Day.png',
     'RT_Baro-7Day.png', 'RT_Baro-24Hr.png', 'RT_Baro-30Day.png',
     'RT_Precip-7Day.png', 'RT_Precip-24Hr.png', 'RT_Precip-30Day.png',
     'RT_Wind-7Day.png', 'RT_Wind-24Hr.png', 'RT_Wind-30Day.png'))

LOCAL_DIRECTORY_BASE = '/tmp/blackrock/'

SCP = '/usr/bin/sftp'
CONVERT = '/usr/bin/convert'

PURGE_OLDER_THAN = '+30'

DEBUG = True

REMOTE_DIRECTORY = '/Camera_Photo'
REMOTE_FILENAME = 'Lodge.jpg'
LOCAL_WEBCAM_DIRECTORY_BASE = ''
LOCAL_FILENAME_PREFIX = 'Black_Rock'

PROCESSED_DATA_DIR = '/tmp/processed/'
