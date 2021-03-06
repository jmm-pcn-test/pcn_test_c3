from app import app
import unittest

import random

class FlaskAppTests(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing=True

    def test_users_status_code(self):
        result = self.app.get('/api/v1/users')
        self.assertEqual(result.status_code, 200)

    def test_addusers_status_code(self):
        result = self.app.post(
            '/api/v1/users',
            data='{"username":"dumb", "email":"dumb@abc.abc", "password":"test123", "name":"dumb"}',
            content_type='application/json')
        result = self.app.post(
            '/api/v1/users',
            data='{"username":"jonathan%s", "email":"%s@abc.abc", "password":"test123", "name":"jon"}' % (random.randint(0,100),random.randint(0,100)),
            content_type='application/json')
        print(result)
        self.assertEqual(result.status_code,201)

    def test_updusers_status_code(self):
        result = self.app.put(
            '/api/v1/users/4',
            data='{"password":"testing123"}',
            content_type='application/json'
        )
        self.assertEqual(result.status_code,200)

    def test_delusers_status_code(self):
        result = self.app.delete(
            '/api/v1/users',
            data='{"username":"dumb"}',
            content_type='application/json'
        )
        self.assertEqual(result.status_code, 200)

    def test_addtweet_status_code(self):
        result = self.app.post('/api/v2/tweets',
                               data='{"username":"a", "body":"Something %s"}'%(random.randint(0,10000)),
                               content_type='application/json')
        self.assertEqual(result.status_code, 201)

    def test_get_tweets(self):
        result = self.app.get('/api/v2/tweets')
        self.assertEqual(result.status_code, 200)

