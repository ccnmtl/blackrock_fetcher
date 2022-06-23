# Copy this file to local_settings.py and customize.

API_KEY = '<INSERT_API_KEY>'
VIRTUAL_FOREST_ID = '1g7AuUZiwYQhM2RCS7ztFXtK6sH7NFk9J'
METADATA_URI = ('https://www.googleapis.com/drive/v3/'
                'files?q=%27{0}%27+in+parents&key={1}')
FILE_URI = 'https://www.googleapis.com/drive/v3/files/{0}?alt=media&key={1}'

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

CONVERT = '/usr/bin/convert'

PURGE_OLDER_THAN = '+30'

DEBUG = True

REMOTE_FILENAME = 'Lodge.jpg'
LOCAL_WEBCAM_DIRECTORY_BASE = ''
LOCAL_FILENAME_PREFIX = 'Black_Rock'

PROCESSED_DATA_DIR = '/tmp/processed/'
