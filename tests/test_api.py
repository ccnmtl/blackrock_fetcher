import unittest
from blackrock_data_fetcher import get_api_response
from requests import Response

try:
    from local_settings import (
        FILE_URI, METADATA_URI, VIRTUAL_FOREST_ID
    )
except ImportError:
    from example_settings import (
        FILE_URI, METADATA_URI, VIRTUAL_FOREST_ID
    )


RESPONSE_CLASS = Response()
FOLDER_MIMETYPE = 'application/vnd.google-apps.folder'


class TestMetadataRequest(unittest.TestCase):
    response = get_api_response(METADATA_URI, VIRTUAL_FOREST_ID)

    def test_get__directory_response(self):
        self.assertIsInstance(self.response, type(Response()))

    def test_response_status_code(self):
        self.assertEqual(200, self.response.status_code)

    def test_response_type(self):
        self.assertEqual(self.response.json()['kind'], 'drive#fileList')

    def test_directory_is_not_empty(self):
        self.assertGreater(len(self.response.json()['files']), 0)


class TestFileRequest(unittest.TestCase):
    response = get_api_response(METADATA_URI, VIRTUAL_FOREST_ID)
    # Migrate to a file
    re_json = response.json()['files'][0]
    while re_json['mimeType'] == FOLDER_MIMETYPE:
        response = get_api_response(
            METADATA_URI,
            re_json['id'])
        re_json = response.json()['files'][0]
    response = get_api_response(FILE_URI, re_json['id'])

    def test_get_file_respnose(self):
        self.assertIsInstance(self.response, type(Response()))

    def test_response_status_code(self):
        self.assertEqual(200, self.response.status_code)


if __name__ == '__main__':
    unittest.main()
