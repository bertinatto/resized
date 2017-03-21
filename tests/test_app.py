import io
import json
import unittest

from resized.app import create_app
from resized.settings import Settings


class APITestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(Settings)
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

    def tearDown(self):
        self.app_context.pop()

    def test_404(self):
        response = self.client.get('/wrong/url')
        self.assertTrue(response.status_code == 404)

    def test_upload_image(self):
        with open('tests/data/earth.jpg', 'rb') as fd:
            img = dict(file=(io.BytesIO(fd.read()), 'earth.jpg'))
            resp = self.client.post('/api/image',
                                    content_type='multipart/form-data',
                                    data=img)

            self.assertEqual(resp.status_code, 200)
            jresp = json.loads(resp.data)
            self.assertTrue(jresp['success'])

            resp_images = self.client.get('/image/{0}'.format(jresp['token']))
            self.assertEqual(resp_images.status_code, 200)
