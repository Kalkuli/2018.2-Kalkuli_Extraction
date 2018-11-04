from project.tests.base import BaseTestCase
import json, io

class TestExtraction(BaseTestCase):
    def test_extract_no_file(self):
        response = self.client.post(
            '/extract',
            content_type='multipart/form-data'
        )

        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 422)
        self.assertIn(data["Error"], "No file sent")

    def test_extract_invalid_extension(self):
        post_data = {}
        post_data['file'] = (io.BytesIO(b"abcdef"), 'test.jpg')

        response = self.client.post(
            '/extract',
            data=post_data,
            content_type='multipart/form-data'
        )

        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 415)
        self.assertIn(data["Error"], "Extension not allowed. Use PDF.")
