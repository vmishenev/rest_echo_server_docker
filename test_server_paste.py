#!/usr/bin/python
# -*- coding: utf-8 -*-

from paste.fixture import TestApp

from server import app
import unittest
import json


class TestServer(unittest.TestCase):

    def test_notfound(self):
        middleware = []
        testApp = TestApp(app.wsgifunc(*middleware))
        r = testApp.get('/storage/test', status="*")
        self.assertEqual(r.status, 404)

    def test_add(self):
        middleware = []
        testApp = TestApp(app.wsgifunc(*middleware))
        key = 'test2'
        message = 'jhfsdf'
        obj_data = {'key': key, 'message': message}
        r1 = testApp.post('/storage/' + key, params=json.dumps(obj_data))
        r = testApp.get('/storage/' + key)
        self.assertEqual(r1.status, 200)
        self.assertEqual(r.status, 200)
        self.assertEqual(json.loads(r.body.decode('utf-8'))['message'], message)

    def test_delete(self):
        middleware = []
        testApp = TestApp(app.wsgifunc(*middleware))
        key = 'test3'
        message = 'jhfsdf'
        obj_data = {'key': key, 'message': message}
        r1 = testApp.post('/storage/' + key, params=json.dumps(obj_data))
        r = testApp.get('/storage/' + key)
        self.assertEqual(r1.status, 200)
        self.assertEqual(r.status, 200)
        self.assertEqual(json.loads(r.body.decode('utf-8'))['message'], message)
        r3 = testApp.delete('/storage/' + key)
        r4 = testApp.get('/storage/'+ key, status="*")
        self.assertEqual(r4.status, 404)

if __name__ == '__main__':
    unittest.main()

